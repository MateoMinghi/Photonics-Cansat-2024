from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, DataTable, DateFormatter, TableColumn
from bokeh.layouts import layout
from bokeh.plotting import figure
from datetime import datetime
from math import radians
import numpy as np


#figura 1
p1 = figure(x_axis_type="datetime", width=450, height=350)
source1 = ColumnDataSource(dict(x=[], y=[]))

#figura 2
p2 = figure(x_axis_type="datetime", width=450, height=350)
source2 = ColumnDataSource(dict(x=[], y=[]))

source3=ColumnDataSource(dict(x=[], y=[], z=[]))

#valores aleatoreos
def create_value():
    draw = np.random.randint(0,5, size=200)
    steps = np.where(draw>0,1,-1)
    walk = steps.cumsum()
    return walk[-1]

#líneas en la gráfica

p1.circle(x="x", y="y", color="red", line_color="red", source=source1)
p2.circle(x="x", y="y", color="red", line_color="red", source=source2)
p1.line(x="x", y="y", source=source1)
p2.line(x="x", y="y", source=source2)

#actualizar datos en la gráfica
def update():
    new_data = dict(x=[datetime.now()], y=[create_value()])
    new_data_table = dict(x=[create_value()], y=[create_value()], z=[create_value()])
    source1.stream(new_data, rollover=200)
    source2.stream(new_data, rollover=200)
    source3.stream(new_data_table, rollover=200)
    p1.title.text="Rayos UV" 
    p2.title.text="Altitud" 
    print(datetime.now())
    

#eje x
p1.xaxis.axis_label = "Tiempo"
p1.xaxis.major_label_orientation = radians(80)
p2.xaxis.axis_label = "Tiempo"
p2.xaxis.major_label_orientation = radians(80)

#eje y
p1.yaxis.axis_label = "Radiación UV"
p2.yaxis.axis_label = "Altitud"

columns = [
        TableColumn(field="x", title="x"),
        TableColumn(field="y", title="y"),
        TableColumn(field="y", title="z"),
    ]
data_table = DataTable(source=source3, columns=columns, width=400, height=280)

#layout
lay_out = layout([p1], [p2], [data_table])

#título
curdoc().title = "Panel Cansat"

#añadir layout al documento
curdoc().add_root(lay_out)

#periodic callback
curdoc().add_periodic_callback(update, 500)
