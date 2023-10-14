import pandas as pd
import matplotlib.pyplot as plt

# Read the input data from the Excel file
data = pd.read_excel('Values.xlsx')
right_knee_flexion_angle = data['Right knee flexion angle']

# Initialize variables
total_samples = 75
mmst_counter = 7
mmsw_detected = False
hs_detected = False
ff_detected = False
ho_detected = False
mmst_detected = False
to_detected = False

right_knee_flexion_angle_maxima = right_knee_flexion_angle.idxmax()
right_knee_flexion_angle_minima = right_knee_flexion_angle.idxmin()

# Create a list to store the indices of detected phases
mmsw_indices = []
hs_indices = []
ff_indices = []
ho_indices = []
mmst_indices = []
to_indices = []

# Detect phases for each sample in the gait cycle
for i in range(total_samples):
    current_angle = right_knee_flexion_angle[i]
    previous_angle = right_knee_flexion_angle[i - 1] if i > 0 else None
    pre_previous_angle = right_knee_flexion_angle[i - 2] if i > 1 else None

    if (
            previous_angle is not None and current_angle is not None and pre_previous_angle is not None and
            0 <= abs(previous_angle - current_angle) < 0.2 and
            right_knee_flexion_angle_minima is not None and
            (i - right_knee_flexion_angle_maxima) <= 0.15 * total_samples or (
            i - right_knee_flexion_angle_maxima) <= 1.0 * total_samples
    ):
        ff_indices.append(i)
        ff_detected = True

    if (
            current_angle is not None and
            previous_angle is not None and current_angle is not None and pre_previous_angle is not None and
            current_angle < 0 and
            previous_angle - current_angle < 0 and
            pre_previous_angle - previous_angle < 0 and
            (previous_angle - current_angle) > 0.9 * (pre_previous_angle - previous_angle) and
            (i - right_knee_flexion_angle_maxima) <= 0.3 * total_samples or (
            i - right_knee_flexion_angle_maxima) <= 1.0 * total_samples
    ):
        ho_indices.append(i)
        ho_detected = True

# Plot the graph with colored vertical lines indicating detected phases
plt.plot(right_knee_flexion_angle)

if ff_detected:
    plt.axvline(x=ff_indices[0], color='b', linestyle='--', label='FF')
if ho_detected:
    plt.axvline(x=ho_indices[0], color='m', linestyle='--', label='HO')

plt.legend()
plt.show()
