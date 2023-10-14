import pandas as pd
import matplotlib.pyplot as plt

def detect_gait_phases(data):
    fc = 10  # Cut-off frequency (Hz)
    samples = len(data)
    w = [0] * (samples + 1)
    mst = msw = ic = to = 0
    phases = []

    for i in range(1, samples):
        w[i] = round(i / fc) + 1

        if max(data[:i]) > 0 and msw == 0 and data[i] < data[i-1]:
            msw = 1
            to = 0
            if len(phases) % 66 == 0:  # Only add the phase if it's the first one after every 66 samples
                phases.append('MsW')
        elif data[i] > data[i-1]:
            ic = 1
            if len(phases) % 66 == 0:
                phases.append('IC')
        else:
            ic += 1
            if len(phases) % 66 == 0:
                phases.append(None)

        if ic == 1:
            if w[i] == round(i / fc) + 1:
                mst = 1
                if len(phases) % 66 == 0:
                    phases[-1] = 'Mst'

        if mst == 1:
            to = 1
            mst = msw = ic = 0
            if len(phases) % 66 == 0:
                phases[-1] = 'TO'

        if mst != 1 and sum(w[:i]) < sum(w[:i-1]):
            mst = 1
            i = i * fc + 10
            if len(phases) % 66 == 0:
                phases[-1] = 'Mst'

    return phases

# Read Excel file
df = pd.read_excel("C:/Users/ibra5/Desktop/Internships/GAC/Test_source.xlsx")
shank_angular_velocity = df['Foot angular velocity'].tolist()

# Chunk size for repeating the analysis
chunk_size = 66

# Detect gait phases
gait_phases = detect_gait_phases(shank_angular_velocity)

# Keep only one phase for each repetition
gait_phases = [phase for i, phase in enumerate(gait_phases) if i % chunk_size == 0]

# Plot graph
plt.plot(shank_angular_velocity)
plt.xlabel('Sample')
plt.ylabel('Foot Angular Velocity')

# Draw vertical lines for detected gait phases
for i in range(len(gait_phases)):
    if gait_phases[i] == 'MsW':
        plt.axvline(x=i*chunk_size, color='b', linestyle='--')  # MsW phase
    elif gait_phases[i] == 'IC':
        plt.axvline(x=i*chunk_size, color='g', linestyle='--')  # IC phase
    elif gait_phases[i] == 'Mst':
        plt.axvline(x=i*chunk_size, color='m', linestyle='--')  # Mst phase
    elif gait_phases[i] == 'TO':
        plt.axvline(x=i*chunk_size, color='r', linestyle='--')  # TO phase

plt.show()

