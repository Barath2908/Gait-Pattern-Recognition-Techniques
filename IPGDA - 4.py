import pandas as pd
import matplotlib.pyplot as plt

# Load the input excel file into a pandas dataframe
df = pd.read_excel('C:/Users/ibra5/Desktop/Internships/GAC/IGPDA-1/output_file.xlsx')

# Set the threshold values
Ax_threshold = 1.5  # m/s^2
Ay_threshold = 1.75  # m/s^2
Gz_threshold = 0.75  # rad/s

# Initialize the lists to store the indices of HO, TO, and HD
HO_idx = []
TO_idx = []
HD_idx = []

# Loop through the data in increments of 60 samples (i.e., every i = 60)
for i in range(60, len(df), 60):

    # Check for HO
    if (df['Ax_filtered'][i] < (df['Ax_new'][i] - Ax_threshold) and
            df['Ax_filtered'][i] < df['Ax_filtered'][i - 1] and
            df['Gz_filtered'][i] < df['Gz_filtered'][i - 1] and
            df['Gz_filtered'][i] < df['Gz_new'][i]):

        HO_idx.append(i)

    # Check for TO
    elif df['Gz_filtered'][i] > df['Gz_new'][i]:
        TO_idx.append(i)

    # Check for HD
    elif (df['Ax_filtered'][i] < (df['Ax_new'][i] - Ax_threshold) and
          df['Ay_filtered'][i] > df['Ay_new'][i] and
          df['Gz_filtered'][i] < df['Gz_new'][i]):

        HD_idx.append(i)

# Plot the entire dataset with HO in blue, TO in green, and HD in orange
fig, ax = plt.subplots()
ax.plot(df.index, df['Ax_filtered'], label='Ax_filtered')
ax.plot(df.index, df['Ay_filtered'], label='Ay_filtered')
ax.plot(df.index, df['Gz_filtered'], label='Gz_filtered')
ax.scatter(HO_idx, df['Gz_filtered'][HO_idx], color='blue', label='HO')
ax.scatter(TO_idx, df['Gz_filtered'][TO_idx], color='green', label='TO')
ax.scatter(HD_idx, df['Gz_filtered'][HD_idx], color='orange', label='HD')
ax.legend()
plt.show()
