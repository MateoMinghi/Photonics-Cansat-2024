from bokeh.io import curdoc
from bokeh.models import ColumnDataSource
from bokeh.layouts import layout
from bokeh.plotting import figure
from datetime import datetime
from math import radians
import numpy as np


# Create the first figure and data source
p1 = figure(x_axis_type="datetime", width=450, height=350)
source1 = ColumnDataSource(dict(x=[], y=[]))

# Create the second figure and data source
p2 = figure(x_axis_type="datetime", width=450, height=350)
source2 = ColumnDataSource(dict(x=[], y=[]))

# Function to create a random value
def create_value():
    draw = np.random.randint(0,5, size=200)
    steps = np.where(draw>0,1,-1)
    walk = steps.cumsum()
    return walk[-1]

# Plot circles and lines for both graphs
p1.line(x="x", y="y", source=source1)

p2.line(x="x", y="y", source=source2)

# Update function to stream data to both graphs
def update():
    new_data = dict(x=[datetime.now()], y=[create_value()])
    source1.stream(new_data, rollover=200)
    source2.stream(new_data, rollover=200)
    p1.title.text="Rayos UV" 
    p2.title.text="Altitud" 
    


# Update function for Select widget
def update_intermed(attrname, old, new):
    source1.data=dict(x=[], y=[])
    source2.data=dict(x=[], y=[])
    update()

# Define date patterns

# Set x-axis label and orientation
p1.xaxis.axis_label = "Tiempo"
p1.xaxis.major_label_orientation = radians(80)
p2.xaxis.axis_label = "Tiempo"
p2.xaxis.major_label_orientation = radians(80)

# Set y-axis label
p1.yaxis.axis_label = "Radiación UV"
p2.yaxis.axis_label = "Altitud"

# Define Select widget options

# Define layout
lay_out = layout([p1], [p2])

# Set document title
curdoc().title = "Panel Cansat"

# Add layout to document root
curdoc().add_root(lay_out)

# Add periodic callback to update function
curdoc().add_periodic_callback(update, 500)
