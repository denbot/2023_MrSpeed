#!/usr/bin/env bash

# This script is used to as a one-time roborio setup script for the 2023 season

# Set the WIFI_NETWORK variable to either "${1}" or "team1339" if not supplied
WIFI_NETWORK="${1:-1339_CompBot}"

## Color support
if [[ $(type tput 2>&-) ]]; then
  red=$(tput setaf 1)
  green=$(tput setaf 2)
  yellow=$(tput setaf 3)
  reset=$(tput sgr0)
fi

## Dependency Checks ##
# Test if running on a Mac
if [[ "$OSTYPE" != "darwin"* ]]; then
    >&2 echo "${red}This script is only for MacOS${reset}"
    exit 1
fi

# Test if pip3 is installed
if ! command -v pip3 &>-; then
    >&2 echo "${red}pip3 could not be found${reset}"
    exit 1
fi

# Test if python3.11 is installed
if ! command -v python3.11 &>-; then
    >&2 echo "${red}python3.11 could not be found${reset}"
    exit 1
fi

# Network connectivity test
if ! ping -c 1 google.com &>-; then
    >&2 echo "${red}No network connectivity${reset}"
    exit 1
fi

pip3 install -U robotpy[rev]

pip3 install robotpy-installer
robotpy-installer download-python
robotpy-installer download robotpy[rev]

## Switch to roborio wifi network ##
# Find Wi-Fi network interface
NETWORK_INTERFACE=$(networksetup -listallhardwareports | grep -A1 'Wi-Fi' | awk '/Device:/{ print $2}')
# Announce the change in network
>&2 echo "${yellow}############"
>&2 echo "Switching to roborio wifi network: ${WIFI_NETWORK} on interface: ${NETWORK_INTERFACE}"
>&2 echo "############${reset}"
## Switch to roborio wifi network
networksetup -setairportnetwork "${NETWORK_INTERFACE}" "${WIFI_NETWORK}"

robotpy-installer install-python
robotpy-installer install robotpy[rev]
