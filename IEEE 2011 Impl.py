import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt

def butter_lowpass(cutoff, fs, order=2):
    nyquist = 0.2 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=2):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = filtfilt(b, a, data)
    return y

def detect_gait_events(angular_velocity, fs=100, cutoff_f1=3, cutoff_f2=10, Df1=0.1, Df2=0.2):
    # Preprocessing: Filtering and differentiation
    xf1 = butter_lowpass_filter(angular_velocity, cutoff_f1, fs)
    xf2 = butter_lowpass_filter(angular_velocity, cutoff_f2, fs)
    af1 = np.gradient(xf1)

    # Variables initialization
    MS_event = False
    gait_events = []

    # Detection of MS points
    for i in range(1, len(xf1)-1):
        if not MS_event and xf1[i] > xf1[i-1] and xf1[i] > xf1[i+1] and af1[i] > 0:
            MSf1 = i
            MSf2 = np.argmax(xf2[MSf1 - int(Df1*fs):MSf1]) + MSf1 - int(Df1*fs)
            MSunf = np.argmax(angular_velocity[MSf2 - int(Df2*fs):MSf2]) + MSf2 - int(Df2*fs)
            MS_event = True
            gait_events.append((MSunf, "MS"))

    # Detection of EC points
    for MSf1, event_type in gait_events:
        ECf1 = np.argmin(xf1[MSf1::-1])
        ECf2 = np.argmin(xf2[ECf1 - int(Df1*fs):ECf1]) + ECf1 - int(Df1*fs)
        indices = range(ECf2 - int(Df2 * fs), ECf2)
        if indices and len(indices) > 0:
            ECunf = np.argmin(angular_velocity[indices]) + ECf2 - int(Df2 * fs)
        else:
            # Handle the case where the range is empty or invalid
            ECunf = 0  # or any other suitable value

        # Detection of IC points
        for i in range(1, len(xf1)-1):
            if MS_event and xf1[i] < xf1[i-1] and xf1[i] < xf1[i+1]:
                ICf1 = i
                if MSf2 < ICf1:
                    ICf2 = np.argmin(xf2[MSf2:ICf1]) + MSf2
                    ICunf = np.argmin(angular_velocity[ICf2:ICf1]) + ICf2
                    gait_events.append((ICunf, "IC"))
                    MS_event = False

    return gait_events

# Read data from Excel file
data = pd.read_excel('C:/Users/ibra5/Desktop/Internships/GAC/Test_source.xlsx')  # Replace 'data.xlsx' with your Excel file name
# Extract angular velocity data from the DataFrame
angular_velocity = data['Foot angular velocity'].values

# Set the sampling frequency (fs) and other parameters
fs = 75  # Replace with your sampling frequency
cutoff_f1 = 1.5
cutoff_f2 = 5
Df1 = 0.2
Df2 = 0.2

# Detect gait events
detected_events = detect_gait_events(angular_velocity, fs, cutoff_f1, cutoff_f2, Df1, Df2)

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(angular_velocity, label='Foot Angular Velocity')
plt.xlabel('Sample')
plt.ylabel('Foot Angular Velocity')
plt.title('Gait Event Detection')
plt.grid(True)

# Mark the detected events as vertical lines with different colors
colors = {'MS': 'red', 'EC': 'blue', 'IC': 'green'}
for event in detected_events:
    index = event[0]
    event_type = event[1]
    plt.axvline(x=index, color=colors[event_type], linestyle='--')

# Show the legend
plt.legend()

# Display the plot
plt.show()