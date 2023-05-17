# Filebrowser
Initially, Docker needed to be installed. The Raspbian OS was a fresh install in an attempt to clear the NCP leftovers, since it rooted itself deep into the system:
```bash
curl -fsSL https://get.Docker.com -o get-Docker.sh
```

Afterwards, the required image needed to be pulled, but not run yet. To run the file, a [docker-compose.yml](docker-compose.yml) file was used.
In there, all the requirements are set: The location for the files to be saved, the location of the db etc.


Only thing left was to make sure that the container would run whenever the system needs to reboot. This is accomplished with the restart flag: ```--restart unless-stopped``` will restart the container unless it was stopped, which shouldn't be the case on a reboot. Since this container is run with a docker-compose file, it needs to be implemented as follows:
```Dockerfile
services:
  myservice:
    image: myimage
    restart: unless-stopped
```
