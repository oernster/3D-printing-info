# Guide to levelling a Trident (I have a 350 bed)

## Heat your bed to 105C if your typical filament is ABS/ASA.  For TAP probing you will need to reduce your temp to around 150C before you can home which is necessary for the next step. 

1) Home your printer.
2) Send the command PROBE_CALIBRATE
3) Adjust z in Mainsail until, with a piece of paper under the nozzle, you haev medium to light friction pushing back and forth.
4) Accept and SAVE_CONFIG.
5) Set bed temp back to 105C again following the save_config's firmware_restart.

## Open your favourite slicer e.g. Orca

1) Create a primitive cube (not the voron or orca cube) and scale it to approx 1/2 the width / depth of your print bed on x and y using uniform scaling.
2) Turn off uniform scaling and set the z height to 0.24mm.
3) Slice the print and send it to the printer.
4) Live adjust z on the fly while it prints either using your printer's small screen or in mainsail to get a perfect first layer.
5) On COMPLETION of the print, NOT BEFORE, perform a SAVE on the z offset section in Mainsail, then perform a SAVE_CONFIG; a firmware_restart should then update.
6) You may need to repeat steps 4 and 5 until you get a perfect first layer.
7) Once you've done all of that then you can print with a levelled printer.
