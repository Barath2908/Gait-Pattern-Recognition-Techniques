import pandas as pd
import numpy as np
from scipy.signal import butter, filtfilt
import matplotlib.pyplot as plt

# Read gyroscope data from Excel sheet
df = pd.read_excel('Test_source.xlsx', sheet_name='Sheet1')
gyro_data = df['Shank angular velocity'].values

# Constants
sampling_frequency = 60  # Hz
cutoff_frequency = 10  # Hz

# Initialize variables
Time = 0
MSW = 0
IC = 0
TO = 0
Cnt = 0
Previous_minima = 0
Immediate_minima = 0
Wn_1 = 0
Dn_1 = 0

# Create time axis
time_axis = np.arange(len(gyro_data)) / sampling_frequency

# Main loop
for Wn in gyro_data:
    # Apply filter
    filtered_velocity = butterworth_lowpass_filter(Wn, sampling_frequency, cutoff_frequency)

    # Compute difference
    Dn = filtered_velocity - Wn_1

    # Check conditions
    if Time > Tgiven:
        break

    if Dn < 0 and Dn_1 > 0:
        if filtered_velocity > 100:
            MSW = 1
            IC = 0
            TO = 0
            if Time > 0:
                Wn_1 = Wn

    elif Dn > 0 and Dn_1 < 0:
        if MSW == 1 and filtered_velocity < 0:
            if any_maxima_in_window(Immediate_minima, Previous_minima, filtered_velocity, 80, 10):
                Immediate_minima = IC
            else:
                Previous_minima = IC
            IC = 1
            TO = 0
            Cnt = 0
            Wn_1 = Wn

    if IC == 1 and filtered_velocity < -20 and Cnt > 300:
        TO = 1
        IC = 0
        Wn_1 = Wn

    # Update variables
    Time += 1
    Cnt += 1
    Dn_1 = Dn


# Function to check if any maxima in a given window
def any_maxima_in_window(Immediate_minima, Previous_minima, sample, window_size, magnitude_diff):
    maxima_count = 0
    for i in range(len(sample) - window_size):
        window = sample[i:i + window_size]
        max_val = max(window)
        min_val = min(window)
        if max_val - min_val >= magnitude_diff:
            maxima_count += 1
    return maxima_count > 0


# Function to apply Butterworth lowpass filter
def butterworth_lowpass_filter(sample, fs, cutoff):
    nyquist_frequency = 0.5 * fs
    normal_cutoff = cutoff / nyquist_frequency
    b, a = butter(2, normal_cutoff, btype='low', analog=False)
    filtered_sample = filtfilt(b, a, sample)
    return filtered_sample


# Plot input data and detected events
plt.figure(figsize=(10, 6))
plt.plot(time_axis, gyro_data, label='Shank angular velocity')
plt.plot(time_axis, MSW * gyro_data, 'ro', label='Mid-Swing (MSW)')
plt.plot(time_axis, IC * gyro_data, 'gs', label='Initial Contact (IC)')
plt.plot(time_axis, TO * gyro_data, 'y^', label='Toe Off (TO)')
plt.xlabel('Time (seconds)')
plt.ylabel('Angular Velocity')
plt.title('Detection of Events in Gyroscope Data')
plt.legend()
plt.grid(True)
plt.show()