#!/usr/bin/env bash

# Set the ROBOT_SSID variable to either "${1}" or "1339_CompBot" if not supplied
ROBOT_SSID="${1:-1339_CompBot}"

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

NETWORK_INTERFACE=$(networksetup -listallhardwareports | grep -A1 'Wi-Fi' | awk '/Device:/{ print $2}')

function get_current_ssid {
	networksetup -getairportnetwork "${NETWORK_INTERFACE}" | awk -F': ' '/Current Wi-Fi Network:/ {print $2}'
}

function wifi_connect {
	local WIFI_NET="${1}"
	local NET_INT="${2}"
	>&2 echo "${yellow}############"
	>&2 echo "Switching wifi network: ${WIFI_NET} on interface: ${NET_INT}"
	>&2 echo "############${reset}"
	networksetup -setairportnetwork "${NET_INT}" "${WIFI_NET}"
	until [[ $(get_current_ssid) == "${WIFI_NET}" ]]; do
	sleep 1
	done
}

function deploy {
	>&2 echo "${green}############"
	>&2 echo "Deploying code to robot"
	>&2 echo "############${reset}"
	python3 robot.py deploy
}

STARTING_NETWORK=$(get_current_ssid)

if [[ "${STARTING_NETWORK}" != "${ROBOT_SSID}" ]]; then
	wifi_connect "${ROBOT_SSID}" "${NETWORK_INTERFACE}"
	deploy
	wifi_connect "${STARTING_NETWORK}" "${NETWORK_INTERFACE}"
else
	deploy
fi
