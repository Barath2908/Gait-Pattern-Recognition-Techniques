import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the data from Excel file
filename = 'data.xlsx'
sheet = 'Sheet1'  # Assuming data is on the first sheet
range = 'A2:B1000'  # Assuming the data is in columns A and B (excluding headers)

# Read the data from Excel file
data = pd.read_excel(filename, sheet_name=sheet, usecols=range, header=None)
gyro_signal = data[0].values
timestamps = data[1].values

# Filter cutoff frequency
cutoff_frequency = 10  # Hz

# Algorithm parameters
threshold_msw_slope = 0
threshold_msw_velocity = 100  # degrees/sec
window_size = 80  # ms
maxima_difference = 10  # degrees/sec
to_counter = 300  # ms
threshold_to_velocity = -20  # degrees/sec

# Filter implementation (Butterworth low-pass filter)
from scipy.signal import butter, filtfilt

def butter_lowpass(cutoff, fs, order=2):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=2):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = filtfilt(b, a, data)
    return y

# Apply the low-pass filter
filtered_signal = butter_lowpass_filter(gyro_signal, cutoff_frequency, fs=100, order=2)

# Algorithm implementation
gait_events = []
ic_candidate = None

for i in range(1, len(filtered_signal)):
    # Mid-Swing (MSW) detection
    if filtered_signal[i] > threshold_msw_slope and filtered_signal[i] > threshold_msw_velocity:
        # Initial Contact (IC) detection
        if ic_candidate is None:
            ic_candidate = i
        else:
            # Check for maxima closer to the already detected minima
            if max(filtered_signal[ic_candidate:i]) - filtered_signal[i] <= maxima_difference:
                ic_candidate = i
            else:
                gait_events.append(('IC', timestamps[ic_candidate]))
                ic_candidate = None

    # Toe-Off (TO) detection
    if ic_candidate is not None and (timestamps[i] - timestamps[ic_candidate]) >= to_counter and filtered_signal[i] < threshold_to_velocity:
        gait_events.append(('TO', timestamps[i]))
        ic_candidate = None

# Plotting the data and marking gait events
plt.figure(figsize=(12, 6))
plt.plot(timestamps, gyro_signal, label='Gyroscope Signal')
plt.plot(timestamps, filtered_signal, label='Filtered Signal')
for event, timestamp in gait_events:
    plt.axvline(x=timestamp, color='red', linestyle='--', label=f'{event} Event')
plt.xlabel('Timestamp')
plt.ylabel('Signal')
plt.title('Gyroscope Signal and Detected Gait Events')
plt.legend()
plt.show()