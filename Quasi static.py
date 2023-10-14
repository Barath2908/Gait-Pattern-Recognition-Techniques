import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def detect_gait_phases(data, ms_threshold):
    ms = []
    hs = []
    to = []
    zero_crossings = []
    ms_detected = False
    hs_detected = False
    cycle_start = 0
    cycle_end = 125

    while cycle_end <= len(data):
        current_cycle = data[cycle_start:cycle_end]

        for i in range(len(current_cycle)):
            if current_cycle[i] >= ms_threshold:
                if not ms_detected:
                    ms.append([cycle_start + i, current_cycle[i]])
                    ms_detected = True
                elif ms_detected and ms[-1][0] + 27 < cycle_start + i:
                    ms.append([cycle_start + i, current_cycle[i]])

            if ms_detected and current_cycle[i] < 0 and current_cycle[i - 1] > 0:
                hs.append([cycle_start + i, current_cycle[i]])
                hs_detected = True

            if len(ms) > 0 and len(hs) > 0 and hs[-1][0] - ms[-1][0] > 100 and current_cycle[i] > 0 and current_cycle[
                i - 1] < 0:
                zero_crossings.append([cycle_start + i, current_cycle[i]])

        if len(zero_crossings) > 0:
            min_val = float('inf')
            min_index = -1
            for i in range(len(ms)):
                if zero_crossings[0][0] - ms[i][0] > 0 and ms[i][1] < min_val:
                    min_val = ms[i][1]
                    min_index = i
            if min_index != -1:
                to.append([zero_crossings[0][0], zero_crossings[0][1]])

        cycle_start += 125
        cycle_end += 125
        ms_detected = False
        hs_detected = False

    return ms, hs, to


# Read Excel file
df = pd.read_excel("C:/Users/ibra5/Desktop/Internships/GAC/Test_source.xlsx")
shank_angular_velocity = df['Shank angular velocity'].tolist()

# Define MS threshold and detect gait phases
ms_threshold = 0.0005
ms, hs, to = detect_gait_phases(shank_angular_velocity, ms_threshold)

# Plot graph
plt.plot(shank_angular_velocity)
plt.xlabel('Sample')
plt.ylabel('Shank Angular Velocity')

# Draw vertical lines for MS, HS, and TO phases
for ms_phase in ms:
    plt.axvline(x=ms_phase[0], color='b', linestyle='--')  # MS phase

for hs_phase in hs:
    plt.axvline(x=hs_phase[0], color='g', linestyle='--')  # HS phase

for to_phase in to:
    plt.axvline(x=to_phase[0], color='r', linestyle='--')  # TO phase

plt.show()
