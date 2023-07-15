//Conexión del sensor de pH PH-4502C al Arduino:
//Conecta el pin VCC del sensor al pin 5V del Arduino.
//Conecta el pin GND del sensor al pin GND del Arduino.
//Conecta el pin de salida (OUT) del sensor al pin analógico A0 del Arduino.

#include <OneWire.h>
#include <DallasTemperature.h>

#include <SoftwareSerial.h>  // Incluimos la librería SoftwareSerial para leer el sensor de flujo de agua
SoftwareSerial flowSerial(10, 11);  // RX: pin 10, TX: pin 11

#define ONE_WIRE_BUS 2  // Conecta el pin de datos del sensor DS18B20 al pin 2 del Arduino

OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

int phSensorPin = A0; // Pin analógico al que está conectado el sensor de pH

void setup() {
  Serial.begin(9600);
  flowSerial.begin(9600);  // Inicializamos la comunicación con el sensor de flujo de agua
  sensors.begin();
}

void loop() {
  sensors.requestTemperatures();  // Realiza una lectura de temperatura

  float temperatureC = sensors.getTempCByIndex(0);  // Obtiene la temperatura en grados Celsius
  float temperatureF = sensors.getTempFByIndex(0);  // Obtiene la temperatura en grados Fahrenheit

  Serial.print("Temperatura (C): ");
  Serial.print(temperatureC);
  Serial.print("  Temperatura (F): ");
  Serial.println(temperatureF);

  if (flowSerial.available()) {  // Verificamos si hay datos disponibles del sensor de flujo de agua
    String flowData = flowSerial.readStringUntil('\n');  // Leemos la línea completa de datos
    float flowRate = flowData.toFloat();  // Convertimos los datos a un valor numérico

    Serial.print("Tasa de flujo de agua: ");
    Serial.print(flowRate);
    Serial.println(" L/min");
  }

  int phValue = analogRead(phSensorPin); // Leer el valor analógico del sensor de pH
  float voltage = phValue * (5.0 / 1023.0); // Convertir el valor a voltaje (0-5V)
  float pH = 3.5 * voltage; // Calcular el valor de pH según la curva de calibración

  Serial.print("Valor de pH: ");
  Serial.println(pH);

  delay(1000);  // Espera 1 segundo antes de la siguiente lectura
}
