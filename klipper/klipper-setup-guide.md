# KLIPPER SETUP GUIDE

Setup is relatively straightforward.  Install mainsail using the raspberry pi imager on your pi.  (Make sure you configure wifi and ssh to be on).  Then do a 

# sudo apt install git

 then do a 

# git clone https://github.com/th33xitus/kiauh.git

run

# ./kiauh/kiauh.sh

 and install klipper if it hasn't already been installed by the mainsail image.

Then you'll need to 

# cd klipper

 and do a 

# make menuconfig

 and setup the klipper build according to your particular motherboard.  You will need to identify the chip on your motherboard by looking at it directly or googling for the schematic online.  Once you've configured the klipper build, do a 
make

 and then copy the klipper.bin file from the out directory to an SD card.

The SD card should be no larger than 16GB ideally as some motherboards don't like large sized cards.  Rename the klipper.bin file to firmware.bin and then turn your printer off, plug in the SD card, turn it on and wait for 5 minutes.  Then turn it off again, unplug the SD card and turn it on again.

Then I recommend downloading an app you can get from https://www.fing.com/ and scan your network for the pi device.  This is to retrieve the IP address of the pi.  Then go to that IP address on your browser and mainsail should appear.

After that you will need to edit (from the machine section in mainsail) the printer.cfg file appropriately for your needs.  First off, aside from getting a config file off the internet ideally, you will need to identify the correct mcu.

To do that, you need to ssh into your pi, e.g. 

# ssh pi@10.0.0.1

 then first make sure you pi is connected to the printer using a USB A to USB B cable.  Then send the command 

# lsusb

 - that will show you whether the pi can see the printer.

Next, you need to run the command: 

# ls /dev/serial/by-id

 and the full string that is displayed, you will need to copy and insert in the mcu section of your printer.cfg file.

After that you should be up and running with mainsail.  TBH the most challenging bit is configuring klipper for a build but it's not very hard to do if you've identified the chip.

I recommend printing a case for your pi though - there are plenty on printables.com or thingiverse; take your pick

