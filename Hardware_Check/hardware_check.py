from datetime import date
from pushbullet import Pushbullet
from vcgencmd import Vcgencmd
import time
import os

#token
pb = Pushbullet("o.1WBLdaCPq6RO6Ax0LZV7yHAd3gguE5m7")
#set device
dev = pb.get_device("Samsung SM-A528B")

#hardware checks
vcgm = Vcgencmd()

#throttle
throttle_o = vcgm.get_throttled()
throttle = throttle_o.get("raw_data")

#temp
temp = vcgm.measure_temp()

#push when throttle OR temp > 77
if throttle == "0x50005" or throttle == "0x00005":
        push = dev.push_note("UNDERVOLT", "Raspi has recently undervolted!!!")
elif temp > 77.0:
        push = dev.push_note("THERMAL THROTTLING", f"The Pi is too hot, currently {temp}")
