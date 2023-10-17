#!/usr/bin/env bash

#### message library

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

## Message Helpers

function do_run_as_root_msg {
    echo -e "\nSonar - A WiFi Keepalive daemon\n"
    echo -e "This Script is not intended to run as ${USER}!\n"
    echo -e "Please enable the service by\n"
    echo -e "\t\e[34msudo systemctl enable sonar.service --now\e[0m\n"
    echo -e "GoodBye ..."
}

function wrong_args_msg {
    echo -e "Sonar: Invalid argument!\n"
    help_msg
}

function help_msg {
    echo -e "sonar - WiFi Keepalive deamon\nUsage:"
    echo -e "\t sonar [Options]"
    echo -e "\n\t\t-h Prints this help."
    echo -e "\n\t\t-v Prints Version of sonar."
    echo -e "\n\t\t-d Run sonar in DEBUG Mode.\n"
}

function fallback_msg {
    log_msg "WARN: No configuration file found ..."
    log_msg "INFO: Using fallback setup ..."
}

function debug_msg {
    printf "\e[31mDEBUG:\e[0m %s\n" "${1}"
}
