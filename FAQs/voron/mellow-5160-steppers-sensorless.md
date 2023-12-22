# FAQs

# Mellow v1.5 external 5160 drivers setup on an Octopus Pro by BTT

You will need to jump the horizontal SD and the horizontal SPI pins on the 5160 stepper external board.

NOTE: This is for sensorless setup; see my configs in printers/voronTrident350 for details; specifically printer.cfg [stepper_x] and y and also the tmc6160 variants.  Furthermore, please review the configs/sensorless.cfg file.

NOTE 2: If you are starting out then I recommend you set the threshold values to -64 for both x and y steppers to begin with when testing home of x and y; the toolhead should no move in this case.

The ribbon cables should be mounted AFTER you have gently lifted and moved aside the black ribbon plastic mount on the stepper itself and with the blue side of the ribbon cable on the black side, then carefully slot it back into place.

Be careful not to supply 48V to the external stepper drivers or you'll bork them!  Been there, done that!

If you experience GSTAT or GLOBAL SCALER errors then it might be worth trying this command to check that you can read/write to the steppers:

### DUMP_TMC STEPPER=stepper_x (Repeat for stepper_y) - You should see movement on the toolhead.

To save you constantly performing a firmware_retsart, consider sending this command: 

### SET_TMC_FIELD FIELD=SGT STEPPER=stepper_y VALUE=-2

You can adjust the stepper_ to x or y as appropriate and the VALUE to the value that you would normally set the driver_SGT value to.

It's worth performing a stepper buzz on x and y to see if the print toolhead moves in an appropriate direction and the steppers are actually functioning:

### STEPPER_BUZZ stepper=stepper_y (repeat for x)

Now, if like me, you migrated from endstops to sensorless, it is quite possible that when you cut your endstop wires you also cut your motor wires (don't ask) so please check you haven't done this or your toolhead will not home x and y correctly.

Once all this has been sorted out then you should be able to comfortably bump but not crash into x on the side of your printer and y at the rear of your printer as appropriate, then home z.

