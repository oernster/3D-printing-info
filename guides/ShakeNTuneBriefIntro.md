# Brief introduction to Shake 'n' Tune (original author of SnT is Frix)

### This guide is based on this tool: https://github.com/Frix-x/klippain-shaketune

### NOTE: A LIS2DW accelerometer will produce unpredictable results.  You ideally want an ADXL345 accelerometer.

### The RESULTS will be stored under MACHINE in mainsail in KShakeTune_Results 

## Order of events

(Do all of this cold; apart from your final measurement of your axes (input shaping) which should be done hot with fans going at normal rates to test correct resonances).

1) Do your belts

2) Do your input shaping

2a) Remove unwanted resonances seen in input shaping graphs

2b) Rinse and repeat input shaping until resonances disappear that you do not want

3) Run vibrations graph generator

## BELTS

### Mounting the belts...

Lay both of your belts on the floor (a flat surface not a carpet) and ensure that both are EXACTLY the same length.

Then, using a sharpie, (red works well), mark a tooth on both sides 20cm vertically on both belts (this assumes a 350 printer, consider 15cm for a 300, maybe 12cm for a 250).

Next loosen up both idlers completely.

Then mount the belts.  You want to be able to see when mounting that the red lines line up vertically on the front of the printer, left and right sides

Pull the belts to reasonable tension on both sides (as tight as possible without overdoing it; you'll struggle to get them overtight unless you are pulling them towards you).

Then once you've mounted both belts successfully to the carriage using whatever mounting mechanism you use and tightened up the belt mounts, tighten up the idlers.

### 1) First off we need to get your belts tuned to be 110Hz on each belts

Methods include (all require that you turn off motors and move the gantry to 15cm/150mm from the front idlers):

a) Use a 3D printed and constructed GT2 tension meter; this: 

https://github.com/Diyshift/3D-Printer/blob/main/GT2%20Belt%20Tension%20Meter/Manual/GT2_Tensiometer_Manual.pdf

b) Use Spectroid (available on Android phones) and tune to 110Hz on left and right belt.

c) Use Gates carbon drive (available on apple and android phones)

d) Use a guitar tuning app and tune to the tone that is 110Hz

e) Use this online tone generator and use your ears if they are good enough: https://onlinetonegenerator.com/

### 2) Now that you've done that, home your printer and run the macro: COMPARE BELTS RESPONSES.

DEEP DIVE HERE: https://github.com/Frix-x/klippain-shaketune/blob/main/docs/macros/compare_belts_responses.md

a) You should be able to see (if you have a good starting point and tuned to 110Hz on each belt well) that you are almost getting 

two peaks which need to align (in purple and orange) or potentially two double peaks which need to align.

What you are after is the purple and orange peaks to be aligned and at the same height in an ideal world but if the amplitude differences

are not completely aligned it's not the end of the world.  Furthermore, in an ideal world you are after 90%+ similarity on the belts;

NOTE: The percentage similarity is less important than the shape of the graph; you are aiming for ideally a single joint peak.

NOTE2: For more assistance with SnT belts tuning and general resonance tuning there is a special channel available to those who have serialised their Voron printers on Discord.

When tuning the belts, you want to tighten by about 1/4 to 1/8th of a turn each time you adjust on either the B or A idler.

The B idler is on the left and the A idler is on the right.  Think of looking at your printer as like looking at a sheep; a sheep goes BAAAAAA, hence BA left to right.

Now, ignore the peak labels on the graphs, they are badly labelled - they are NOT your belts.  Your B belt is the orange graph, the purple one is your A belt.
NOTE: The peak labelling is planned to be changed to Greek lettering to reduce confusion soon.

### 3) Now run the AXES SHAPER CALIBRATION macro.  This will perform your input shaping.

DEEP DIVE HERE: https://github.com/Frix-x/klippain-shaketune/blob/main/docs/macros/axis_tuning.md

Once you see the results for input shaping as a graph, typically if you see peaks starting around 0Hz this might be caused by binding (i.e. a low frequency signal) 

so check your idlers and pulleys for too much tension and you may need to redo your belts at this point if you adjust tension here.

Other peaks that are unwanted can be tested by hand; what you need to do is insert the frequency, the time of run (I choose about 60 seconds) and the axis that is resonating on the input 

shaping graph that is producing said peak or peaks; you may need to excite multiple frequencies.

The macro to run is called: EXCITE AXIS AT FREQ; use the DROPDOWN.

NOTE: if you have a lot of noise in your graph then you can increase the accel_per_hz value by e.g. 20-25 at a time to 100 (default is 75), then 125 etc under [resonance_tester] in your  printer.cfg file.

Once you're done, take the recommended shaper for either performance or vibrations (I always take the best vibrations one; preferably 0.0% or 0.something%), frequency and damping ratio 

and add it to your printer.cfg (or at the base in the commented section if you have already saved one to replace that.

If you have greater than 5% vibrations on either IS graph (x or y) then you may want to worry about your hardware a little.  The recommended shaper is a combination of vibrations and smoothing 

at the recommended acceleration and most of the time smoothing is more important according to Frix.  You can always check and validate with a test print.

I've spoken to Frix and he says that the filter recommendation (performance) will be suitable for most scenarios in future and the vibrations shaper will be much more of a last resort choice.

You want to choose the lower of the two max recommended accels (x and y) for your outer walls on your slicer profile for printer with.

### 4) Once you've tuned everything

DEEP DIVE HERE: https://github.com/Frix-x/klippain-shaketune/blob/main/docs/macros/vibrations_profile.md

Run the macro CREATE VIBRATIONS PROFILE.

This will produce a set of useful graphs that you can study to improve your slicer settings.  Generally speaking you might want to choose a minimum speed to avoid vibrations in your slicer.

Apart from that, this section I will leave relatively limited I'm afraid for now as this is a new feature that I'm still getting familiar with myself; I'll update as I learn more.
