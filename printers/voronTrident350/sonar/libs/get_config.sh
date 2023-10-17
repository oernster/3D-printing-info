#!/usr/bin/env bash

#### get_config library

#### Sonar - A WiFi Keepalive daemon
####
#### Written by Stephan Wendel aka KwadFan <me@stephanwe.de>
#### Copyright 2022
#### https://github.com/mainsail-crew/sonar
####
#### This File is distributed under GPLv3
####

# shellcheck enable=require-variable-braces

set -Ee

## Determine Configuration File and set defaults if not found.

function get_config_path {
    local dot_config_file new_path old_path path
    dot_config_file="${BASE_SNR_PATH}/tools/.config"
    new_path="${BASE_USER_HOME}/printer_data/config/sonar.conf"
    old_path="${BASE_USER_HOME}/klipper_config/sonar.conf"
    fallback="${BASE_SNR_PATH}/resources/sonar.conf"

    if [[ -f "${dot_config_file}" ]]; then
        # shellcheck disable=SC1090
        source "${dot_config_file}"
        if [[ -f "${SONAR_CONFIG_PATH}" ]]; then
            path="${SONAR_CONFIG_PATH}"
        fi
    fi
    if [[ -f "${new_path}" ]] && [[ ! -h "${new_path}" ]]; then
        path="${new_path}"
    fi
    if [[ -f "${old_path}" ]] && [[ ! -f "${new_path}" ]]; then
        path="${old_path}"
    fi
    # Fallback Handling
    if [[ ! -f "${old_path}" ]] && [[ ! -f "${new_path}" ]]; then
        path="${fallback}"
        fallback_msg
    fi
    echo "${path}"
}
