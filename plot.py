import pandas as pd
import matplotlib.pyplot as plt

# Load data
data = pd.read_csv("sensor_data.csv")

# Print to verify
print(data.head())

# Plot
plt.figure()

plt.plot(data['temperature'], label='Temperature')
plt.plot(data['vibration'], label='Vibration')
plt.plot(data['load'], label='Load')

plt.xlabel("Time Steps")
plt.ylabel("Sensor Values")
plt.title("Sensor Data Monitoring")
plt.legend()

plt.show()
