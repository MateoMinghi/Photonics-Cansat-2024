from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, DataTable, TableColumn, GMapOptions, Button,CustomJS, Div, Styles
from bokeh.layouts import layout
from bokeh.themes import Theme
from bokeh.plotting import figure, gmap
from math import radians, sin, cos, sqrt, atan2
from datetime import datetime
import random,serial

# Configuración de la conexión serial (ajusta el puerto según tu configuración)
arduino_port = "COM5"  # Reemplaza con tu puerto
baud_rate = 9600

# Necesitarás una clave API de Google Maps
google_api_key = "*******"

# Iniciar conexión serial con Arduino
try:
    ser = serial.Serial(arduino_port, baud_rate)
except Exception as e:
    print(f"Error connecting to Arduino: {e}")
    ser = None

# Clase de simulación del servomotor
class Servo:
    def _init_(self):
        self.active = False
        
    def toggle(self):
        self.active = not self.active
        print(f"Servo {'activated' if self.active else 'deactivated'}")
        if ser:
            if self.active:
                ser.write(b'H\n')  # Enviar comando 'H' para mover los servos a 90 grados
            else:
                ser.write(b'L\n')   # Enviar comando 'L' para mover los servos a 0 grados

# Crear instancia del servomotor
servo = Servo()

# URLs de las imágenes
image_off_url = "https://cdn.pixabay.com/photo/2013/07/12/18/40/button-153684_1280.png"  # URL de la imagen de estado desactivado
image_on_url = "https://cdn.pixabay.com/photo/2013/07/12/18/40/button-153682_1280.png"  # URL de la imagen de estado activado

# Función del callback del botón para cambiar la etiqueta según el estado del servo
def update_button_label():
    if servo.active:
        button.label = "Desactivar Servo"
    else:
        button.label = "Activar Servo"

# Crear el botón y agregar el JavaScript para cambiar la imagen
button = Button(label="Activar Servo", width=200, height=100)
div = Div(text=f'<img src="{image_off_url}" width="150" height="150">', width=200, height=100)

button_callback = CustomJS(args=dict(div=div, on_url=image_on_url, off_url=image_off_url), code="""
    if (div.tags.length === 0 || div.tags[0] === 'off') {
        div.tags = ['on'];
        div.text = <img src="${on_url}" width="150" height="150">;
    } else {
        div.tags = ['off'];
        div.text = <img src="${off_url}" width="150" height="150">;
    }
""")

# Función del callback del botón para cambiar el estado del servo y la etiqueta del botón
def toggle_servo():
    servo.toggle()
    update_button_label()

button.js_on_click(button_callback)
button.on_click(toggle_servo)


# Inicialización de las listas donde se guardan los valores de los sensores 
sensor_values = {i: [] for i in range(1, 13)}
timestamps = []

# Función para simular datos
def simulate_data():
    simulated_values = [random.uniform(20, 30) for _ in range(8)]  # Valores de sensores arbitrarios
    lat1, lon1 = random.uniform(20.611412, 20.615), random.uniform(-100.41, -100.40)  # Primer GPS
    lat2, lon2 = random.uniform(20.611412, 20.615), random.uniform(-100.41, -100.40)  # Segundo GPS
    simulated_values.extend([lat1, lon1, lat2, lon2])
    return simulated_values

# Leer y procesar los datos que arrojan los sensores
def process_data():
    try:
        sensorValues = simulate_data()
        for i in range(1, 13):
            sensor_values[i].append(sensorValues[i-1])
        timestamps.append(datetime.now())
    except Exception as e:
        print(f"Error processing data: {e}")

# Crear un mapa con los datos de GPS
map_options = GMapOptions(lat=20.613, lng=-100.405, map_type="roadmap", zoom=15)
p_map = gmap("AIzaSyBmEuJTZzc1DktZZIgOgbKNpMxQgWCEwi8", map_options, title="GPS Map", width=400, height=280)
source_map = ColumnDataSource(data=dict(x=[], y=[]))
p_map.circle(x="x", y="y", size=10, fill_color="red", fill_alpha=0.6, line_color="red", source=source_map)

# Función para calcular la distancia entre dos puntos GPS en kilómetros
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371.0  # Radio de la Tierra en kilómetros
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2)*2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)*2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance

# Crear las fuentes de datos para las tablas
source_table1 = ColumnDataSource(data=dict(x=[], y=[]))
source_table2 = ColumnDataSource(data=dict(x=[], y=[]))

# Definir las columnas para las tablas
columns1 = [
    TableColumn(field="x", title="GPS1 X"),
    TableColumn(field="y", title="GPS1 Y"),
]
columns2 = [
    TableColumn(field="x", title="GPS2 X"),
    TableColumn(field="y", title="GPS2 Y"),
]


# Crear las tablas
data_table1 = DataTable(source=source_table1, columns=columns1, width=400, height=280,index_position=-1)
data_table2 = DataTable(source=source_table2, columns=columns1, width=400, height=280,index_position=-1)


# Agregar el JavaScript para el autoscroll
data_table1.js_on_change("source", CustomJS(code="""
    console.log('Updating scroll position:...');
    setTimeout(function() {
        var scrollDiv = document.getElementsByClassName('slick-viewport')[0];
        scrollDiv.scrollTop = scrollDiv.scrollHeight;
    }, 500);
"""))

