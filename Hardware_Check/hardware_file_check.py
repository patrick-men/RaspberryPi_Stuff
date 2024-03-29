from datetime import date
from pushbullet import Pushbullet
from vcgencmd import Vcgencmd
import time
import csv
import urllib.request
import os


file_path = "/home/pi/pushnotif/data_read.csv"


#checks if there is an internet connection, and only start the actual script once there is
#prevents the attempt to send push notifs that go nowhere due to lack of internet connection
def check_internet():
    while True:
        try:
            urllib.request.urlopen('http://www.google.com', timeout=1)
            return True
        except urllib.request.URLError:
            pass
        time.sleep(1)


# Wait for an active internet connection before running the script
while not check_internet():
    time.sleep(1)


#token
pb = Pushbullet("o.1WBLdaCPq6RO6Ax0LZV7yHAd3gguE5m7")
#set device
dev = pb.get_device("Samsung SM-A528B")

#hardware checks
vcgm = Vcgencmd()

#startup-message
push = dev.push_note("Reboot:", "The Pi has just been rebooted")


#in this loop, the file is read and overwritten
#this way, the file will automatically be "renewed" every minute
#upon reading the file, it will be written for a minute, before it's overwritten again
while True:

    #open the file in write mode with a context manager that automatically closes when done
    with open(file_path, 'w', newline="") as f:

        writer = csv.writer(f)
        
        
        #repeat 39 times, i.e. for a minute
        #with leeway in case something slows down/unknown runtime of reading and pushing notif
        for i in range(38):
                #throttle
                throttle_o = vcgm.get_throttled()
                throttle = throttle_o.get("raw_data")

                #temp
                temp = vcgm.measure_temp()

                #write to file
                writer.writerow([temp, throttle])

                #sleep 1.5s, i.e ~40 scans per minute
                time.sleep(1.5)

        time.sleep(1)


    #open the file in read mode with a context manager that automatically closes when done
    with open(file_path, 'r', newline="") as f:

        reader = csv.reader(f)

        #check for critical values, and push if found
        for row in reader:
            temp_value = float(row[0])
            throttle_value = row[1]
            if temp_value > 77.0:
                push = dev.push_note("ELEVATED TEMP", f"The Raspi is hot af, currently {temp}")
            elif throttle_value == "0x50005" or throttle_value == "0x50003" or throttle_value == "0x50007":
                push = dev.push_note("THROTTLING", "There was recent undervolting or thermal throttling")

    os.remove(file_path)
