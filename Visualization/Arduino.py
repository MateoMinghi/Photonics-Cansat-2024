import serial

Serial_port = 'COM3'
Baud_rate = 115200

ser = serial.Serial(Serial_port, Baud_rate)

x = []
sensorValue1 = []
sensorValue2 = []

def process_data():
    line = ser.readline().decode('utf-8').strip()
    sensorValues = line.split(', ')

    x.append(float(sensorValues[0]))
    sensorValue1.append(int(sensorValues[1]))
    sensorValue2.apped(int(sensorValues[2]))

    print(f'Tiempo:  {sensorValues[0]}, Sensor 1 : {sensorValues[1]}, Sensor 2: {sensorValues[2]}')
