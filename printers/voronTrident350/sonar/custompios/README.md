# Sonar

Sonar - A WiFi Keepalive daemon

# Developer Documentation

The folder 'sonar' is made to add to your existing CustomPIOS Structure.

If you are not already familiar with this, copy 'sonar' folder to

    /src/modules

Also edit the config file to choose, if moonraker should get an \
update manager entry for sonar.

    # Add Sonar to moonraker.conf (update manager) bool (1:yes / 0:no)
    [ -n "$SONAR_SONAR_ADD_SONAR_MOONRAKER" ] || SONAR_SONAR_ADD_SONAR_MOONRAKER=1

This is enabled by default.

Finally add sonar to your config!
As example:

    export MODULES="base(network,raspicam(klipper,moonraker,mainsail,sonar))"
