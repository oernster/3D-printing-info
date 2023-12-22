# Levelling a Voron 0 without a probe guide

Bed must be HOT as typical temperature; I use 105C for bed for ABS/ASA.

1) Perform a probe calibrate and get medium to light friction by stepping down to the print bed, then save_config after accepting.
2) Perform a BED_SCREWS_ADJUST with paper and get medium to light friction on each of the 3 probe points on the bed.  If you have to turn the screw for any probe point more than 1/4 of a turn then select adjusted, else accept.
3) Perform another probe_calibrate with paper for medium to light friction.
4) In your favourite slicer, e.g. orca slicer, create a cube primitive (a standard cube, not a voron cube which is shaped differently), scale it to match most of the size of the bed with uniform scaling.
5) Turn off uniform scaling and set z mm setting to 0.24mm.
6) Slice that print.
7) Send it to your printer and print it.
8) Live adjust z while printing to get the best level you can.
9) You may need to do step 7 multiple times, potentially 8 as well with adjustments to your bed screws as appropriate.
10) Once you have a lovely first layer you are now ready to print.
