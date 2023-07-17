# Levelling starter for 10

If you want to level then just download calibration shapes from Ultimaker 
as a plugin to Cura.  Then, restart Cura.

Next, under part for calibration in the extensions menu, create a cube.  
Turn off uniform and snap scaling and set the z to 0.24mm.

Most FDM cartesian printers:
If your printer allows live adjusting of your z offset while printing 
(marlin is fine for this, just use your printer menus)…

[Alternatively, in a klipper setup where you can send GCODE commands from 
a browser such as: G92 Z0.1 (this means go down 0.1mm on the z-axis; -ve 
means go up) in the console].

Ender 3 specific:

If you have an ender, as I understand it you cannot live adjust the z 
offset.  In this case, just print one square at a time.  In this case, 
adjust your z offset on a per print basis to match the ideal layer in the 
pictures.  Start with about 0.25mm above the heatbed and then adjust down 
gradually by 0.05mm then 0.01mm.

Continuing to sort the squares out:

Then multiply the square by 8 copies in cura so you have 9 well spaced 
squares, then set your z offset to about 0.05mm x 5-6 above the build 
plate.  To clarify for people who aren't very bright, this means multiply
0.05mm by 5 or 6 to give you approx 0.25mm to ensure that you don't crash
your nozzle into the build plate.

Then, print your 9 squares and after each one manually adjust your z 
offset down by 0.05mm and then 0.01mm or up if need be to eventually match 
the ideal goal in the pictures in that guide for a good layer. 

You may need to print 2 sets of 9 squares to get it just right but once 
done you should be very happy with the results.

Refer to my Prusa calibration picture in this directory for an example of 
a really good first layer/square.
