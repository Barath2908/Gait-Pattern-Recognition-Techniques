import pandas as pd
import matplotlib.pyplot as plt

def detect_toe_off(data):
    # Initialize variables
    Alast = 0
    Alast2 = 0
    iAlast = 0
    iAlast2 = 0
    iTO_list = []

    for i in range(0, len(data)-65, 66):
        cycle_data = data[i:i+66]  # Extract one gait cycle (66 samples)

        # Find local maximums
        local_max = cycle_data[(cycle_data.diff() > 0) & (cycle_data.diff().shift(-1) < 0)]

        if len(local_max) >= 2:
            Alast2 = Alast
            iAlast2 = iAlast
            if len(local_max) > 0:
                Alast = local_max.iloc[-1]
                iAlast = cycle_data[cycle_data == Alast].index[0]

                # Check condition for toe-off detection
                if (iAlast - iAlast2) > 10:
                    iTO = iAlast + 2
                else:
                    iTO = iAlast

                iTO_list.append(iTO)

    return iTO_list

# Read the Excel file
data_frame = pd.read_excel('C:/Users/ibra5/Desktop/Internships/GAC/Test_source.xlsx')

# Assuming the column containing shank angular velocity is named 'Shank Angular Velocity'
shank_angular_velocity = data_frame['Shank angular velocity']

# Detect toe-off
toe_off_values = detect_toe_off(shank_angular_velocity)

# Plotting
plt.plot(shank_angular_velocity)

# Draw vertical lines at toe-off positions
for iTO in toe_off_values:
    plt.axvline(x=iTO, color='r', linestyle='--')

plt.xlabel('Sample Index')
plt.ylabel('Shank Angular Velocity')
plt.title('Toe-Off Detection')
plt.show()
