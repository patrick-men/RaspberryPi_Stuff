# Hardware Check
With an upcoming RAID1 as well as regular crontab tasks in mind, I've implemented a script that regularly (1x per minute) checks certain hardware elements: Temperature and Undervolting.
Here, once again, the tool Pushbullet is being used, so that i can the notifications on my phone.

On a second go, this programm was changed as follows:
- The Script runs on startup, this is done with crontab: ```@reboot /bin/usr/python3 /path/to/script.py```
- Since the push notifications require internet, i implemented a check whether there is an active internet connection or not. Once that is fulfilled, the script itself starts running
- Every second a python script reads the values and writes them into a .csv
- The main script, instead of getting the values from the device, reads the .csv
- This way, there's a more conistent data flow, meaning that if there was an undervolt or throttling within the last minute, it will be detected and reported

## Temperature
Temp was chosen both because of the workloads, as well as the upcoming summer. If the Raspi reaches temps above 80°, it'll start throttling. As such, it's good to know when it's close. This allows to try cooling it down, assuming i'm nearby.

## Untervolting
Since there will be hardware attached to the Raspi, i want to ensure that there's no undervolting happening. This was the case when the 2 HDDs for the RAID1 were used, which is why it was moved to an external usb hub with its own power cord.
Since there's still the chance of undervolting, by whichever means that may be, it was added into this script.

## Files that are being used
I've tried several times to check the contents of the file while the script was running, either by spamming ```cat``` or using ```tail -f```.
This didn't work and I assumed that the code was broken. This is, however, false (but lead to me optimizing the code):

When a file is being used by a script like here, the data isn't directly written into the file, but rather saved in a cache. As such, the file is under use at it saves ressources this way. This leads to the file not having any content when observed from outside with the aforementioned methods.
As such, the script works and I got lost in an error that didn't exist :D
