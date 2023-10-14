import numpy as np
import matplotlib.pyplot as plt


# Preprocessing: Apply appropriate signal processing techniques to filter and preprocess the gyroscope, accelerometer, and angular velocity signals

# Assuming you have the preprocessed gyroscope, accelerometer, and angular velocity signals as numpy arrays: gyro_signal, accel_signal, and angvel_signal

def detect_gait_phases(gyro_signal, accel_signal, angvel_signal):
    # Initialize variables
    gait_phases = []

    # Locate Toe-Off (TO) and Initial Contact (IC)
    ic_index = np.argmin(gyro_signal)
    to_index = np.argmax(gyro_signal[:ic_index])

    # Set counter for FFS to 40 ms
    counter = int(0.04 * 1000)

    # Detect Footflat Start (FFS)
    ffs1_index = np.argmax(accel_signal[ic_index:ic_index + counter]) + ic_index
    ffs2_index = np.argmin(accel_signal[ic_index:ic_index + counter]) + ic_index

    if ffs1_index != ffs2_index:
        # Mark Footflat Start (FFS) event
        gait_phases.append(('Foot-flat', ffs1_index, ffs2_index))

        # Find the immediate local maxima after FFS2 in the angular velocity signal
        max_index = np.argmax(angvel_signal[ffs2_index:])
        msw_index = max_index + ffs2_index

        # Adjust counter based on magnitude of Mid-Swing (MSW)
        msw_magnitude = angvel_signal[msw_index]

        if msw_magnitude < 260:
            counter = int(0.09 * 1000)
        elif 260 < msw_magnitude < 320:
            counter = int(0.07 * 1000)
        else:
            counter = int(0.05 * 1000)

        # Mark Mid-Swing (MSW) event
        gait_phases.append(('Mid-Swing', msw_index))

        # Set counter for MST to 30 ms
        counter = int(0.03 * 1000)

        # Detect Heel-Off (HO)
        ho1_index = np.where(np.diff(np.sign(accel_signal[msw_index:msw_index + counter])))[0][0] + msw_index

        # Calculate difference between current and previous acceleration values
        accel_diff = np.abs(np.diff(accel_signal))

        if np.max(accel_diff) >= 0.1:
            ho2_index = np.argmax(accel_diff) + 1
            ho2_index = np.where(np.diff(np.sign(accel_signal[:ho2_index])))[0][0]
            gait_phases.append(('Push-off', ho1_index, ho2_index))
        else:
            gait_phases.append(('Push-off', ho1_index))

    return gait_phases


# Usage example
import pandas as pd

# Read the Excel sheet into a DataFrame
df = pd.read_excel("C:/Users/ibra5/Desktop/Internships/GAC/Joana Code/test_dummy.xlsx")

# Extract the required signals
gyro_signal = df['GyroscopeX']  # Replace 'gyro_x' with the actual column name for the gyroscope signal
accel_signal = df['Ax']  # Replace 'accel_z' with the actual column name for the accelerometer signal
angvel_signal = df['Angular_velocity_X']  # Replace 'angular_velocity_x' with the actual column name for the angular velocity signal

# Detect gait phases
result = detect_gait_phases(gyro_signal, accel_signal, angvel_signal)
print(result)

# Plot the signals with detected gait phases
plt.figure(figsize=(10, 6))
plt.plot(gyro_signal, label='Gyroscope Signal')
plt.plot(accel_signal, label='Accelerometer Signal')
plt.plot(angvel_signal, label='Angular Velocity Signal')

# Plot the detected gait phases
for phase in result:
    phase_name = phase[0]
    start_index = phase[1]
    if len(phase) == 3:
        end_index = phase[2]
        plt.scatter(start_index, gyro_signal[start_index], color='red', marker='o', label=f'{phase_name} Start')
        plt.scatter(end_index, gyro_signal[end_index], color='green', marker='o', label=f'{phase_name} End')
    else:
        plt.scatter(start_index, gyro_signal[start_index], color='red', marker='o', label=phase_name)

plt.legend()
plt.xlabel('Time')
plt.ylabel('Signal Value')
plt.title('Gait Phases with Detected Points')
plt.show()
