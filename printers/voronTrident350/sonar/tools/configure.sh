#!/usr/bin/env bash

#### Sonar - A WiFi Keepalive daemon
####
#### Written by Stephan Wendel aka KwadFan <me@stephanwe.de>
#### Copyright 2022
#### https://github.com/mainsail-crew/sonar
####
#### This File is distributed under GPLv3
####

# shellcheck enable=require-variable-braces
# shellcheck disable=SC2317

# Exit on errors
set -Ee

# Debug
# set -x

### Non root
if [[ ${UID} == '0' ]]; then
    echo -e "DO NOT RUN AS ROOT!\nExiting..."
    exit 1
fi

# Global Vars
SR_CONFIG_USER=$(whoami)
SR_CONFIG_CONFIGFILE="tools/.config"
SR_CONFIG_ROOTPATH="/home/${SR_CONFIG_USER}/printer_data"
SR_CONFIG_CONFIGPATH="${SR_CONFIG_ROOTPATH}/config"
SR_CONFIG_LOGPATH="${SR_CONFIG_ROOTPATH}/logs"
SR_CONFIG_ENVPATH="${SR_CONFIG_ROOTPATH}/systemd"
SR_MOONRAKER_CONFIG_PATH="${SR_CONFIG_CONFIGPATH}/moonraker.conf"

### Messages
header_msg() {
    clear
    echo -e "\e[34m\n #### Sonar Install Configurator ####\e[0m\n"
}

welcome_msg() {
    header_msg
    echo -e "This will guide you through install configuration"
    echo -e "After successful configuration use\n"
    echo -e "\t\e[32msudo make install\e[0m\n"
    echo -e "to install Sonar ..."
}

abort_msg() {
    header_msg
    echo -e "Configuration aborted by user ... \e[31mExiting!\e[0m"
}

check_config_file_msg() {
    header_msg
    echo -e "\n\t\e[33mWarning:\e[0m Found an existing .config!\n"
}


default_path_msg() {
    echo -e "Hit ENTER to use default."
}

config_path_msg() {
    header_msg
    echo -e "Please specify path to config file (sonar.conf)\n"
    echo -e "\t\e[34mNOTE:\e[0m File names are hardcoded! Also skip trailing backslash!"
    echo -e "\tDefault: \e[32m${SR_CONFIG_CONFIGPATH}\e[0m\n"
}

log_path_msg() {
    header_msg
    echo -e "Please specify path to log file (sonar.log)\n"
    echo -e "\t\e[34mNOTE:\e[0m File names are hardcoded! Also skip trailing backslash!"
    echo -e "\tThe log will only appear if persistant_log is set to 'true'"
    echo -e "\tOtherwise use journalctl to view log."
    echo -e "\tDefault: \e[32m${SR_CONFIG_LOGPATH}\e[0m\n"
}

env_path_msg() {
    header_msg
    echo -e "Please specify path to service environment file (sonar.env)\n"
    echo -e "\t\e[34mNOTE:\e[0m File names are hardcoded! Also skip trailing backslash!"
    echo -e "\tDefault: \e[32m${SR_CONFIG_ENVPATH}\e[0m\n"
}

add_moonraker_entry_msg() {
    header_msg
    echo -e "Should the update_manager entry added to your moonraker.conf?\n"
    echo -e "\t\e[34mNOTE:\e[0m\n\tThis will only work if your moonraker.conf"
    echo -e "\tshares the same path as your Sonar.conf!!!\n"
    echo -e "If you want/have to do that manually,\nplease see 'resources/moonraker_update.txt'"
    echo -e "Copy the content in your moonraker.conf\n"
}

goodbye_msg() {
    header_msg
    echo -e "\t\e[32mSuccessful\e[0m configuration."
    echo -e "\tIn order to install Sonar, please run:\n"
    echo -e "\t\t\e[32msudo make install\e[0m\n"
    echo -e "Goodbye ..."
}

### funcs
continue_config() {
    local reply
    while true; do
        read -erp "Continue? [Y/n]: " -i "Y" reply
        case "${reply}" in
            [Yy]* )
                break
            ;;
            [Nn]* )
                abort_msg
                exit 0
            ;;
            * )
                echo -e "\e[31mERROR: Please type Y or N !\e[0m"
            ;;
        esac
    done
}

check_config_file() {
    local reply
    if [[ -f "${SR_CONFIG_CONFIGFILE}" ]]; then
        check_config_file_msg
        while true; do
            read -erp "Overwrite? [y/N]: " -i "N" reply
            case "${reply}" in
                [Yy]* )
                    rm -f tools/.config
                    break
                ;;
                [Nn]* )
                    abort_msg
                    exit 0
                ;;
                * )
                    echo -e "\e[31mERROR:\e[0m Please type Y or N !"
                ;;
            esac
        done
        return 0
    fi
    return 0
}

create_config_header() {
    echo -e "BASE_USER=\"${SR_CONFIG_USER}\"" >> "${SR_CONFIG_CONFIGFILE}"
}

specify_config_path() {
    local reply
    config_path_msg
    default_path_msg
    read -erp "Please enter path: " reply
    if [[ -z "${reply}" ]]; then
        echo -e "SONAR_CONFIG_PATH=\"${SR_CONFIG_CONFIGPATH}\"" >> \
        "${SR_CONFIG_CONFIGFILE}"
        return 0
    fi
    if [[ -n "${reply}" ]]; then
        echo -e "SONAR_CONFIG_PATH=\"${reply}\"" >> "${SR_CONFIG_CONFIGFILE}"
        SR_MOONRAKER_CONFIG_PATH="${reply}/moonraker.conf"
        return 0
    fi
}

specify_log_path() {
    local reply
    log_path_msg
    default_path_msg
    read -erp "Please enter path: " reply
    if [[ -z "${reply}" ]]; then
        echo -e "SONAR_LOG_PATH=\"${SR_CONFIG_LOGPATH}\"" >> \
        "${SR_CONFIG_CONFIGFILE}"
        return 0
    fi
    if [[ -n "${reply}" ]]; then
        echo -e "SONAR_LOG_PATH=\"${reply}\"" >> "${SR_CONFIG_CONFIGFILE}"
        return 0
    fi
}

add_moonraker_entry() {
    local reply
    add_moonraker_entry_msg
    while true; do
        read -erp "Add update_manager entry? [Y/n]: " -i "Y" reply
        case "${reply}" in
            [yY]*)
                echo -e "SONAR_ADD_SONAR_MOONRAKER=\"1\"" >> "${SR_CONFIG_CONFIGFILE}"
                echo "SONAR_MOONRAKER_CONF_PATH=\"${SR_MOONRAKER_CONFIG_PATH}\"" \
                >> "${SR_CONFIG_CONFIGFILE}"
                break
            ;;
            [nN]*)
                echo -e "SONAR_ADD_SONAR_MOONRAKER=\"0\"" >> "${SR_CONFIG_CONFIGFILE}"
                break
            ;;
            * )
                    echo -e "\e[31mERROR:\e[0m Please type Y or N !"
            ;;
        esac
    done
}

### Main func
main() {
    # Step 1: Welcome Message
    welcome_msg
    continue_config
    # Step 2: Check for existing file
    check_config_file
    # Step 3: Create config header
    create_config_header
    # Step 4: Specify config file path.
    specify_config_path
    # Step 5: Specify log file path.
    specify_log_path
    # Step 6: Moonraker entry
    add_moonraker_entry
    # Step 7: Display finished message
    goodbye_msg
}

### MAIN
main
exit 0
