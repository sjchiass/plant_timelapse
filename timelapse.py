import subprocess
from brightpi import *
import os

LEDS = (5, 8)

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

brightPi = BrightPi()

brightPi.reset()
brightPi.set_led_on_off(LEDS, ON)

subprocess.call("./timelapse.sh")

brightPi.set_led_on_off(LEDS, OFF)
brightPi.reset()
