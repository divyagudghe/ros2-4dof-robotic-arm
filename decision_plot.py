import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("sensor_data.csv")

# convert status to numeric
mapping = {'normal': 0, 'warning': 1, 'failure': 2}
data['state_num'] = data['status'].map(mapping)

plt.figure()

plt.plot(data['state_num'])

plt.yticks([0,1,2], ['RUNNING','WARNING','STOP'])
plt.xlabel("Time Steps")
plt.ylabel("System State")
plt.title("System Decision Over Time")

plt.show()
