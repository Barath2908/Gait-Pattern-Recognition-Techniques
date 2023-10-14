import pandas as pd
import matplotlib.pyplot as plt

# Load input Excel file
df = pd.read_excel('C:/Users/ibra5/Desktop/Internships/GAC/IGPDA-1/output_file.xlsx')

# Set thresholds
Ax_threshold = -1
Ay_threshold = -1

# Initialize HO, TO, and HD lists
HO = []
TO = []
HD = []

# Loop through every 60 samples
for i in range(66, len(df), 66):
    # Extract current 60 samples
    df_current = df.iloc[i-66:i]

    # Apply HO, TO, and HD algorithms
    HO_current = df_current[(df_current['Ax_filtered'] < (df_current['Ax_new'] - Ax_threshold)) &
                            (df_current['Ax_filtered'] < df_current['Ax_filtered'].shift(1)) &
                            (df_current['Ay_filtered'] > df_current['Ay_new'])]
    TO_current = df_current[(df_current['Ax_filtered'] > (df_current['Ax_new'] + Ax_threshold)) &
                            (df_current['Ay_filtered'] < (df_current['Ay_new'] - Ay_threshold))]
    HD_current = df_current[(df_current['Ax_filtered'] < (df_current['Ax_new'] - Ax_threshold)) &
                            (df_current['Ay_filtered'] > (df_current['Ay_new'] + Ay_threshold)) &
                            (df_current['Ax_filtered'] < df_current['Ax_filtered'].shift(1))]

    # Append HO, TO, and HD indices to their respective lists
    HO.extend(list(HO_current.index))
    TO.extend(list(TO_current.index))
    HD.extend(list(HD_current.index))

# Plot HO, TO, and HD
plt.plot(df.index, df['Ax_filtered'], label='Ax_filtered')
plt.plot(df.index, df['Ay_filtered'], label='Ay_filtered')
plt.plot(HO, df.loc[HO, 'Ax_filtered'], 'bo', label='HO')
plt.plot(TO, df.loc[TO, 'Ax_filtered'], 'go', label='TO')
plt.plot(HD, df.loc[HD, 'Ax_filtered'], 'yo', label='HD')
plt.legend()
plt.show()
