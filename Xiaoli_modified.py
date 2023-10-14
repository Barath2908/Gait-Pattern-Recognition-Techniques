import pandas as pd
import matplotlib.pyplot as plt

# Load the data from the Excel file
data = pd.read_excel('C:/Users/ibra5/Desktop/GAC/Xiaoli/Values.xlsx')

# Extract the required columns
right_angular_velocity = data['Right foot angular velocity']
left_angular_velocity = data['Left foot angular velocity']
right_knee_flexion_angle = data['Right knee flexion angle']

# Define the gait cycle length
cycle_length = 124

# Initialize empty lists for storing the detected gait events
mswr = []
mswl = []
to = []
hs = []
fa = []
ho = []
ot = []
oh = []

# Iterate over the data in cycles of length cycle_length
for i in range(0, len(data), cycle_length):
    cycle_right_angular_velocity = right_angular_velocity[i:i+cycle_length]
    cycle_left_angular_velocity = left_angular_velocity[i:i+cycle_length]
    cycle_right_knee_flexion_angle = right_knee_flexion_angle[i:i+cycle_length]

    # MSwR detection
    if cycle_right_angular_velocity.idxmax() < cycle_length:
        mswr.append(i + cycle_right_angular_velocity.idxmax())

    # MSwL detection
    if cycle_left_angular_velocity.idxmax() < cycle_length:
        mswl.append(i + cycle_left_angular_velocity.idxmax())

    # TO detection
    if cycle_left_angular_velocity.idxmin() < cycle_length:
        to.append(i + cycle_left_angular_velocity.idxmin())

    # HS detection
    if mswr and to:
        cycle_right_angular_velocity_zero_crossings = cycle_right_angular_velocity.diff().apply(lambda x: x > 0)
        crossings_after_to_mswr = cycle_right_angular_velocity_zero_crossings[to[-1]:mswr[-1]+cycle_length].values
        hs_idx = to[-1] + cycle_right_angular_velocity_zero_crossings[to[-1]:mswr[-1]+cycle_length][crossings_after_to_mswr].index[0]
        hs.append(hs_idx)

    # FA detection
    fa.append(i + cycle_right_knee_flexion_angle.idxmax())

    # HO detection
    if mswl:
        mswl_idx = mswl[-1]
        mswl_right_knee_flexion_angle = cycle_right_knee_flexion_angle[mswl_idx:mswl_idx+cycle_length]
        if (cycle_right_knee_flexion_angle[mswl_idx] > mswl_right_knee_flexion_angle).any() and (cycle_left_angular_velocity[0] < 0):

            ho.append(i + cycle_right_knee_flexion_angle.idxmin())

    # OT detection
    ot.append(i + cycle_right_angular_velocity.idxmin())

    # OH detection
    if to and ho:
        oh_idx = (to[-1] + ho[-1]) // 2
        oh.append(oh_idx)

# Plotting the detected events
plt.plot(right_angular_velocity, color='black', label='Right Foot Angular Velocity')
plt.plot(left_angular_velocity, color='blue', label='Left Foot Angular Velocity')
plt.plot(right_knee_flexion_angle, color='red', label='Right Knee Flexion Angle')

# Plot MSwR events
for mswr_idx in mswr:
    plt.axvline(mswr_idx, color='green', linestyle='--', label='MSwR')
for mswl_idx in mswl:
    plt.axvline(mswl_idx, color='black', linestyle='--', label='MSwL')
for to_idx in to:
    plt.axvline(to_idx, color='purple', linestyle='--', label='TO')
for hs_idx in hs:
    plt.axvline(hs_idx, color='yellow', linestyle='--', label='HS')
for fa_idx in fa:
    plt.axvline(fa_idx, color='magenta', linestyle='--', label='FA')
for ho_idx in ho:
    plt.axvline(ho_idx, color='cyan', linestyle='--', label='HO')
for ot_idx in ot:
    plt.axvline(ot_idx, color='brown', linestyle='--', label='OT')
for oh_idx in oh:
    plt.axvline(oh_idx, color='gray', linestyle='--', label='OH')
plt.xlabel('Samples')
plt.ylabel('Value')
plt.legend(loc='upper right')
plt.show()

