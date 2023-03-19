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

Next ssh/winscp or putty into your pi and copy either the printer_cura.cfg or the printer_superslicer.cfg file I have attached to this repository to the /home/pi/printer_data/config directory.  Note prusaslicer does not support klipper natively; though it _sort of works_ with marlin 2 set as the firmware; personally I would not trust that.

Insert IP address of your pi into your browser and you're almost good to go.

## Slicer configuration

# Prusa/Superslicer

In Printer Settings ~ Custom Gcode ~ Start gcode: enter... 

PRINT_START EXTRUDER={first_layer_temperature[initial_extruder] + extruder_temperature_offset[initial_extruder]} BED=[first_layer_bed_temperature] CHAMBER=[chamber_temperature]

In end gcode enter...

PRINT_END

# Cura

In Settings ~ Printer ~ Manage Printers ~ Machine Settings ~ Start gcode: enter...

SET_GCODE_VARIABLE MACRO=START_PRINT VARIABLE=bed_temp VALUE={material_bed_temperature_layer_0}
SET_GCODE_VARIABLE MACRO=START_PRINT VARIABLE=extruder_temp VALUE={material_print_temperature_layer_0}
START_PRINT

In end gcode enter...

SET_GCODE_VARIABLE MACRO=END_PRINT VARIABLE=machine_depth VALUE={machine_depth}
END_PRINT

Now you want the 'moonraker connection' plugin for cura as you want to be able to upload to your pi as well after you've sliced a print.

Once you have installed it, restart cura. 

In Settings ~ Printer ~ Manage Printers ~ Connect Moonraker set your ip address as follows: http://10.0.0.1/ (adjust for the ip address of your pi).

Next, in the Upload tab, select UFP with thumbnail.  I tick everything else but that's up to you.