data_table2.js_on_change("source", CustomJS(code="""
    console.log('Updating scroll position:...');
    setTimeout(function() {
        var scrollDiv = document.getElementsByClassName('slick-viewport')[1];
        scrollDiv.scrollTop = scrollDiv.scrollHeight;
    }, 500);
"""))

# Actualizar los datos para hacer el "stream"
def update():
    process_data()
    
    if len(timestamps) > 0:
        new_data1 = dict(x=[timestamps[-1]], y=[sensor_values[1][-1]])
        new_data2 = dict(x=[timestamps[-1]], y=[sensor_values[2][-1]])
        new_data3 = dict(x=[timestamps[-1]], y=[sensor_values[3][-1]])
        new_data4 = dict(x=[timestamps[-1]], y=[sensor_values[4][-1]])
        new_data5 = dict(x=[timestamps[-1]], y=[sensor_values[7][-1]])
        new_data6 = dict(x=[timestamps[-1]], y=[sensor_values[6][-1]])
        new_data7 = dict(x=[sensor_values[4][-1]], y=[sensor_values[5][-1]], z=[sensor_values[6][-1]])
        new_data8 = dict(x=[sensor_values[8][-1]], y=[sensor_values[9][-1]], z=[sensor_values[10][-1]])
        
        # Datos del mapa
        lat1, lon1 = sensor_values[10][-1], sensor_values[11][-1]
        new_data_map = dict(x=[lat1], y=[lon1])

        source1.stream(new_data1, rollover=200)
        p1.title.text = "Temperatura"
        source2.stream(new_data2, rollover=200)
        p2.title.text = "Presión"
        source3.stream(new_data3, rollover=200)
        p3.title.text = "Humedad"
        source4.stream(new_data4, rollover=200)
        p4.title.text = "Altitud"
        source5.stream(new_data5, rollover=200)
        p5.title.text = "Aceleración"
        source6.stream(new_data6, rollover=200)
        p6.title.text = "UV"
        source7.stream(new_data7, rollover=200)
        source8.stream(new_data8, rollover=200)
        source_map.stream(new_data_map, rollover=200)
        
        # Datos para las tablas
        new_data_table1 = dict(x=[sensor_values[10][-1]], y=[sensor_values[11][-1]])
        new_data_table2 = dict(x=[sensor_values[8][-1]], y=[sensor_values[9][-1]])

        # Actualizar las fuentes de datos de las tablas
        source_table1.stream(new_data_table1, rollover=200)
        source_table2.stream(new_data_table2, rollover=200)

        print(datetime.now())

# Las líneas azules de la gráfica
p1 = figure(x_axis_type="datetime", width=450, height=350)
source1 = ColumnDataSource(data=dict(x=[], y=[]))
p1.line(x="x", y="y", source=source1)

p2 = figure(x_axis_type="datetime", width=450, height=350)
source2 = ColumnDataSource(data=dict(x=[], y=[]))
p2.line(x="x", y="y", source=source2)

p3 = figure(x_axis_type="datetime", width=450, height=350)
source3 = ColumnDataSource(data=dict(x=[], y=[]))
p3.line(x="x", y="y", source=source3)

p4 = figure(x_axis_type="datetime", width=450, height=350)
source4 = ColumnDataSource(data=dict(x=[], y=[]))
p4.line(x="x", y="y", source=source4)

p5 = figure(x_axis_type="datetime", width=450, height=350)
source5 = ColumnDataSource(data=dict(x=[], y=[]))
p5.line(x="x", y="y", source=source5)

p6 = figure(x_axis_type="datetime", width=450, height=350)
source6 = ColumnDataSource(data=dict(x=[], y=[]))
p6.line(x="x", y="y", source=source6)

source7 = ColumnDataSource(dict(x=[], y=[], z=[]))
source8 = ColumnDataSource(dict(x=[], y=[], z=[]))

# Labels de la gráfica
p1.xaxis.axis_label = "Time"
p1.xaxis.major_label_orientation = radians(80)
p2.xaxis.axis_label = "Time"
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

# Añadir las columnas faltantes
columns = [
    TableColumn(field="x", title="rotacionX"),
    TableColumn(field="y", title="rotacionY"),
    TableColumn(field="z", title="rotacionZ"),
]
data_table3 = DataTable(source=source7, columns=columns, width=400, height=280)

columns_2 = [
    TableColumn(field="x", title="aceleracionX"),
    TableColumn(field="y", title="aceleracionY"),
    TableColumn(field="z", title="aceleracionZ"),
]
data_table4 = DataTable(source=source8, columns=columns_2, width=400, height=280)



# Layout: Cómo están organizadas las gráficas y los componentes
lay_out = layout([
        [p1, p2, p3],
        [p4, p5, p6],
        [p_map, data_table1,data_table2],
        [data_table3, data_table4, button, div],
    ]) 

curdoc().theme = 'dark_minimal'

# Título del documento
curdoc().title = "Panel Cansat"

# Añadir el layout al documento
curdoc().add_root(lay_out)

# Callback periódico
curdoc().add_periodic_callback(update, 500)