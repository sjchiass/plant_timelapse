import subprocess
from brightpi import *
import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

brightPi = BrightPi()

brightPi.reset()
brightPi.set_led_on_off(LED_ALL, ON)

subprocess.call("./timelapse.sh")

brightPi.set_led_on_off(LED_ALL, OFF)
brightPi.reset()

