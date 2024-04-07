# Data Collection and CSV Update Script

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
