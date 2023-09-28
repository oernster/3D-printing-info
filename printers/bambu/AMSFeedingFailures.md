### Solutions for the AMS having issues feeding filament (feeding back and forth multiple times and asking for a retry after multiple failures)...

## 1) Internal bowden issues

If your internal bowden clamp (the push down to release ring black clip device that holds your bowden in place to the extruder) is frayed then this can cause the AMS to feed filament back and forth and promote constant retry events on the touch screen UI.

This bowden also pokes just outside the rear of the printer.

In this scenario, please replace that bowden tube with a suitable length of spare bowden (Bambu supply plenty of spare tubing but you can pick up more if required on Amazon cheaply).

## 2) Bowden feeding to the AMS hub kinked

If the bowden on the rear of the AMS that feeds into the AMS hub on the rear of the printer is kinked, perhaps due to poor printer orientation c.f. the AMS position, then that will prevent the filament from feeding in to the AMS hub.

If this happens, you _may_ be able to get away with simply reorienting the printer so the bowden is no longer kinked.  Worst case scenario, replace the bowden that enters the rear of the AMS and feeds into the AMS hub on the rear of the printer.

## 3) The extruder and/or hotend may be clogged.

In this case, I recommend cleaning one or both of those while they are hot to ensure that there is no filament blocking the feeding path for printing.

Personally, I can recommend a noclogger tool (the short variant) from noclogger.com that can be used on this printer and others to carefully clean out the two pieces of hardware down to the nozzle while the hotend is hot, after removing the bowden tube and front plastic housing on the toolhead.

Once this has been done, reinsert the bowden securely and replace the front toolhead housing (be careful not to remove the connector to the toolhead front plastic piece housing while doing all of this but it is easy to reinsert it if this happens), then resume your print.  

## 4) Last resort

Refer to BambuAMSCleaning.md.  This is quite a lot more work but is likely to resolve your issues.

### CAVEAT

These are all the issues I've come across to date; feel free to refer to the official Bambu wiki.  There may well be others that cause the AMS to flash red or simply feed the filament back and forth multiple times then fail to continue printing.

I plan on maintaining this little document (and others) for the use of the community.
