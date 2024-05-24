from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, DataTable, DateFormatter, TableColumn
from bokeh.layouts import layout
from bokeh.plotting import figure
from math import radians
import serial
from datetime import datetime

#Port configuration
Serial_port = 'COM3'
Baud_rate = 115200
ser = serial.Serial(Serial_port, Baud_rate)

#Lists where data is stored 
sensorValue1 = []
sensorValue2 = []
sensorValue3 = []
sensorValue4 = []
sensorValue5 = []
sensorValue6 = []
sensorValue7 = []
sensorValue8 = []
sensorValue9 = []
sensorValue10 = []
sensorValue11 = []
timestamps = []

#Read and process data
def process_data():
    try:
        line = ser.readline().decode('utf-8').strip()
        print(f"Raw line: {line}")
        sensorValues = line.split(',')
        if len(sensorValues) == 11:
            sensorValue1.append(float(sensorValues[0]))
            sensorValue2.append(float(sensorValues[1]))
            sensorValue3.append(float(sensorValues[2]))
            sensorValue4.append(float(sensorValues[3]))
            sensorValue5.append(float(sensorValues[4]))
            sensorValue6.append(float(sensorValues[5]))
            sensorValue7.append(float(sensorValues[6]))
            sensorValue8.append(float(sensorValues[7]))
            sensorValue9.append(float(sensorValues[8]))
            sensorValue10.append(float(sensorValues[9]))
            sensorValue11.append(float(sensorValues[10]))

            timestamps.append(datetime.now())
        else:
            print(f"Unexpected data format: {line}")
    except Exception as e:
        print(f"Error processing data: {e}")
 
p1 = figure(x_axis_type="datetime", width=450, height=350)
source1 = ColumnDataSource(data=dict(x=[], y=[]))

p2 = figure(x_axis_type="datetime", width=450, height=350)
source2 = ColumnDataSource(data=dict(x=[], y=[]))

p3 = figure(x_axis_type="datetime", width=450, height=350)
source3 = ColumnDataSource(data=dict(x=[], y=[]))

p4 = figure(x_axis_type="datetime", width=450, height=350)
source4 = ColumnDataSource(data=dict(x=[], y=[]))

p5 = figure(x_axis_type="datetime", width=450, height=350)
source5 = ColumnDataSource(data=dict(x=[], y=[]))

p6 = figure(x_axis_type="datetime", width=450, height=350)
source6 = ColumnDataSource(data=dict(x=[], y=[]))

source7 = ColumnDataSource(dict(x=[], y=[], z=[]))
source8 = ColumnDataSource(dict(x=[], y=[], z=[]))


#update data for the stream
def update():
    process_data()
    new_data1 = dict(x=[timestamps[-1]], y=[sensorValue1[-1]])
    new_data2 = dict(x=[sensorValue4[-1]], y=[sensorValue2[-1]])

    new_data3 = dict(x=[timestamps[-1]], y=[sensorValue3[-1]])
    new_data4 = dict(x=[timestamps[-1]], y=[sensorValue4[-1]])

    new_data5 = dict(x=[timestamps[-1]], y=[sensorValue7[-1]])
    new_data6 = dict(x=[timestamps[-1]], y=[sensorValue11[-1]])

    new_data7 = dict(x=[sensorValue5[-1]], y=[sensorValue6[-1]], z=[sensorValue7[-1]])
    new_data8 = dict(x=[sensorValue8[-1]], y=[sensorValue9[-1]], z=[sensorValue10[-1]])
    
    source1.stream(new_data1, rollover=200)
    source2.stream(new_data2, rollover=200)
    source3.stream(new_data3, rollover=200)
    source4.stream(new_data4, rollover=200)
    source5.stream(new_data5, rollover=200)
    source6.stream(new_data6, rollover=200)
    source7.stream(new_data7, rollover=200)
    source8.stream(new_data8, rollover=200)

    print(datetime.now())

#lines in the plot
p1.line(x="x", y="y", source=source1)
p2.line(x="x", y="y", source=source2)
p3.line(x="x", y="y", source=source3)
p4.line(x="x", y="y", source=source4)
p5.line(x="x", y="y", source=source5)
p6.line(x="x", y="y", source=source6)



#labels
p1.xaxis.axis_label = "Time"
p1.xaxis.major_label_orientation = radians(80)
p2.xaxis.axis_label = "Presión"
p2.xaxis.major_label_orientation = radians(80)

p3.xaxis.axis_label = "Time"
p3.xaxis.major_label_orientation = radians(80)
p4.xaxis.axis_label = "Time"
p4.xaxis.major_label_orientation = radians(80)

p5.xaxis.axis_label = "Time"
p5.xaxis.major_label_orientation = radians(80)
p6.xaxis.axis_label = "Time"
p6.xaxis.major_label_orientation = radians(80)

p1.yaxis.axis_label = "Temperatura"
p2.yaxis.axis_label = "Presión"
p3.yaxis.axis_label = "Humedad"
p4.yaxis.axis_label = "Altitud"
p5.yaxis.axis_label = "Aceleración"
p6.yaxis.axis_label = "UV"





#tables
columns = [
        TableColumn(field="x", title="aceleraciónX"),
        TableColumn(field="y", title="aceleraciónY"),
        TableColumn(field="z", title="aceleraciónZ"),
    ]
data_table = DataTable(source=source7, columns=columns, width=400, height=280)

columns_2 = [
        TableColumn(field="x", title="rotacionX"),
        TableColumn(field="y", title="rotacionY"),
        TableColumn(field="z", title="rotacionZ"),
]
data_table2 = DataTable(source=source8, columns=columns_2, width=400, height=280)

#layout of the interphase
lay_out = layout([[p1], [p2], [p3]],
                [[p4], [p5], [p6]],
                [[data_table], [data_table2]])



curdoc().title = "Panel Cansat"

curdoc().add_root(lay_out)

curdoc().add_periodic_callback(update, 500)
