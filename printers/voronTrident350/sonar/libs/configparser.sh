#!/usr/bin/env bash

#### Configparser library

#### Sonar - A WiFi Keepalive daemon
####
#### Written by Stephan Wendel aka KwadFan <me@stephanwe.de>
#### Copyright 2022
#### https://github.com/mainsail-crew/sonar
####
#### This File is distributed under GPLv3
####

# shellcheck enable=require-variable-braces

# Exit on Errors
set -Ee

# Read Configuration File
# call get_param section param
# spits out raw value
function get_param {
    local section param
    section="${1}"
    param="${2}"
    crudini --get "$(get_config_path)" "${section}" "${param}" 2> /dev/null | \
    sed 's/\#.*//;s/[[:space:]]*$//'
}
