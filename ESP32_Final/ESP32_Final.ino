#include <Wire.h>
#include "SparkFun_SCD30_Arduino_Library.h"
#include <DHT.h>
#include <WiFi.h>
#include <HTTPClient.h>


// ------------------- Configuración Sala -------------------
#define DEVICE_NAME "Nombre Sala"  

// ------------------- Configuración DHT11 -------------------
#define DHTTYPE DHT11
const int DHTPin = 15;
DHT dht(DHTPin, DHTTYPE);

// ------------------- Pines sensores -------------------
#define RXD2 16
#define TXD2 17
const int ldrPin = 35;
const int coPin = 32;

// ------------------- SCD30 (CO2) -------------------
SCD30 scd30;

// ------------------- WiFi -------------------
#define WIFI_SSID "RED WIFI"
#define WIFI_PASSWORD "CONTRASEÑA"

// ------------------- InfluxDB -------------------
#define INFLUXDB_URL "URL_INFLUXDB"
#define INFLUXDB_ORG "ID_ORGANIZACIÓN" 
#define INFLUXDB_BUCKET "NOMBRE_BUCKET" //El bucket no puede tener el mismo nombre que la organizacion
#define INFLUXDB_TOKEN "TOKEN"


// ------------------- Variables -------------------
unsigned int pm1 = 0, pm2_5 = 0, pm10 = 0;
int valorLDR = 0;
int valorCO = 0;
int valorCO2 = 0;

unsigned long lastSendTime = 0;
const unsigned long sendInterval = 15000; // 15 s

// ------------------- Setup -------------------
void setup() {
  Serial.begin(115200);
  Serial2.begin(9600, SERIAL_8N1, RXD2, TXD2); // Sensor de partículas
  dht.begin();

  // Inicializar I2C para SCD30
  Wire.begin(18, 19); // SDA, SCL
  Wire.setClock(100000);

  Serial.println("Iniciando SCD30...");
  if (!scd30.begin()) {
    Serial.println("Error: No se detectó SCD30");
  } else {
    Serial.println("SCD30 iniciado correctamente");
    delay(2000);
  }

  // Conectar WiFi
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Conectando a WiFi...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConectado a WiFi!");
}

// ------------------- Loop -------------------
void loop() {
  unsigned long currentMillis = millis();

  // Leer datos cada 15 segundos
  if (currentMillis - lastSendTime >= sendInterval) {
    lastSendTime = currentMillis;

    // -------- Lectura DHT11 --------
    float h = dht.readHumidity();
    float t = dht.readTemperature();
    if (isnan(h) || isnan(t)) { h = 0; t = 0; }

    // -------- Lectura PM --------
    leerDatosPM();

    // -------- Lectura LDR --------
    valorLDR = analogRead(ldrPin);

    // -------- Lectura CO --------
    valorCO = analogRead(coPin);

    // -------- Lectura CO2 --------
    if (scd30.dataAvailable()) {
      valorCO2 = (int) scd30.getCO2();
    }

    // -------- Mostrar datos en consola --------
    Serial.println("====== DATOS ======");
    Serial.printf("Temp: %.1f C, Hum: %.0f%%\n", t, h);
    Serial.printf("PM1: %u, PM2.5: %u, PM10: %u\n", pm1, pm2_5, pm10);
    Serial.printf("Luz: %u, CO: %u, CO2: %u\n", valorLDR, valorCO, valorCO2);
    Serial.println("==================");

    // -------- Enviar a InfluxDB --------
    enviarDatosAInflux(t, h, pm1, pm2_5, pm10, valorLDR, valorCO, valorCO2);
  }
}

// ------------------- Funciones -------------------
void leerDatosPM() {
  int index = 0;
  uint8_t value, previousValue;

  while (Serial2.available()) {
    value = Serial2.read();

    if ((index == 0 && value != 0x42) || (index == 1 && value != 0x4D)) { index = 0; continue; }

    if (index == 4 || index == 6 || index == 8) previousValue = value;
    else if (index == 5) pm1 = 256 * previousValue + value;
    else if (index == 7) pm2_5 = 256 * previousValue + value;
    else if (index == 9) pm10 = 256 * previousValue + value;
    else if (index > 15) break;

    index++;
  }

  while (Serial2.available()) Serial2.read();
}

void enviarDatosAInflux(float temperatura, float humedad, int pm1, int pm2_5, int pm10, int luz, int co, int co2) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    String url = String(INFLUXDB_URL) + "/api/v2/write?org=" + INFLUXDB_ORG + "&bucket=" + INFLUXDB_BUCKET + "&precision=s";

    http.begin(url);
    http.addHeader("Authorization", String("Token ") + INFLUXDB_TOKEN);
    http.addHeader("Content-Type", "text/plain");

    String data = String("ambiente,device=") + DEVICE_NAME +
                  " temperatura=" + String(temperatura,1) +
                  ",humedad=" + String(humedad,0) +
                  ",pm1=" + String(pm1) +
                  ",pm2_5=" + String(pm2_5) +
                  ",pm10=" + String(pm10) +
                  ",luz=" + String(luz) +
                  ",co=" + String(co) +
                  ",co2=" + String(co2);

    int httpResponseCode = http.POST(data);

    if (httpResponseCode > 0) {
      Serial.print("Datos enviados a InfluxDB. Código: "); Serial.println(httpResponseCode);
    } else {
      Serial.print("Error al enviar a InfluxDB. Código: "); Serial.println(httpResponseCode);
    }

    http.end();
  } else {
    Serial.println("WiFi no conectado. No se enviaron datos.");
  }
}
