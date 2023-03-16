# Colour changes via performing a filament change operation in your slicer

## Acquire a suitable print

A suitable print typically has a layer that you want in one colour and then at a certain height, the print changes so you want to perform a filament change e.g. to a new colour.

I have provided a Captain America shield STL in this github folder as a not so trivial example that has a number of colour changes.

It will require red, blue and white PLA.

## SLICING

### Prusa or super slicer

1) import the STL file into your slicer and centre it on your print bed.

2) Slice the print.

3) Now, in prusa slicer it might offer you the opportunity to automatically perform the colour changes for you if it guesses it's a logo.

We are not going to do that for this example but knock yourself out if you want to try that; we are considering the more general case of filament colour changes, e.g. for a key fob in this particular case.

4) Move the vertical slider up so it rises to the first two rings of the Captain America shield and only just dismisses the base layer.

5) Click the plus sign on the side of the vertical slider.

6) Rinse and repeat this operation for the next circle and then finally for the top star.

7) Reslice the print.

8) Export the gcode to an SD card for your printer OR upload it to a raspberry pi or similar and you can print.

### Cura

1) Perform the same operations as above for Prusa slicer or super slicer; however, instead of just clicking a plus button, you need to insert the command: M600.  Again rinse and repeat for all height filament colour changes.  There may be a plugin for cura that simplifies this process but I no longer use cura regularly so I am not an expert on the matter.

## PRINTING

1) Kick off the print

2) When the filament change operation occurs (I'm assuming marlin here, as I've never done it on klipper though I doubt it's very different, your printer may beep and ask you to press a button and remove/retract the current PLA filament.  Do that.

3) Insert new filament.  It will extrude and you may need to confirm the colour change is good on your printer menu.  If you need to extrude more filament to ensure that the filament is the correct colour then do so.  Nip off the filament ideally using some needle nosed pliers; hopefully your print head will have moved to the side of the bed and up a little to allow this operation.  When you're happy, confirm this with a button press on your printer and I strongly suspect a little more filament will extrude (it does on my prusa) just before you restart printing.  When this happens you need to be QUICK to nip that off with some needle nosed pliers or a suitable tool before it starts printing the next layer or it might smudge the print and make it look bad so be careful and quick about it.

4) Wait for the next layer to print, rinse and repeat this process until the print is done.  Wait for bed to cool and then remove the print from the bed and you'll be golden.

5) Happy filament colour change printing!!!
