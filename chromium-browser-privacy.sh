#!/bin/bash
#
# Copyright (c) 2011 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

# This file is obtained from https://src.fedoraproject.org/rpms/chromium/
# and modified by Akarshan Biswas <akarshanbiswas@fedoraproject.org>. All modifications are also
# licensed under 3-clause BSD license.
CHROMIUM_DISTRO_FLAGS=()

# Let the wrapped binary know that it has been run through the wrapper.
export CHROME_WRAPPER="$(readlink -f "$0")"

HERE="`dirname "$CHROME_WRAPPER"`"
export CHROME_DESKTOP="chromium-browser-privacy.desktop"
# We include some xdg utilities next to the binary, and we want to prefer them
# over the system versions when we know the system versions are very old. We
# detect whether the system xdg utilities are sufficiently new to be likely to
# work for us by looking for xdg-settings. If we find it, we leave $PATH alone,
# so that the system xdg utilities (including any distro patches) will be used.
if ! which xdg-settings &> /dev/null; then
  # Old xdg utilities. Prepend $HERE to $PATH to use ours instead.
  export PATH="$HERE:$PATH"
else
  # Use system xdg utilities. But first create mimeapps.list if it doesn't
  # exist; some systems have bugs in xdg-mime that make it fail without it.
  xdg_app_dir="${XDG_DATA_HOME:-$HOME/.local/share/applications}"
  mkdir -p "$xdg_app_dir"
  [ -f "$xdg_app_dir/mimeapps.list" ] || touch "$xdg_app_dir/mimeapps.list"
fi

# Always use our versions of ffmpeg libs.
# This also makes RPMs find the compatibly-named library symlinks.
if [[ -n "$LD_LIBRARY_PATH" ]]; then
  LD_LIBRARY_PATH="$HERE:$HERE/lib:$LD_LIBRARY_PATH"
else
  LD_LIBRARY_PATH="$HERE:$HERE/lib"
fi
export LD_LIBRARY_PATH

#On wayland pass the correct GDK_BACKEND
# In future this will be used for running chromium natively on Wayland
if [ $XDG_SESSION_TYPE == "wayland" ]; then
export GDK_BACKEND=x11
fi


# Sanitize std{in,out,err} because they'll be shared with untrusted child
# processes (http://crbug.com/376567).
exec < /dev/null
exec > >(exec cat)
exec 2> >(exec cat >&2)


CHROMIUM_DISTRO_FLAGS+=" --enable-plugins \
                         --enable-extensions \
                         --enable-user-scripts \
                         --enable-features=WebRTCPipeWireCapturer \
                         --enable-printing \
                         --disable-sync \
                         --disable-background-networking \
                         --force-local-ntp \
                         --disallow-signin"

exec -a "$0" "@@CHROMIUMDIR@@/$(basename "$0" | sed 's/\.sh$//')" $CHROMIUM_DISTRO_FLAGS "$@"
