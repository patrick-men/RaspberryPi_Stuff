# Hardware Check
With an upcoming RAID1 as well as regular crontab tasks in mind, I've implemented a script that regularly (1x per minute) checks certain hardware elements: Temperature and Undervolting.
Here, once again, the tool Pushbullet is being used, so that i can the notifications on my phone.

On a second go, this programm was changed as follows:
- Every second a python script reads the values and writes them into a .txt
- The main script, instead of getting the values from the device, reads the .txt
- This way, there's a more conistent data flow, meaning that if there was an undervolt or throttling within the last minute, it will be detected and reported

## Temperature
Temp was chosen both because of the workloads, as well as the upcoming summer. If the Raspi reached temps above 80°, it'll start throttling. As such, it's good to know when it's close. This allows to try cooling it down, assuming i'm nearby.

## Untervolting
Since there will be hardware attached to the Raspi, i want to ensure that there's no undervolting happening. This was the case when the 2 HDDs for the RAID1 were used, which is why it was moved to an external usb hub with its own power cord.
Since there's still the chance of undervolting, by whichever means that may be, it was added into this script.
