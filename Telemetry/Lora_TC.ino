#include "I2Cdev.h"
#include "MPU6050.h"
#include "Wire.h"
#include <Wire.h>
#include <SPI.h>
#include <Adafruit_Sensor.h>
#include "Adafruit_BME680.h"
#include <SoftwareSerial.h>
#include <TinyGPS.h>
#include <LoRa.h>

#define SEALEVELPRESSURE_HPA (1013.25)
MPU6050 acc;
Adafruit_BME680 bme; // I2C

#define SLCK 13
#define MISO 12
#define MOSI 11
#define CS 10
#define RST 9
#define DI0 2

int ax, ay, az;
int gx, gy, gz;
float latitud, longitud;
int sat;
int year;
byte month, day, hour, minute, second, hundredths;
TinyGPS gps;
SoftwareSerial ss(4, 3); // pin 4(rx) y 3(tx)
int UVOUT = A0; // Output from the acc
int REF_3V3 = A1; // 3.3V power on the Arduino board

void setup() {
  Serial.begin(115200);
  pinMode(UVOUT, INPUT);
  pinMode(REF_3V3, INPUT);
  
  Wire.begin(); // Iniciando I2C  
  acc.initialize(); // Iniciando el sensor de aceleracion

  if (acc.testConnection()) Serial.println("MPU6050 iniciado correctamente");
  else Serial.println("Error al iniciar el MPU6050");
  while (!Serial);
  
  Serial.println(F("BME680 async test"));

  if (!bme.begin()) {
    Serial.println(F("Could not find a valid BME680 acc, check wiring!"));
    while (1);
  }

  // Set up oversampling and filter initialization for BME680
  bme.setTemperatureOversampling(BME680_OS_8X);
  bme.setHumidityOversampling(BME680_OS_2X);
  bme.setPressureOversampling(BME680_OS_4X);
  bme.setIIRFilterSize(BME680_FILTER_SIZE_3);
  bme.setGasHeater(320, 150); // 320*C for 150 ms

  // Iniciar LoRa
  LoRa.setPins(CS, RST, DI0); // Set LoRa pins
  if (!LoRa.begin(433E6)) { // or 915E6, the MHz speed of your module
    Serial.println("Starting LoRa failed!");
    while (1);
  }
}

void loop() {
  bool newData = false;
  unsigned long chars;
  unsigned short;
  int uvLevel = averageAnalogRead(UVOUT);
  
  int refLevel = averageAnalogRead(REF_3V3);
  float outputVoltage = 3.3 / refLevel * uvLevel;
  float uvIntensity = mapfloat(outputVoltage, 0.99, 2.9, 0.0, 15.0);

  // Leer las aceleraciones y velocidades angulares
  acc.getAcceleration(&ax, &ay, &az);
  acc.getRotation(&gx, &gy, &gz);
  
  // Tell BME680 to begin measurement.
  unsigned long endTime = bme.beginReading();
  if (endTime == 0) {
    Serial.println(F("Failed to begin reading :("));
    return;
  }

  delay(50); // This represents parallel work.

  // Obtain measurement results from BME680.
  if (!bme.endReading()) {
    Serial.println(F("Failed to complete reading :("));
    return;
  }

  // Durante un segundo analizamos los datos de GPS e informamos algunos valores clave
  // for (unsigned long start = millis(); millis() - start < 800;) {
  //   while (ss.available()) {
  //     char c = ss.read();
  //     if (gps.encode(c)) // ¿Ha entrado una nueva sentencia válida?
  //       newData = true;
  //   }
  // }

  // if (newData) {
  //   //latitud y longitud, numero de satelites disponibles    
  //   gps.f_get_position(&latitud, &longitud);
  //   sat = gps.satellites() == TinyGPS::GPS_INVALID_SATELLITES ? 0 : gps.satellites();
  // }

  // Imprimir valores de los sensores en el monitor serial
  Serial.print("Temperature: "); Serial.println(bme.temperature);
  Serial.print("Pressure: "); Serial.println(bme.pressure / 100.0);
  Serial.print("Humidity: "); Serial.println(bme.humidity);
  Serial.print("Altitude: "); Serial.println(bme.readAltitude(SEALEVELPRESSURE_HPA));
  Serial.print("ax: "); Serial.println(ax);
  Serial.print("ay: "); Serial.println(ay);
  Serial.print("az: "); Serial.println(az);
  Serial.print("gx: "); Serial.println(gx);
  Serial.print("gy: "); Serial.println(gy);
  Serial.print("gz: "); Serial.println(gz);
  Serial.print("UV Intensity: "); Serial.println(uvIntensity);
  Serial.println(); 

  // Enviar datos a través de LoRa
  LoRa.beginPacket();  
  LoRa.print(bme.temperature); LoRa.print(",");
  LoRa.print(bme.pressure / 100.0); LoRa.print(",");
  LoRa.print(bme.humidity); LoRa.print(",");
  LoRa.print(bme.readAltitude(SEALEVELPRESSURE_HPA)); LoRa.print(",");
  LoRa.print(ax); LoRa.print(",");
  LoRa.print(ay); LoRa.print(",");
  LoRa.print(az); LoRa.print(",");
  LoRa.print(gx); LoRa.print(",");
  LoRa.print(gy); LoRa.print(",");
  LoRa.print(gz); LoRa.print(",");
  LoRa.print(uvIntensity); LoRa.print("\n");
  // if (newData) {
  //   LoRa.print("LAT: "); LoRa.print(latitud == TinyGPS::GPS_INVALID_F_ANGLE ? 0.0 : latitud, 6); LoRa.print("\n");
  //   LoRa.print("LON: "); LoRa.print(longitud == TinyGPS::GPS_INVALID_F_ANGLE ? 0.0 : longitud, 6); LoRa.print("\n");
  //   LoRa.print("SAT: "); LoRa.print(sat); LoRa.print("\n");
  // }
  LoRa.endPacket();
}

int averageAnalogRead(int pinToRead) {
  byte numberOfReadings = 8;
  unsigned int runningValue = 0; 

  for(int x = 0 ; x < numberOfReadings ; x++)
    runningValue += analogRead(pinToRead);
  runningValue /= numberOfReadings;

  return(runningValue);  
}

float mapfloat(float x, float in_min, float in_max, float out_min, float out_max) {
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}
