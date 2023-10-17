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

## disabeld SC2086 for some lines because there we want 'word splitting'

# Exit on Errors
set -Ee

# Global Vars
TITLE="Sonar - A WiFi Keepalive daemon"
[[ -n "${BASE_USER}" ]] || BASE_USER="$(whoami)"
[[ -n "${SONAR_UNATTENDED}" ]] || SONAR_UNATTENDED="0"
[[ -n "${SONAR_DEFAULT_CONF}" ]] || SONAR_DEFAULT_CONF="resources/sonar.conf"

# Message Vars
CN_OK="\e[32mOK\e[0m"
CN_SK="\e[33mSKIPPED\e[0m"

### Global Setup
### noninteractive Check
if [ "${DEBIAN_FRONTEND}" != "noninteractive" ]; then
    export DEBIAN_FRONTEND=noninteractive
fi

### Check non-root
if [[ ${UID} != '0' ]]; then
    echo -e "\n\tYOU NEED TO RUN INSTALLER AS ROOT!"
    echo -e "\tPlease try 'sudo make install'\nExiting..."
    exit 1
fi

### Global functions

### Messages
### Welcome Message
welcome_msg() {
    echo -e "${TITLE}\n"
    echo -e "\t\e[34mAhoi!\e[0m"
    echo -e "\tThank you for installing sonar ;)"
    echo -e "\tThis will take a while ... "
    echo -e "\tPlease reboot after installation has finished.\n"
    sleep 1
}

### Config Message
config_msg() {
    echo -e "\nConfig file not found!\n\tYOU NEED TO CREATE A CONFIGURATION!"
    echo -e "\tPlease use 'make config' first!\nExiting..."
    exit 1
}

### Goodbye Message
goodbye_msg() {
    echo -e "\nInstallation \e[32msuccessful\e[0m.\n"
    echo -e "\t\e[33mTo take changes effect, you need to reboot your machine!\e[0m\n"
}

### Installer

### General
## These two functions are reused from custompios common.sh
## Credits to guysoft!
## https://github.com/guysoft/CustomPiOS

install_cleanup_trap() {
    # kills all child processes of the current process on SIGINT or SIGTERM
    trap 'cleanup' SIGINT SIGTERM
}

cleanup() {
    # make sure that all child processed die when we die
    echo -e "Killed by user ...\r\nGoodBye ...\r"
    # shellcheck disable=2046
    [[ -n "$(jobs -pr)" ]] && kill $(jobs -pr) && sleep 5 && kill -9 $(jobs -pr)
}

err_exit() {
    if [[ "${1}" != "0" ]]; then
        echo -e "ERROR: Error ${1} occured on line ${2}"
        echo -e "ERROR: Stopping $(basename "$0")."
        echo -e "Goodbye..."
    fi
    # shellcheck disable=2046
    [[ -n "$(jobs -pr)" ]] && kill $(jobs -pr) && sleep 5 && kill -9 $(jobs -pr)
    exit 1
}

### Init ERR Trap
trap 'err_exit $? $LINENO' ERR

### Import config
import_config() {
    ## Source config if present
    if [[ -s tools/.config ]]; then
        # shellcheck disable=SC1091
        . tools/.config
        return 0
    else
        config_msg
        return 0
    fi
}

create_filestructure() {
    for i in "${SONAR_CONFIG_PATH}" "${SONAR_LOG_PATH%/*.*}"; do
        if [[ ! -d "${i}" ]] && [[ ! -L "${i}" ]]; then
            sudo -u "${BASE_USER}" \
            mkdir -p "${i}"
        fi
    done
}

install_packages() {
    ### sonar Dependencies
    PKGLIST="git crudini iputils-ping"

    echo -e "Running apt update first ..."
    ### Run apt update
    sudo apt-get -q --allow-releaseinfo-change update

    echo -e "Installing 'sonar' Dependencies ..."
    # shellcheck disable=SC2086
    # disable because we want 'wordsplitting'
    sudo apt-get install -q -y --no-install-recommends ${PKGLIST}

    echo -e "Installing 'sonar' Dependencies ... [${CN_OK}]"
}

install_sonar() {
    local bin_path config sonar_bin
    bin_path="/usr/local/bin"
    config="${SONAR_CONFIG_PATH}/sonar.conf"
    sonar_bin="/home/${BASE_USER}/sonar/sonar"
    # Link sonar to $PATH
    echo -en "Linking sonar ...\r"
    # Remove if exist!
    if [[ -f /usr/local/bin/sonar ]]; then
        rm -f /usr/local/bin/sonar
    fi
    sudo ln -sf "${sonar_bin}" "${bin_path}" > /dev/null
    echo -e "Linking sonar ... [${CN_OK}]\r"
    # Install base line config
    # Make sure not overwrite existing!
    if [[ -f "${config}" ]]; then
        echo -e "Found existing 'sonar.conf' in ${SONAR_CONFIG_PATH}"
        echo -e "Copying sonar.conf ... [${CN_SK}]"
    fi

    if [[ ! -f "${config}" ]]; then
        echo -en "Copying sonar.conf ...\r"
        sudo -u "${BASE_USER}" \
        cp -f "${SONAR_DEFAULT_CONF}" "${config}" &> /dev/null
        echo -e "Copying sonar.conf ... [${CN_OK}]\r"
    fi
    return 0
}

