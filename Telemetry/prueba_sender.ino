#include <SPI.h>
#include <LoRa.h>

// Define the pins used by the LoRa module
// estos quizás se deban de cambiar, dependen del cableado
#define NSS 10  // Chip select pin
#define RST 9   // Reset pin
#define DIO0 2  // DIO0 pin

void setup() {
  Serial.begin(9600); //quizás se tengan que cambiar los baudios 
  while (!Serial);

  // Set the pins for the LoRa module
  LoRa.setPins(NSS, RST, DIO0);

  if (!LoRa.begin(433E6)) {
    Serial.println("Starting LoRa failed!");
    while (1);
  }
}

void loop() {
  // send packet
  LoRa.beginPacket();
  LoRa.print("Hello World");
  LoRa.endPacket();

  delay(1000);
}
