# pizero-temp
Pi Zero W Temperature/Humidity sensor script

Sample script from playing with a Pi Zero W and a DHT22 temperature sensor
* [Pi Zero W](https://www.raspberrypi.org/products/raspberry-pi-zero-w/)
* [DHT22 Temperature Sensor](https://www.adafruit.com/product/385)

Python requirements include:
* `pip install Adafruit_DHR`
* `pip install influxdb`
* `pip install --no-cache-dir --no-binary pyyaml pyyaml`

Create a config.yaml in the root of your project that contains the following settings:
```
influxdb:
    host: influxdb_host_or_ip
    port: influxdb_port
    database: influxdb_database
```

I'm sure there's an easier way to document python package requirements but the requirements are minimal here
I assumed it'd be easier to just list the two required packages.

Sends metrics to InfluxDB, once every 60 seconds in the form of the following document:
```
[{
    "measurement": "temp_event",
    "tags": {
        "host": "pizero-garage"
    },
    "time": "2021-08-30T01:00:00Z",
    "fields": {
        "temperature": 75.4,
        "humidity": 41
    }
}]
```