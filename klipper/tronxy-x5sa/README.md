# tronxy-x5sa-klipper-setup
Setup guide for Tronxy x5sa with klipper

You will need: Your 8GB Tronxy x5sa supplied SD card, a computer with SD card port/USB adaptor, another SD card for a raspberry pi or whatever pi variant you want to use and the pi variant itself; ideally an rpi but an orange pi or rock pi will do just fine.

## Flash Mainsail to your pi using raspberry pi imager

Note: If you do not have a RPI then use kiauh as follows...

First install git on your pi variant:

sudo apt install git

Then...

git clone https://github.com/th33xitus/kiauh.git

run

### ./kiauh/kiauh.sh

and install klipper if it hasn't already been installed by the mainsail image, as well as mainsail.

## Flash klipper to your printer (assumes F446 chip)

Turn off printer.

Insert 8GB SD card into your PC/linux box/mac and copy either the update-marlin or update-klipper directory as appropriate for the firmware you want.  Then rename the directory to update instead of update-klipper or update-marlin - you ONLY WANT ONE of these directories present.

I have provided marlin and klipper flashable firmwares for this chipset.  Here on in I will be only concerned with klipper.

Eject the SD card from your computer once the update directory is present and insert into your printer.

Turn on the printer.

Once flashed, it should beep twice to confirm; it's possible you haven't got the beeps turned on in which case just wait for 3-5 mins - your printer may look like it's crashed - IT HAS NOT do NOT worry.

The screen will not display anything of interest.

Next ssh/winscp or putty into your pi and copy ther printer.cfg file I have attached to this repository to the /home/pi/printer_data/config directory.

Insert IP address of your pi into your browser and you're almost good to go.

## Slicer configuration

# Prusa/Superslicer

In Printer Settings ~ Custom Gcode ~ Start gcode: enter... 

PRINT_START EXTRUDER={first_layer_temperature[initial_extruder] + extruder_temperature_offset[initial_extruder]} BED=[first_layer_bed_temperature] CHAMBER=[chamber_temperature]

In end gcode enter...

PRINT_END

# Cura

In Settings ~ Printer ~ Manage Printers ~ Machine Settings ~ Start gcode: enter...

PRINT_START EXTRUDER='"{first_layer_temperature[initial_extruder] + extruder_temperature_offset[initial_extruder]}"' BED='"[first_layer_bed_temperature]"' CHAMBER='"[chamber_temperature]"'

In end gcode enter...

PRINT_END
