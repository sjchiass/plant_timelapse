import serial
from datetime import datetime

ser = serial.Serial("/dev/ttyACM0", timeout=30)

with open("/home/pi/plant_repo/sensor_data/data.csv", "a+") as f:
    out = datetime.now().isoformat()
    out += ","
    out += ser.readline().decode("utf-8")
    if len(out) != 46:
        print(f"ERROR: output not the expected length ({len(out)} vs. 46)")
        print(f"OUTPUT: {out}")
    elif out[-1] == "\r\n":
        print(f"ERROR: output does not end with newline")
        print(f"OUTPUT: {out}")
    else:
        f.write(out)
        
