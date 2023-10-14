import pandas as pd
import numpy as np

def detect_gait_phases(segment_positions, segment_accelerations, knee_angles, segment_velocities):
    # Define thresholds for each gait phase
    knee_flexion_threshold = 30  # Adjust as needed
    mid_swing_threshold = 10  # Adjust as needed
    knee_extension_threshold = -10  # Adjust as needed
    heel_strike_threshold = 0.5  # Adjust as needed
    midstance_threshold = 0.2  # Adjust as needed
    toe_off_threshold = -0.2  # Adjust as needed

    # Initialize an empty list to store the detected gait phases
    gait_phases = []

    # Iterate through each gait cycle
    for i in range(len(segment_positions)):
        # Extract relevant parameters for the current gait cycle
        segment_position = segment_positions[i]
        segment_acceleration = segment_accelerations[i]
        knee_angle = knee_angles[i]
        segment_velocity = segment_velocities[i]

        # Detect gait phases based on the provided criteria
        if knee_angle > knee_flexion_threshold:
            gait_phases.append("Knee Flexion")
        elif segment_velocity < mid_swing_threshold:
            gait_phases.append("Mid Swing")
        elif knee_angle < knee_extension_threshold:
            gait_phases.append("Knee Extension")
        elif segment_acceleration[1] < heel_strike_threshold:
            gait_phases.append("Heel Strike")
        elif abs(segment_velocity[2]) < midstance_threshold:
            gait_phases.append("Midstance")
        elif segment_acceleration[2] < toe_off_threshold:
            gait_phases.append("Toe-Off")

    return gait_phases

# Read data from Excel sheet
data = pd.read_excel("C:/Users/ibra5/Desktop/Internships/GAC/Joana Code/test_dummy.xlsx")

# Extract X, Y, Z values from the Excel columns
segment_positions = data[['X', 'Y', 'Z']].to_numpy()
segment_accelerations = data[['Acc_X', 'Acc_Y', 'Acc_Z']].to_numpy()
knee_angles = data['Knee Angle'].to_numpy()
segment_velocities = data[['Vel_X', 'Vel_Y', 'Vel_Z']].to_numpy()

# Example usage
detected_phases = detect_gait_phases(segment_positions, segment_accelerations, knee_angles, segment_velocities)
print(detected_phases)