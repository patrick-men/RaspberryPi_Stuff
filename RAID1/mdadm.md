```
sudo apt update && sudo apt upgrade -y
sudo apt install mdadm

#check for name of drives and corresponding partitions
lsblk
```
Output:
```
NAME        MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT
sda           8:0    0 931.5G  0 disk
└─sda1        8:1    0 931.5G  0 part
sdb           8:16   0 931.5G  0 disk
└─sdb1        8:17   0 931.5G  0 part
mmcblk0     179:0    0  59.6G  0 disk
├─mmcblk0p1 179:1    0   256M  0 part /boot
└─mmcblk0p2 179:2    0  59.4G  0 part /
```

The chosen HDDs are sda and sdb
For RAID to work, the partitions need to be wiped:
```
sudo parted /dev/sda "rm 1"
sudo parted /dev/sdb "rm 1"
```

To check if everything worked out as intended: 
```
lsblk
```
Output:
```
NAME        MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT
sda           8:0    0 931.5G  0 disk
sdb           8:16   0 931.5G  0 disk
mmcblk0     179:0    0  59.6G  0 disk
├─mmcblk0p1 179:1    0   256M  0 part /boot
└─mmcblk0p2 179:2    0  59.4G  0 part /
```

Set partition tables for RAID1 (HDDs have < 2TB, so the msdos partition table is used):
```
sudo parted /dev/sda "mklabel msdos"
sudo parted /dev/sdb "mklabel msdos"
```

Now the partitions need to be set & activated
```
sudo parted /dev/sda "mkpart primary ext4 1M -1"
sudo parted /dev/sdb "mkpart primary ext4 1M -1"

sudo parted /dev/sda "set 1 raid on"
sudo parted /dev/sdb "set 1 raid on"
```

Check if everything is setup properly
```
sudo parted -s /dev/sda print
sudo parted -s /dev/sdb print
```
Output:
```
Model: Seagate Basic (scsi)
Disk /dev/sda: 1000GB
Sector size (logical/physical): 512B/4096B
Partition Table: msdos
Disk Flags:

Number  Start   End     Size    Type     File system  Flags
 1      1049kB  1000GB  1000GB  primary  ntfs         raid
---------------------------------------
Model: Seagate Basic (scsi)
Disk /dev/sdb: 1000GB
Sector size (logical/physical): 512B/4096B
Partition Table: msdos
Disk Flags:

Number  Start   End     Size    Type     File system  Flags
 1      1049kB  1000GB  1000GB  primary  ntfs         raid
```
Looks correct.

Now RAID needs to be initiated:

```
sudo mdadm --create /dev/md0 --level=1 --raid-devices=2 /dev/sda1 /dev/sdb1
```
Output: 
```
mdadm: /dev/sda1 appears to be part of a raid array:
       level=raid1 devices=2 ctime=Sat May  6 19:36:41 2023
mdadm: partition table exists on /dev/sda1 but will be lost or
       meaningless after creating array
mdadm: Note: this array has metadata at the start and
    may not be suitable as a boot device.  If you plan to
    store '/boot' on this device please ensure that
    your boot-loader understands md/v1.x metadata, or use
    --metadata=0.90
mdadm: partition table exists on /dev/sdb1
mdadm: partition table exists on /dev/sdb1 but will be lost or
       meaningless after creating array
Continue creating array? yes
mdadm: Defaulting to version 1.2 metadata
mdadm: array /dev/md0 started.
```
Check:
```
cat /proc/mdstat
```
Output: 
```
Personalities : [raid1]
md0 : active raid1 sdb1[1](F) sda1[0]
      976628736 blocks super 1.2 [2/1] [U_]
      bitmap: 8/8 pages [32KB], 65536KB chunk

unused devices: <none>
```
