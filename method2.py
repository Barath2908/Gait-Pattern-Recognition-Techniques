import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Function to calculate composite acceleration
def calculate_composite_acceleration(acceleration_x, acceleration_y, acceleration_z):
    composite_acceleration = np.sqrt(acceleration_x ** 2 + acceleration_y ** 2 + acceleration_z ** 2)
    return composite_acceleration


# Function to detect gait events using IGDA algorithm
def detect_gait_events(composite_acceleration, cA200, cA50):
    ms_indices = []
    ps_indices = []
    sw_indices = []
    lr_indices = []

    # Constants for the conditions
    threshold = 1.2 * np.mean(composite_acceleration)
    quarter_cycle = int(len(composite_acceleration) / 4)

    # 'isMStance' condition
    for i in range(len(composite_acceleration)):
        if (composite_acceleration[i] < threshold and
                composite_acceleration[i] < cA50[i] and
                np.all(np.diff(cA50[i - quarter_cycle:i]) < -0.1 * cA50[i])):
            ms_indices.append(i)

    # Mid-stance (MS) to pre-swing (PS) transition
    for i in range(1, len(composite_acceleration)):
        if (composite_acceleration[i] > composite_acceleration[i - 1] and
                composite_acceleration[i] > cA50[i] and
                composite_acceleration[i] < cA200[i]):
            ps_indices.append(i)

    # Pre-swing (PS) to swing (SW) transition
    turning_points = []
    for i in range(1, len(composite_acceleration) - 1):
        if (composite_acceleration[i] > composite_acceleration[i - 1] and
                composite_acceleration[i] > composite_acceleration[i + 1]):
            turning_points.append(i)
    for i in turning_points:
        if composite_acceleration[i] > cA50[i]:
            sw_indices.append(i)

    # Swing (SW) to loading response (LR) transition
    for i in range(1, len(cA200) - 1):
        if (cA200[i] < cA200[i - 1] and
                cA200[i] < cA200[i + 1] and
                composite_acceleration[i] > cA200[i] and
                np.any(np.diff(composite_acceleration[i:]) > 0)):
            lr_indices.append(i)

    return ms_indices, ps_indices, sw_indices, lr_indices


# Load data from Excel file
data = pd.read_excel('C:/Users/ibra5/Desktop/Internships/GAC/Composite Accleration_WindowTime/acc.xlsx')
acceleration_x = data['acceleration_x'].values
acceleration_y = data['acceleration_y'].values
acceleration_z = data['acceleration_z'].values

# Calculate composite acceleration
composite_acceleration = calculate_composite_acceleration(acceleration_x, acceleration_y, acceleration_z)

# Calculate cA200 and cA50
cA200 = pd.Series(composite_acceleration).rolling(window=200).mean().values
cA50 = pd.Series(composite_acceleration).rolling(window=50).mean().values

# Detect gait events
ms_indices, ps_indices, sw_indices, lr_indices = detect_gait_events(composite_acceleration, cA200, cA50)

# Plotting the data
fig, ax = plt.subplots()

# Plot composite acceleration
ax.plot(composite_acceleration, color='black', label='Composite Acceleration')

# Plot gait events in different colors
if ms_indices:
    ax.scatter(ms_indices, composite_acceleration[ms_indices], color='blue', label='Mid-Stance')
if ps_indices:
    ax.scatter(ps_indices, composite_acceleration[ps_indices], color='red', label='Pre-Swing')
if sw_indices:
    ax.scatter(sw_indices, composite_acceleration[sw_indices], color='green', label='Swing')
if lr_indices:
    ax.scatter(lr_indices, composite_acceleration[lr_indices], color='orange', label='Loading Response')

# Set plot labels and legend
ax.set_xlabel('Time')
ax.set_ylabel('Composite Acceleration')
ax.legend()

# Display the plot
plt.show()

