import pandas as pd
import matplotlib.pyplot as plt

# Load data from the Excel file
df = pd.read_excel('C:/Users/ibra5/Desktop/Internships/GAC/AZ Method/Low passed.xlsx')

# Define parameters
k = 10
epsilon = 1


# Function to check if a given gait cycle has an abnormal toe strike
def has_abnormal_toe_strike(gait_cycle):
    # Extract relevant columns
    shank_angular_velocity = gait_cycle['Shank angular velocity']
    vertical_acceleration = gait_cycle['VerticalAcceleration']
    horizontal_acceleration = gait_cycle['HorizontalAcceleration']
    low_passed_velocity = gait_cycle['Low passed']

    # Calculate required values
    iz1 = shank_angular_velocity.iloc[0]
    ih = shank_angular_velocity.iloc[int(len(shank_angular_velocity) * 0.5)]
    A = shank_angular_velocity[(iz1 <= shank_angular_velocity) & (shank_angular_velocity <= ih)]

    # Check if there are enough values in A
    if len(A) < 7:
        return False

    A1, A2, A3 = A.nlargest(3)
    Mmin = shank_angular_velocity.min()
    Amin = low_passed_velocity.min()
    Amax = A.max()
    Amax2 = A.nlargest(2).iloc[1]
    Amax_bar = low_passed_velocity.max()
    Pmax = gait_cycle['Shank Angle'].max()
    P1 = gait_cycle['Shank Angle'].idxmax()
    V = vertical_acceleration[int(iz1):int(ih)]
    G = horizontal_acceleration[int(iz1):int(ih)]
    sign_sum = (V * V.shift(1) < 0).sum()

    # Check the conditions
    if len(A) >= 7 and A1 < A2 and A1 < A3 and A2 > A1 and A2 > A3 and A2 > 1.3 * A3 and \
       Mmin != A1 and Mmin != A2 and Mmin != A3 and abs(Amin) > abs(Amax) and \
       0.5 * Amax > Amax2 and Amax_bar / Amax < 0.4 and P1 != Pmax and sign_sum < 0:
        return True
    else:
        return False

# Iterate over gait cycles and detect normal toe strikes
normal_toe_strikes = []
for i in range(0, len(df), 66):
    gait_cycle = df.iloc[i:i + 66]
    if has_abnormal_toe_strike(gait_cycle):
        continue
    else:
        normal_toe_strikes.append(i)

# Plot shank angular velocity with vertical lines indicating normal toe strikes
plt.plot(df['Shank angular velocity'])
for i in normal_toe_strikes:
    plt.axvline(x=i, color='blue')
plt.xlabel('Sample')
plt.ylabel('Shank angular velocity')
plt.title('Detection of Normal Toe Strikes')
plt.show()
