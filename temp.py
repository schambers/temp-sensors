import Adafruit_DHT
import time
import datetime
import yaml
from influxdb import InfluxDBClient

# This is the pin and library for a DHT22 temperature sensor
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4

# Read yaml config
file = open('config.yml', 'r')
cfg = yaml.load(file, Loader=yaml.FullLoader)

# Create the InfluxDB client loading config from secrethub
client = InfluxDBClient(host=cfg['influxdb']['host'], port=cfg['influxdb']['port'], database=cfg['influxdb']['database'])

while True:
    humidity, temp = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temp is not None:
        tempf = (temp * 9/5) + 32
        print("Temp={0:0.1f}F Temp={1:0.1f}C Humidity={2:0.1f}%".format(tempf, temp, humidity))

        # Create measurement json data
        json_body = [
            {
                "measurement": "temp_event",
                "tags": {
                    "host": "pizero-garage"
                },
                "time": datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
                "fields": {
                    "temperature": tempf,
                    "humidity": humidity
                }
            }
        ]

        # Send measurement to InfluxDB
        client.write_points(json_body)
    else:
        print("Sensor failure. Check wiring.");

    # Sleep for 60 seconds before sending the next measurement
    time.sleep(60);
