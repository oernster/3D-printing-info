# sovol-sv06-klipper-setup
Setup guide for Sovol SV06 with klipper

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

Next ssh/winscp or putty into your pi and rename either the printer_cura.cfg or the printer_superslicer.cfg file I have attached to this repository to printer.cfg first, then copy it to to the /home/pi/printer_data/config directory.  Note prusaslicer does not support klipper natively; though it _sort of works_ with marlin 2 set as the firmware; personally I would not trust that so if you want klipper I think a good slicer choice is superslicer.  Note that you can export a config bundle from prusaslicer and import it into superslicer if that was your previous slicer.  

Insert IP address of your pi into your browser and you're almost good to go.

## Slicer configuration

# Superslicer

In Printer Settings ~ Custom Gcode ~ Start gcode: enter... 

PRINT_START EXTRUDER={first_layer_temperature[initial_extruder] + extruder_temperature_offset[initial_extruder]} BED=[first_layer_bed_temperature] CHAMBER=[chamber_temperature]

In end gcode enter...

PRINT_END

Make sure you set (using the cog icon in printer settings) your printer name, the ip address of your pi (without http://) and the printer firmware to klipper.
