import pandas as pd
import numpy as np
import panel as pn
import time

# Generate initial empty DataFrame
data = pd.DataFrame(columns=['Time', 'Sensor1', 'Sensor2'])

# Define a function to update data
def update_data():
    while True:
        # Simulate new data from sensors
        new_row = {'Time': time.time(), 'Sensor1': np.random.random(), 'Sensor2': np.random.random()}
        
        # Append new data to the DataFrame
        data.loc[len(data)] = new_row
        
        # Update the plot
        plot_object.data = data
        time.sleep(1)  # Update every 1 second

# Create a Panel plot
plot_object = data.hvplot(x='Time', y=['Sensor1', 'Sensor2'], title='Live Sensor Data')

# Create a Panel app
app = pn.Column(plot_object)

# Start updating the data
update_data_thread = Thread(target=update_data)
update_data_thread.start()

# Display the app
app.servable()
