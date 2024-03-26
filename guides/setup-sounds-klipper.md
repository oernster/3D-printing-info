So, if you want to setup cool sounds; this assumes a 3.5in jack in your pi, I'm using the 3W pihut speakers via usb and jack (you can replace the .wav files as you desire) you can follow my config here:
1) check delayed_gcode in printer.cfg
2) check shell_commands.cfg
3) check /home/pi/printer_data/config/macros.cfg for the calls out to the sound macros.
4) install kiauh's custom shell command capability from advanced menu

You will need to modify the .sh files as follows:
sudo chmod 0777 *.sh
 in your printer_data/config directory.

You will also probably need to run this command and use the up/down cursor keys to set the volume:
alsamixer


https://github.com/oernster/3D-printing-info/tree/main/printers/voronTrident350
https://thepihut.com/products/usb-powered-speakers