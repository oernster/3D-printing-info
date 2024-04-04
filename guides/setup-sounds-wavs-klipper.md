# Playing custom WAV sounds on your raspberry pi in klipper HOWTO (I use 2001 Space Odyssey samples but knock yourself out with whatever you want for YOUR printer).

## You will need:

1) A klipper printer

2) A set of speakers ( I use these: https://thepihut.com/products/usb-powered-speakers ); these are USB/audio jack speakers.  I have not experimented with a bluetooth speaker setup.

## 1) Install via kiauh, which you can find here:

https://github.com/dw-0/kiauh 

...the advanced option: gcode shell command.

## 2) Create a shell command similar to my shell command here: https://github.com/oernster/3D-printing-info/blob/main/printers/voronTrident350/print_start.sh

This pre-supposes that you have a print_start.wav file.  It also assumes you have aplay installed which if not on your variant of raspbian you can install with: sudo apt install aplay


You can customise the print_start.wav filename and shell script name as per your needs.


You _may_ need to install this: sudo apt install alsamixer

This allows you to increase/set the volume of your speakers so you can actually hear something from your setup.  You can run it as alsamixer from teh command line.

## Create a config file such as shell_command.cfg here: https://github.com/oernster/3D-printing-info/blob/main/printers/voronTrident350/shell_command.cfg

This can be customised to your specific needs and wav files.  

Include shell_command.cfg in your printer.cfg header files.  You must have all the wavs and shell scripts in the same directory as your printer.cfg file.


# What if I want a wav file to be played on printer startup?

## To do that you need to add this to your printer.cfg:

```
[delayed_gcode startup]
initial_duration: 2
gcode:
    PRINTER_STARTUP_SOUND
```

### Now, if you want to customise your macros to play specific sounds due to an event then simply make a call to the relevant gcode customised sound from the shell_command.cfg file we discussed earlier.
### Examples can be found in my PRINT_START macro here: https://github.com/oernster/3D-printing-info/blob/main/printers/voronTrident350/configs/macros.cfg