install_service_file() {
    local servicefile systemd_dir
    servicefile="${PWD}/resources/sonar.service"
    systemd_dir="/etc/systemd/system"
    echo -en "Install sonar.service file ...\r"
    # Install Service file
    cp -f "${servicefile}" "${systemd_dir}"
}

install_logrotate() {
    local logrotatefile logpath
    logrotatefile="resources/logrotate_sonar"
    logpath="${SONAR_LOG_PATH}/sonar.log"
    # generate pseudo link
    ln -sf /var/log/sonar.log "${logpath}"
    # install logrotate
    echo -en "Install logrotate file ...\r"
    cp -rf "${logrotatefile}" /etc/logrotate.d/sonar
    echo -e "Install logrotate file ... [${CN_OK}]\r"
}

add_update_entry() {
    local moonraker_conf
    moonraker_conf="${SONAR_CONFIG_PATH}/moonraker.conf"
    moonraker_update="${PWD}/resources/moonraker_update.txt"
    echo -en "Adding Sonar Update Manager entry to moonraker.conf ...\r"
    if [[ -f "${moonraker_conf}" ]]; then
        if [[ "$(grep -c "sonar" "${moonraker_conf}")" != "0" ]]; then
            echo -e "Update Manager entry already exists moonraker.conf ... [${CN_SK}]"
            return 0
        fi
        # make sure no file exist
        if [[ -f "/tmp/moonraker.conf" ]]; then
            sudo rm -f /tmp/moonraker.conf
        fi
        echo -e "Adding [update_manager] entry ..."
        sudo -u "${BASE_USER}" \
        cp "${moonraker_conf}" "${moonraker_conf}.backup" &&
        cat "${moonraker_conf}" "${moonraker_update}" > /tmp/moonraker.conf &&
        cp -rf /tmp/moonraker.conf "${moonraker_conf}"
        if [[ "${SONAR_UNATTENDED}" = "1" ]]; then
            sudo rm -f "${moonraker_conf}.backup"
        fi
        echo -e "Adding Sonar Update Manager entry to moonraker.conf ... [${CN_OK}]"
    else
        echo -e "moonraker.conf is missing ... [${CN_SK}]"
    fi
}

## enable service
enable_service() {
    echo -en "Enable sonar.service on boot ...\r"
    sudo systemctl enable sonar.service &> /dev/null
    echo -e "Enable sonar.service on boot ... [${CN_OK}]\r"
}

## start systemd service
start_service() {
        sudo systemctl daemon-reload &> /dev/null
        sudo systemctl start sonar.service &> /dev/null
}

## ask reboot
ask_reboot() {
    local reply
    while true; do
        read -erp "Reboot NOW? [y/N]: " -i "N" reply
        case "${reply}" in
            [yY]*)
                echo -e "Going to reboot in 5 seconds!"
                sleep 5
                reboot
            ;;
            [nN]*)
                echo -e "\n\e[31mNot to reboot may cause issues!"
                echo -e "Reboot as soon as possible!\e[0m\n"
                echo -e "Goodbye ..."
                break
            ;;
            * )
                    echo -e "\e[31mERROR:\e[0m Please choose Y or N !"
            ;;
        esac
    done
}

## Main func
main() {
    ## Initialize traps
    install_cleanup_trap

    ## Welcome message
    welcome_msg

    ## Step 1: import .config file
    if [[ "${SONAR_UNATTENDED}" = "0" ]]; then
        import_config
    fi

    ## Make sure folders exist
    create_filestructure

    ## Step 2: Install dependencies
    install_packages

    ## Step 3: Install sonar
    install_sonar

    ## Step 4: Install service File
    install_service_file

    ## Step 5: Enable service
    if [[ -f /etc/systemd/system/sonar.service ]] &&
    [[ "${SONAR_UNATTENDED}" = "0" ]]; then
        enable_service
    fi
    ## If unattended skip start service
    if [[ "${SONAR_UNATTENDED}" = "0" ]]; then
        start_service
    fi

    ## Step 6: Install logrotate file
    install_logrotate

    ## Step 7: Add moonraker update_manager entry
    if [[ "${SONAR_UNATTENDED}" = "1" ]] ||
    [[ "${SONAR_ADD_SONAR_MOONRAKER}" = "1" ]]; then
        add_update_entry
    fi

    ## Step 8: Ask for reboot
    ## Skip if UNATTENDED
    goodbye_msg
    if [[ "${SONAR_UNATTENDED}" = "0" ]]; then
        ask_reboot
    fi
}

main
exit 0
