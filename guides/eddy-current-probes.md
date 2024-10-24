# There are 3 companies creating eddy current scanners on the market as of October 2024. 

1) Beacon revH.

2) The cartographer

3) The BTT Eddy Current Scanner which is untested by anyone I know and I would avoid that option until it has been.

4) I _think_ there is a Mellow one as well on the market now but I have no experience with it. 

### Carto:

Supports CANBUS/USB, soon™️ will support higher temperature chambers, 1/4 of the price, once you include shipping, not as good quality components as Beacon but perfectly good.  Supports something virtually identical to Beacon Touch called Survey.  Normal and low profile variants available.

### Beacon:

Supports USB, supports higher temp chambers, pricey, high quality electronics and connector, has Beacon Touch.  Normal and low profile variants available.

### Carto CNC mount

Works with both Beacon and Carto.  Supports normal v6 hotends for SB and UHF hotends (I use standoffs but they have a custom variant for just this).  It does not support Xol if you don't have UHF though which is where the aforementioned CNC Xol Carriage comes in.

### For more information:

1) Beacon: https://beacon3d.com/ and here: https://docs.beacon3d.com/quickstart/ and also here: https://github.com/beacon3d/beacon_klipper

2) Cartographer: https://cartographer3d.com/

## Side notes:

If you want info about survey adjustment after scanning but you need to do meshing not by scanning, this is not supported by the Cartographer...

The way to deal with that, would be to create faulty regions in your bed mesh settings; see below:

https://www.klipper3d.org/Bed_Mesh.html#faulty-regions

However, if you're using a magnetic bed or bed with magnets in then maybe an Eddy Current sensor isn't really what you're looking to use on your printer (unless of course you use faulty regions).
