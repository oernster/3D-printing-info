# sovol-sv06-klipper-setup
Setup guide for Sovol SV06 with klipper

First off install git for your PC/linux/mac from here: https://github.com/git-guides/install-git

Then on a command line or terminal (cmd.exe on windows, Terminal on a mac or linux box) go to the green Code button at the top right of this web page and click it.  Then click the two squares button to copy.

Then type:

git clone -paste in your copied command here without minus signs-

This should copy this entire repository to your local machine.

## Flash Mainsail to your pi using raspberry pi imager

Note: If you do not have a RPI then use kiauh as follows...

First install git on your pi variant:

sudo apt install git

Then...

git clone https://github.com/th33xitus/kiauh.git

run

### ./kiauh/kiauh.sh

and install klipper if it hasn't already been installed by the mainsail image, as well as mainsail.

## Flash klipper to your printer

Turn off printer.

Insert 8GB/16GB SD card into your PC/linux box/mac and copy the 
firmware.bin file (which was originally 
'klipper-0.11.0-sovol-sv06.bin') to your SD card root directory.

Eject the SD card from your computer and insert into your printer.

Turn on the printer.

Wait for 3-5 mins.  The screen will not display anything of interest and 
you just need to wait.

Next ssh/winscp or putty into your pi and copy the printer.cfg file I have attached to this repository to the /home/pi/printer_data/config directory.

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
