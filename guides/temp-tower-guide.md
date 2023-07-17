So, quick guide to doing a temperature tower in case you haven't done it before...

First off, here's a useful temperature tower link: https://www.thingiverse.com/thing:2615842

Basically, you slice your temp tower once, then move the slider (vertical) up to the 
next temp change point in 'preview' then enter some example gcode which is 
'M109 S220' say - that would set the temp to 220C and wait for the temp to settle.

Note that this is the same for Marlin and Klipper.

Then repeat on the next temp change point further up to e.g. 'M109 S215' - rinse, 
repeat all the way up.

However, it waits for the hotend to reach it's target rather than sets it; so, this 
assumes that you start at a high temp and are cooling on your way up.

If you happen to have a temperature tower STL that goes UP in temperature as it rises,
then you will need to do a 'M104 S215' which sets the temperature.  You might want to do
both M104 and M109 in that scenario. 
