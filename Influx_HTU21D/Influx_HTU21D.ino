// Load Wi-Fi library
#include <WiFi.h>

// Load InfluxDB client
#include <InfluxDbClient.h>

// Libraries for HTU21D
#include <Wire.h>
#include "SparkFunHTU21D.h"

//Create an instance of the object
HTU21D hum;

// Replace with your network credentials
const char* ssid = "";
const char* password = "";

// InfluxDB server url & db name
#define INFLUXDB_URL "http://192.168.0.80:8090"
#define INFLUXDB_DB_NAME "pizero-temp"

// Single InfluxDB instance
InfluxDBClient client(INFLUXDB_URL, INFLUXDB_DB_NAME);

void setup() {
  Serial.begin(115200);

  hum.begin();
  
  // Connect to Wi-Fi network with SSID and password
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  // Print local IP address and start web server
  Serial.println("");
  Serial.println("WiFi connected.");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void loop(){
  // Define data point with measurement name 'device_status`
  Point pointDevice("temp_event");

  float humd = hum.readHumidity();
  float temp = hum.readTemperature();
  float tempF = (temp * 9/5) + 32;

  // Set tags
  pointDevice.addTag("host", "esp32-office");
  
  // Add data
  pointDevice.addField("temperature", tempF);
  pointDevice.addField("humidity", humd);

  // Write point
  if (!client.writePoint(pointDevice)) {
    Serial.print("InfluxDB write failed: ");
    Serial.println(client.getLastErrorMessage());
  }

  // Sleep for 5 minutes before next reading
  Serial.println("Waiting 60 seconds");
  delay(60000);
}
