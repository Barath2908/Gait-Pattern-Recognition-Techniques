import pandas as pd
import numpy as np

# read data from the Excel file
data = pd.read_excel('input_file.xlsx', header=None)
Ax = data.iloc[:,0].values
Ay = data.iloc[:,1].values
Gz = data.iloc[:,2].values

# compute mean values
x = np.mean(Ax)
y = np.mean(Ay)
z = np.mean(Gz)

# create new columns
Ax_new = Ax - x
Ay_new = Ay - y
Gz_new = Gz - z

# apply low-pass filter
fs = 100 # sampling frequency, assuming 100 Hz
fc = 0.03 # cut-off frequency
alpha = 1/(1 + 2*np.pi*fc/fs) # filter coefficient
Ax_filtered = np.zeros_like(Ax_new)
Ay_filtered = np.zeros_like(Ay_new)
Gz_filtered = np.zeros_like(Gz_new)
Ax_filtered[0] = Ax_new[0]
Ay_filtered[0] = Ay_new[0]
Gz_filtered[0] = Gz_new[0]
for i in range(1, len(Ax_new)):
    Ax_filtered[i] = alpha*Ax_new[i] + (1-alpha)*Ax_filtered[i-1]
    Ay_filtered[i] = alpha*Ay_new[i] + (1-alpha)*Ay_filtered[i-1]
    Gz_filtered[i] = alpha*Gz_new[i] + (1-alpha)*Gz_filtered[i-1]

# write data to new Excel file
output_data = np.vstack((Ax_new, Ay_new, Gz_new, Ax_filtered, Ay_filtered, Gz_filtered)).T
df = pd.DataFrame(output_data, columns=['Ax_new', 'Ay_new', 'Gz_new', 'Ax_filtered', 'Ay_filtered', 'Gz_filtered'])
df.to_excel('output_file.xlsx', index=False)
