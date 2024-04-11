# Data Collection and CSV Update Script
#this doesn´t need to be a separate script, it can be inside the main document
import csv
import time
import random

csv_file = 'sensor_data.csv'

while True:
    # Simulate data collection from sensors
    sensor_data = {
        'time': time.time(),
        'sensor1': random.random(),
        'sensor2': random.random()
    }
    
    # Write data to CSV file
    with open(csv_file, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['time', 'sensor1', 'sensor2'])
        writer.writerow(sensor_data)
    
    # Wait for some time before collecting more data
    time.sleep(1)  # Collect data every 1 second
#this would be a separate script from the visualization one


#in the visualization file:

'''
def update_visualization():
    while True:
        # Read CSV file
        data = pd.read_csv(csv_file)
        
        # Create Panel plot
        plot_object = data.hvplot(x='time', y=['sensor1', 'sensor2'], title='Live Sensor Data')
        
        # Update Panel app
        app[:] = [plot_object]
        
        # Wait for some time before updating visualization
        time.sleep(5)  # Update visualization every 5 seconds
'''
