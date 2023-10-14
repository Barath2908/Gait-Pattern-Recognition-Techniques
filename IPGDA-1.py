import pandas as pd
import matplotlib.pyplot as plt

# Read input Excel file
df = pd.read_excel('C:/Users/ibra5/Desktop/Internships/GAC/IGPDA-1/output_file.xlsx')

# Set threshold for Ax
Ax_threshold = -1.5 # m/s^2

# Initialize lists to store HO, TO, and HD indices
HO_indices = []
TO_indices = []
HD_indices = []

# Loop through every 60 samples
for i in range(60, len(df), 60):
    # Check for HO
    if df['Ax_filtered'][i] < (df['Ax_new'][i] - Ax_threshold) and df['Ax_new'][i] < df['Ax_filtered'][i-1]:
        HO_indices.append(i)

    # Check for TO
    elif df['Ax_filtered'][i] > (df['Ax_new'][i] + Ax_threshold):
        TO_indices.append(i)
    # Check for HD
    elif df['Ax_filtered'][i] < (df['Ax_new'][i] - Ax_threshold):
        HD_indices.append(i)

# Plot HO, TO, and HD for entire data
fig, ax = plt.subplots()
ax.plot(df.index, df['Ax_filtered'], 'k-', label='Ax_filtered')
ax.plot(df.index[HO_indices], df['Ax_filtered'][HO_indices], 'b.', label='HO')
ax.plot(df.index[TO_indices], df['Ax_filtered'][TO_indices], 'g.', label='TO')
ax.plot(df.index[HD_indices], df['Ax_filtered'][HD_indices], 'r.', label='HD')
ax.legend()
plt.show()
