import pandas as pd
import matplotlib.pyplot as plt

# load the input Excel file containing columns Gz_filtered and Gz_new
df = pd.read_excel('C:/Users/ibra5/Desktop/Internships/GAC/IGPDA-1/output_file.xlsx', usecols=['Gz_filtered', 'Gz_new'])

# set the Gz threshold for HO and HD
Gz_threshold = -0.015


# create empty lists to store HO, TO, and HD indices
ho_indices = []
to_indices = []
hd_indices = []

# loop through every 60 samples and detect HO, TO, and HD
for i in range(60, len(df), 60):
    # extract the Gz data for the current window
    gz_filtered_window = df['Gz_filtered'][i - 60:i].values
    gz_new_window = df['Gz_new'][i - 60:i].values

    # detect HO
    if gz_filtered_window.min() < (
            gz_new_window.min() - Gz_threshold) and gz_filtered_window.min() < gz_filtered_window[:-1].min():
        ho_indices.append(i - 60 + gz_filtered_window.argmin())

    # detect TO
    if gz_filtered_window.max() > gz_new_window.max():
        to_indices.append(i - 60 + gz_filtered_window.argmax())

    # detect HD
    if gz_filtered_window.min() < (gz_new_window.min() - Gz_threshold) and gz_filtered_window.max() > (
            gz_new_window.max() + Gz_threshold):
        hd_indices.append(i - 60 + gz_filtered_window.argmin())

# plot the entire data with HO in blue, TO in green, and HD in orange
plt.plot(df['Gz_filtered'], label='Gz_filtered')
plt.plot(ho_indices, df['Gz_filtered'][ho_indices], 'bo', label='HO')
plt.plot(to_indices, df['Gz_filtered'][to_indices], 'go', label='TO')
plt.plot(hd_indices, df['Gz_filtered'][hd_indices], 'yo', label='HD')
plt.legend()
plt.show()
