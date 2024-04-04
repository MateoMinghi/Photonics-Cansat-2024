import pandas as pd
import numpy as np
import panel as pn
import time

# Simulate real-time data source
def generate_data():
    while True:
        yield pd.DataFrame({'x': [time.time()], 'y': [np.random.rand()]})
        time.sleep(1)  # Simulate data arriving every second

# Function to update the plot
def update_plot(data):
    plot.data = data

# Create initial empty plot
plot = pn.pane.Bokeh()

# Define periodic callback to update plot with new data
data_generator = generate_data()
def update():
    data = next(data_generator)
    update_plot(data)

# Create Panel app layout
layout = pn.Column(
    '# Real-Time Data Visualization',
    plot,
)

# Run the periodic update
pn.state.add_periodic_callback(update, period=1000)  # Update every 1000 milliseconds (1 second)

# Display the app
layout.servable()
