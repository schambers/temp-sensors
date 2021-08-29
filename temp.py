import Adafruit_DHT
import time

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4

while True:
    humidity, temp = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temp is not None:
        tempf = (temp * 9/5) + 32
        print("Temp={0:0.1f}F Temp={1:0.1f}C Humidity={2:0.1f}%".format(tempf, temp, humidity))
    else:
        print("Sensor failure. Check wiring.");
    time.sleep(5);
