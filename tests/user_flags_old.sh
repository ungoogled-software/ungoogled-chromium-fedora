#!/usr/bin/env bash

# Load user flags
if [ -n "$XDG_CONFIG_HOME" ]; then
    USER_FLAGS_LOCATION="$XDG_CONFIG_HOME/chromium-flags.conf"
elif [ -n "$HOME" ]; then
    USER_FLAGS_LOCATION="$HOME/.config/chromium-flags.conf"
fi

echo "loc: $USER_FLAGS_LOCATION"

if [ -f $USER_FLAGS_LOCATION ]; then
    CHROMIUM_DISTRO_FLAGS+=`cat $USER_FLAGS_LOCATION`
fi

echo "flags: $CHROMIUM_DISTRO_FLAGS"
