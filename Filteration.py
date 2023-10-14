import pandas as pd
from scipy.signal import butter, filtfilt

# Read the data from Excel file
df = pd.read_excel('G:/DRDO INTERNSHIP/Python Files/Gait_Det_Data.xlsx')

# Define the filter parameters
cutoff_freq = 100  # Cutoff frequency in Hz
fs = 1000  # Sampling frequency in Hz
order = 2  # Filter order

# Normalize the cutoff frequency
normalized_cutoff = cutoff_freq / (0.5 * fs)

# Create the Butterworth filter coefficients
b, a = butter(order, normalized_cutoff, btype='low', analog=False, output='ba')

# Apply the filter to the signals
gyro_signal_filtered = filtfilt(b, a, df['gyro_x'])
accel_signal_filtered = filtfilt(b, a, df['accel_z'])

# Update the DataFrame with the filtered signals
df['Filtered_Gyro_Signal'] = gyro_signal_filtered
df['Filtered_Accel_Signal'] = accel_signal_filtered

# Save the DataFrame with the filtered signals to a new Excel file
df.to_excel('G:/DRDO INTERNSHIP/Python Files/Filtered_Gait.xlsx', index=False)
