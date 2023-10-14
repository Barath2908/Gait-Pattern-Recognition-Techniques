import pandas as pd
import matplotlib.pyplot as plt

# Read excel file
df = pd.read_excel('data.xlsx')

# Initialize variables
swing_start = []
swing_end = []
stance_start = []
stance_end = []
state = 'unknown'
t = 0

# Loop through data
for i in range(len(df)):
    ax = df.loc[i, 'ax']
    wz = df.loc[i, 'ωz']
    ths = df.loc[i, 'θs']

    # Check for swing phase
    if ax > 0.1 and wz < 0 and ths < 0.1:
        if state == 'stance':
            swing_start.append(i)
            state = 'swing'
            t = 0
    # Check for stance phase
    elif ax < 0.1 and wz < 0 and ths > 0.1:
        if state == 'swing':
            stance_start.append(i)
            state = 'stance'
            t = 0
        elif state == 'stance' and t > 0.2:
            stance_end.append(i)
            swing_start.append(i)
            state = 'swing'
            t = 0
    # Check for transition from stance to swing phase
    elif ax > 0.1 and wz < 0 and ths < 0.1 and t > 0.4:
        swing_start.append(i)
        state = 'swing'
        t = 0
    t += 1

# Check if last phase was swing or stance
if state == 'swing':
    swing_end.append(len(df) - 1)
else:
    stance_end.append(len(df) - 1)

# Plot graph with swing and stance phase boundaries
fig, ax = plt.subplots()
ax.plot(df['ax'], label='ax')
ax.plot(df['ωz'], label='ωz')
ax.plot(df['θs'], label='θs')
for start, end in zip(swing_start, swing_end):
    ax.axvspan(start, end, alpha=0.3, color='red')
for start, end in zip(stance_start, stance_end):
    ax.axvspan(start, end, alpha=0.3, color='green')
ax.legend()
plt.show()