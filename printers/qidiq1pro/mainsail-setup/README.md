# Instructions for installing mainsail on a Qidi Q1 Pro

## ssh into the printer (putty/MobaXTerm/command line/powershell/terminal).
## You'll need to identify the IP address of the printer; I recommend AngryIPScanner for this job, found here: https://angryip.org/
## Sort by hostnames after you've scanned.  Then ssh in with user: root, password: makerbase

## Run these commands... (when NOT printing!!!)

### ```sudo apt install git```
### ```cd /home/mks```
### ```git clone https://github.com/mainsail-crew/mainsail.git```
### ```chown www-data:www-data mainsail```
### ```chmod 0644 mainsail```

## Install WinSCP from here: https://winscp.net/eng/download.php

### When it runs, choose SFTP and specify your IP address, username (root) and password (makerbase)
### Copy the mainsail file from this repository into /etc/nginx/sites-available

## Run these commands
### ```ln -s /etc/nginx/sites-available/mainsail /etc/nginx/sites-enabled/```
### ```systemctl restart nginx```

## If any command complains (it shouldn't since you're root), then rerun it with sudo as a prefix with a space e.g.: 
### ```sudo ln -s /etc/nginx/sites-available/mainsail /etc/nginx/sites-enabled/```

## Now run:
### ```systemctl restart moonraker```
### ```systemctl restart klipper```

# Now Mainsail should be available from here: http://(your IP address without brackets):8081

# TADA!
