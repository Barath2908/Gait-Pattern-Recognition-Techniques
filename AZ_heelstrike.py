import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def detect_heel_strike(data):
    """
    Detects heel strikes in the shank angular velocity data using the algorithm provided in the question.

    Args:
        data (pandas.DataFrame): A pandas dataframe with a column named "Shank angular velocity".

    Returns:
        A list of indices where heel strikes are detected.
    """

    # Constants used in the algorithm
    A1_THRES = 0.2  # A1 threshold to detect heel strike
    E_THRESHOLD = 0.5  # E threshold to estimate missing heel strikes
    WINDOW_SIZE = 5  # Size of the window around zero crossings

    # Extract the shank angular velocity data from the dataframe
    angular_vel = data["Shank angular velocity"].values

    # Calculate the zero crossings of the angular velocity data
    zero_crossings = np.where(np.diff(np.sign(angular_vel)))[0]

    # Initialize the variables used in the algorithm
    heel_strikes = []
    e_counter = 0

    iAn = 0
    for i, zc in enumerate(zero_crossings[:-1]):

        # Check if there is a second positive zero crossing
        zc2 = zero_crossings[i+1]
        if zc2 - zc > WINDOW_SIZE:

            # Abnormal heel strike
            iHS = iAn
            e_counter += 1

        else:

            # Find the first local maximum before the negative zero crossing
            iAn = np.argmax(angular_vel[zc-WINDOW_SIZE:zc])
            if iAn < A1_THRES * np.max(angular_vel[zc-WINDOW_SIZE:zc]):
                A1 = angular_vel[zc-WINDOW_SIZE+iAn]
            else:
                iHS = iAn
                e_counter += 1
                continue

            # Check if the first local maximum is within A1±5 samples of the negative zero crossing
            if abs(zc - (zc-WINDOW_SIZE+iAn)) <= WINDOW_SIZE:

                # Normal heel strike
                iHS = iAn

            else:

                # Abnormal heel strike
                iHS = iAn
                e_counter += 1

        heel_strikes.append(iHS)

    # Estimate missing heel strikes if E counter is above the threshold
    if e_counter > E_THRESHOLD * len(heel_strikes):
        for i, hs in enumerate(heel_strikes[:-1]):
            if hs is None:
                imid = int(1.5 * zero_crossings[i] + zc2/2)
                heel_strikes[i] = imid

    # Return the indices of the detected heel strikes
    return [i for i in heel_strikes if i is not None]


# Read the data from the excel file into a pandas dataframe
data = pd.read_excel("C:/Users/ibra5/Desktop/Internships/GAC/Test_source.xlsx")

# Split the data into chunks of 60 samples
chunk_size = 60
num_chunks = len(data) // chunk_size
chunks = np.array_split(data, num_chunks)

# Process each chunk separately
heel_strikes = []
for chunk in chunks:
    chunk_heel_strikes = detect_heel_strike(chunk)
    heel_strikes.extend([i + chunk_size * j for i in chunk_heel_strikes for j in range(num_chunks)])

# Plot the shank angular velocity data
plt.plot(data["Shank angular velocity"])

# Plot vertical lines at the indices of the detected heel strikes
for i in range(len(heel_strikes)):
    if i < len(heel_strikes)-1:
        if heel_strikes[i+1] - heel_strikes[i] > 5:
            color = 'b'
        else:
            color = 'r'
    else:
        color = 'b'
    plt.axvline(x=heel_strikes[i], color=color)

# Show the plot
plt.show()
