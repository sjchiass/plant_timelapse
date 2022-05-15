import serial
from datetime import datetime

ser = serial.Serial("/dev/ttyACM0", timeout=30)

with open("/home/pi/plant_repo/sensor_data/data.csv", "a+") as f:
    f.write(datetime.now().isoformat())
    f.write(",")
    f.write(ser.readline().decode("utf-8"))
