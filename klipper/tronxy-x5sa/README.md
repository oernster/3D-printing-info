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

Next ssh/winscp or putty into your pi and rename either the printer_cura.cfg or the printer_superslicer.cfg file I have attached to this repository to printer.cfg first, then copy it to to the /home/pi/printer_data/config directory.  Note prusaslicer does not support klipper natively; though it _sort of works_ with marlin 2 set as the firmware; personally I would not trust that so if you want klipper I think reasonable slicer choices include _either_ superslicer _or_ cura.  Note that you can export a config bundle from prusaslicer and import it into superslicer if that was your previous slicer.

Insert IP address of your pi into your browser and you're almost good to go.

## Slicer configuration

# Prusa/Superslicer

In Printer Settings ~ Custom Gcode ~ Start gcode: enter... 

PRINT_START EXTRUDER={first_layer_temperature[initial_extruder] + extruder_temperature_offset[initial_extruder]} BED=[first_layer_bed_temperature] CHAMBER=[chamber_temperature]

In end gcode enter...

PRINT_END

# Cura

In Settings ~ Printer ~ Manage Printers ~ Machine Settings ~ Start gcode: enter...

SET_GCODE_VARIABLE MACRO=PRINT_START VARIABLE=bed_temp VALUE={material_bed_temperature_layer_0}
SET_GCODE_VARIABLE MACRO=PRINT_START VARIABLE=extruder_temp VALUE={material_print_temperature_layer_0} 
PRINT_START

In end gcode enter...

SET_GCODE_VARIABLE MACRO=PRINT_END VARIABLE=machine_depth VALUE={machine_depth}
PRINT_END

Now you want the 'moonraker connection' plugin for cura as you want to be able to upload to your pi as well after you've sliced a print.

Once you have installed it, restart cura. 

In Settings ~ Printer ~ Manage Printers ~ Connect Moonraker set your ip address as follows: http://10.0.0.1/ (adjust for the ip address of your pi).

Next, in the Upload tab, select UFP with thumbnail.  I tick everything else but that's up to you.

the field '
