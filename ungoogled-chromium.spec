%global obs 0
%global ninja_verbose 0
%global ccache 0

%define _lto_cflags %{nil}

# set default fuzz=2 for patch
%global _default_patch_fuzz 2

# enable|disable system build flags
%global system_build_flags 0

# disable the package notes info on f36
# workaround for linking issue
%if 0%{?fedora} == 36
%undefine _package_note_file
%endif

# set default numjobs for the koji build
%ifarch aarch64
%global numjobs 8
%else
%global numjobs %{_smp_build_ncpus}
%endif

# This flag is so I can build things very fast on a giant system.
# Enabling this in koji causes aarch64 builds to timeout indefinitely.
%global use_all_cpus 0

%if %{use_all_cpus}
%global numjobs %{_smp_build_ncpus}
%endif
 
# official builds have less debugging and go faster... but we have to shut some things off.
%global official_build 1

# enable|disble bootstrap
# ungoogled-chromium: enable bootstrap
%global bootstrap 1

# Fancy build status, so we at least know, where we are..
# %1 where
# %2 what
%if %{ninja_verbose}
%global build_target() \
	export NINJA_STATUS="[%2:%f/%t] " ; \
	ninja -j %{numjobs} -C '%1' -vvv '%2'
%else
%global build_target() \
	export NINJA_STATUS="[%2:%f/%t] " ; \
	ninja -j %{numjobs} -C '%1' '%2'
%endif

# Define __python2 and __python3 for OBS
%if %{obs}
%global __python2 /usr/bin/python2
%global __python3 /usr/bin/python3
%endif

# ungoogled-chromium: enable|disable PGO
%if 0%{?fedora} >= 38
%global use_pgo 1
%else
%global use_pgo 0
%endif

# set nodejs_version
%global nodejs_version v19.8.1

# set version for devtoolset and gcc-toolset
%global dts_version 12

# set name for toolset
%global toolset gcc-toolset

%global chromium_pybin %{__python3}

# We'd like to always have this on...
%global use_vaapi 1
%global use_v4l2_codec 0

# enable v4l2 and disable vaapi for aarch64 platform
%ifarch aarch64
%if 0%{?fedora} >= 36
%global use_vaapi 0
%global use_v4l2_codec 1
%endif
%endif

%global build_clear_key_cdm 0

# gn/ninja output folder
%global builddir out/Release

# Debuginfo packages aren't very useful here. If you need to debug
# you should do a proper debug build (not implemented in this spec yet)
%global debug_package %{nil}

# A switch to disable domain substitution for development purposes.
%bcond_without domain_substitution

# %%{nil} for Stable; -beta for Beta; -dev for Devel
# dash in -beta and -dev is intentional !
%global chromium_channel %{nil}
%global chromium_menu_name Ungoogled Chromium
%global chromium_browser_channel ungoogled-chromium%{chromium_channel}
%global chromium_path %{_libdir}/ungoogled-chromium%{chromium_channel}

# We don't want any libs in these directories to generate Provides
# Requires is trickier.

# To generate this list, go into %%{buildroot}%%{chromium_path} and run
# for i in `find . -name "*.so" | sort`; do NAME=`basename -s .so $i`; printf "$NAME|"; done
# for RHEL7, append libfontconfig to the end
# make sure there is not a trailing | at the end of the list
# We always filter provides. We only filter Requires when building shared.
%global __provides_exclude_from ^(%{chromium_path}/.*\\.so|%{chromium_path}/.*\\.so.*)$
%global __requires_exclude ^(%{chromium_path}/.*\\.so|%{chromium_path}/.*\\.so.*)$

# enable clang by default
%global clang 1

# set correct toolchain
%if %{clang}
%global toolchain clang
%else
%global toolchain gcc
%endif

# enable system brotli
%global bundlebrotli 0

# Chromium's fork of ICU is now something we can't unbundle.
# This is left here to ease the change if that ever switches.
%global bundleicu 1

%global bundlere2 1

# The libxml_utils code depends on the specific bundled libxml checkout
# which is not compatible with the current code in the Fedora package as of
# 2017-06-08.
%global bundlelibxml 1

# Fedora's Python 2 stack is being removed, we use the bundled Python libraries
# This can be revisited once we upgrade to Python 3
%global bundlepylibs 0

# RHEL 7.9 dropped minizip.
# It exists everywhere else though.
%global bundleminizip 0

# enable qt backend
%global use_qt 1

# enable gtk3 by default
%global gtk3 1

# Chromium really wants to use its bundled harfbuzz. Sigh.
%global bundleharfbuzz 1
%global bundleopus 0
%global bundlelibusbx 0
%global bundlelibwebp 0
%global bundlelibpng 0
%global bundlelibjpeg 0
%global bundlelibdrm 0
%global bundlefontconfig 0
%global bundleffmpegfree 0
# f36 has old libaom
%if 0%{?fedora} == 36
%global bundlelibaom 1
%else
%global bundlelibaom 0
%endif
# system freetype on fedora > 36
%if 0%{?fedora} > 36
%global bundlefreetype 0
%else
%global bundlefreetype 1
%endif

### Google API keys (see http://www.chromium.org/developers/how-tos/api-keys)
### Note: These are for Fedora use ONLY.
### For your own distribution, please get your own set of keys.
### http://lists.debian.org/debian-legal/2013/11/msg00006.html
%global api_key %nil
%global default_client_id %nil
%global default_client_secret %nil
%global chromoting_client_id %nil

#Build with debugging symbols
%global debug_pkg 0

Name:	ungoogled-chromium
Version: 112.0.5615.165
Release: 2%{?dist}
Summary: A lightweight approach to removing Google web service dependency
Url: https://github.com/Eloston/ungoogled-chromium
License: BSD-3-Clause AND LGPL-2.1-or-later AND Apache-2.0 AND IJG AND MIT AND GPL-2.0-or-later AND ISC AND OpenSSL AND (MPL-1.1 OR GPL-2.0-only OR LGPL-2.0-only)

### Chromium Fedora Patches ###
#ungoogled-chromium: this patch is includded in the ungoogled-chromium patches
#Patch0: chromium-70.0.3538.67-sandbox-pie.patch

# Use /etc/chromium for initial_prefs
Patch1: chromium-91.0.4472.77-initial_prefs-etc-path.patch

# Use gn system files
Patch2: chromium-107.0.5304.110-gn-system.patch

# Do not mangle zlib
Patch5: chromium-77.0.3865.75-no-zlib-mangle.patch
# Try to load widevine from other places
Patch8: chromium-108-widevine-other-locations.patch

# Do not download proprietary widevine module in the background (thanks Debian)
Patch9: chromium-99.0.4844.51-widevine-no-download.patch

# Tell bootstrap.py to always use the version of Python we specify
Patch11: chromium-93.0.4577.63-py3-bootstrap.patch

# debian patch, disable font-test 
Patch20: chromium-disable-font-tests.patch

# https://gitweb.gentoo.org/repo/gentoo.git/tree/www-client/chromium/files/chromium-unbundle-zlib.patch
Patch52: chromium-81.0.4044.92-unbundle-zlib.patch

# missing limits.h, error: no member named 'numeric_limits' in namespace 'std'
Patch53: chromium-110-limits.patch

# ../../third_party/perfetto/include/perfetto/base/task_runner.h:48:55: error: 'uint32_t' has not been declared
Patch56: chromium-96.0.4664.45-missing-cstdint-header.patch

# Missing <cstring> (thanks c++17)
Patch57: chromium-96.0.4664.45-missing-cstring.patch

# Fix headers to look for system paths when we are using system minizip
Patch61: chromium-109-system-minizip-header-fix.patch

# Fix issue where closure_compiler thinks java is only allowed in android builds
# https://bugs.chromium.org/p/chromium/issues/detail?id=1192875
Patch65: chromium-91.0.4472.77-java-only-allowed-in-android-builds.patch

# Update rjsmin to 1.2.0
Patch69: chromium-103.0.5060.53-update-rjsmin-to-1.2.0.patch

# Update six to 1.16.0
Patch70: chromium-105.0.5195.52-python-six-1.16.0.patch

# Disable tests on remoting build
Patch82: chromium-98.0.4758.102-remoting-no-tests.patch

# patch for using system brotli
Patch89: chromium-108-system-brotli.patch

# disable GlobalMediaControlsCastStartStop to avoid crash
# when using the address bar media player button
Patch90: chromium-109-disable-GlobalMediaControlsCastStartStop.patch

# patch for using system opus
Patch91: chromium-108-system-opus.patch

# fix prefers-color-scheme
Patch92: chromium-110-gtktheme.patch

# system ffmpeg
Patch114: chromium-107-ffmpeg-duration.patch
Patch115: chromium-107-proprietary-codecs.patch
# drop av_stream_get_first_dts from internal ffmpeg
Patch116: chromium-108-ffmpeg-first_dts.patch
# revert new-channel-layout-api on f36, old ffmpeg-free
Patch117: chromium-108-ffmpeg-revert-new-channel-layout-api.patch

# gcc13
Patch122: chromium-109-gcc13.patch

# Patches by Stephan Hartmann, https://github.com/stha09/chromium-patches
Patch130: chromium-103-VirtualCursor-std-layout.patch

# Pagesize > 4kb
Patch146: chromium-110-LargerThan4k.patch

# VAAPI
# Upstream turned VAAPI on in Linux in 86
Patch202: chromium-104.0.5112.101-enable-hardware-accelerated-mjpeg.patch
Patch203: chromium-112-check-passthrough-command-decoder.patch
Patch204: chromium-112-invert_of_GLImageNativePixmap_NativePixmapEGLBinding.patch
Patch205: chromium-86.0.4240.75-fix-vaapi-on-intel.patch
Patch206: chromium-112-ozone-wayland-vaapi-support.patch
Patch207: chromium-112-enable-vaapi-ozone-wayland.patch

# Apply these patches to work around EPEL8 issues
Patch300: chromium-99.0.4844.51-rhel8-force-disable-use_gnome_keyring.patch

# RPM Fusion patches [free/chromium-freeworld]:
Patch503:       chromium-manpage.patch

# RPM Fusion patches [free/chromium-browser-privacy]:
Patch600:       chromium-default-user-data-dir.patch

# ungoogled-chromium platform patches
Patch700:   chromium-94.0.4606.61-ungoogled-pref-fix.patch

# Use chromium-latest.py to generate clean tarball from released build tarballs, found here:
# http://build.chromium.org/buildbot/official/
# For Chromium Fedora use chromium-latest.py --stable --ffmpegclean --ffmpegarm
# If you want to include the ffmpeg arm sources append the --ffmpegarm switch
# https://commondatastorage.googleapis.com/chromium-browser-official/chromium-%%{version}.tar.xz
%if %{obs}
Source0: https://commondatastorage.googleapis.com/chromium-browser-official/chromium-%{version}.tar.xz
%else
Source0: chromium-%{version}-clean.tar.xz
%endif
Source2: ungoogled-chromium.conf
Source3: ungoogled-chromium.sh
Source4: %{chromium_browser_channel}.desktop
# Also, only used if you want to reproduce the clean tarball.
Source5: clean_ffmpeg.sh
Source6: chromium-latest.py
Source7: get_free_ffmpeg_source_files.py
# Get the names of all tests (gtests) for Linux
# Usage: get_linux_tests_name.py chromium-%%{version} --spec
Source8: get_linux_tests_names.py
# GNOME stuff
Source9: ungoogled-chromium.xml
Source13: master_preferences

# Add our own appdata file.
Source22:       ungoogled-chromium.appdata.xml

# ungoogled-chromium source
%global ungoogled_chromium_revision 112.0.5615.165-1
Source300:      https://github.com/Eloston/ungoogled-chromium/archive/%{ungoogled_chromium_revision}/ungoogled-chromium-%{ungoogled_chromium_revision}.tar.gz

%if %{clang}
BuildRequires: clang
BuildRequires: clang-tools-extra
BuildRequires: llvm
BuildRequires: lld
# needs for libatomic
%else
%if 0%{?fedora}
BuildRequires: gcc-c++
BuildRequires: gcc
BuildRequires: binutils
%endif
%endif

# build with system ffmpeg-free
%if ! %{bundleffmpegfree}
BuildRequires: pkgconfig(libavcodec)
BuildRequires: pkgconfig(libavfilter)
BuildRequires: pkgconfig(libavformat)
BuildRequires: pkgconfig(libavutil)
%endif

# build with system libaom
%if ! %{bundlelibaom}
BuildRequires: libaom-devel
%endif

BuildRequires:	alsa-lib-devel
BuildRequires:	atk-devel
BuildRequires:	bison
BuildRequires:	cups-devel
BuildRequires:	dbus-devel
BuildRequires:	desktop-file-utils
BuildRequires:	expat-devel
BuildRequires:	flex
BuildRequires:	fontconfig-devel
BuildRequires:	glib2-devel
BuildRequires:	glibc-devel
BuildRequires:	gperf

%if %{use_qt}
BuildRequires: pkgconfig(Qt5Core)
BuildRequires: pkgconfig(Qt5Widgets)
%endif

%if ! %{bundleharfbuzz}
BuildRequires:	harfbuzz-devel >= 2.4.0
%endif

BuildRequires: libatomic
BuildRequires:	libcap-devel
BuildRequires:	libcurl-devel

%if ! %{bundlelibdrm}
BuildRequires:	libdrm-devel
%endif

BuildRequires:	libgcrypt-devel
BuildRequires:	libudev-devel
BuildRequires:	libuuid-devel

%if 0%{?fedora} >= 37
BuildRequires:	libusb-compat-0.1-devel
%else
BuildRequires:	libusb-devel
%endif

BuildRequires:	libutempter-devel
BuildRequires:	libXdamage-devel
BuildRequires:	libXtst-devel
BuildRequires:	xcb-proto
BuildRequires:	mesa-libgbm-devel
BuildRequires:	minizip-compat-devel
BuildRequires:	nodejs

%if ! %{bootstrap}
BuildRequires: gn
%endif

BuildRequires:	nss-devel >= 3.26
BuildRequires:	pciutils-devel
BuildRequires:	pulseaudio-libs-devel

# For screen sharing on Wayland
%if 0%{?fedora}
BuildRequires:	pkgconfig(libpipewire-0.3)
%endif

# for /usr/bin/appstream-util
BuildRequires: libappstream-glib

%if %{bootstrap}
# gn needs these
BuildRequires: libstdc++-static
%endif

# Fedora tries to use system libs whenever it can.
BuildRequires:	bzip2-devel
BuildRequires:	dbus-glib-devel
# For eu-strip
BuildRequires:	elfutils
BuildRequires:	elfutils-libelf-devel
BuildRequires:	flac-devel

%if ! %{bundlefreetype}
BuildRequires:	freetype-devel
%endif

# One of the python scripts invokes git to look for a hash. So helpful.
BuildRequires:	/usr/bin/git
BuildRequires:	hwdata
BuildRequires:	kernel-headers
BuildRequires:	libevent-devel
BuildRequires:	libffi-devel

%if ! %{bundleicu}
# If this is true, we're using the bundled icu.
# We'd like to use the system icu every time, but we cannot always do that.
# Not newer than 54 (at least not right now)
BuildRequires:	libicu-devel = 54.1
%endif

%if ! %{bundlelibjpeg}
# If this is true, we're using the bundled libjpeg
# which we need to do because the RHEL 7 libjpeg doesn't work for chromium anymore
BuildRequires:	libjpeg-devel
%endif

%if ! %{bundlelibpng}
# If this is true, we're using the bundled libpng
# which we need to do because the RHEL 7 libpng doesn't work right anymore
BuildRequires:	libpng-devel
%endif

BuildRequires:	libudev-devel

%if ! %{bundlelibusbx}
Requires: libusbx >= 1.0.21-0.1.git448584a
BuildRequires: libusbx-devel >= 1.0.21-0.1.git448584a
%endif

%if %{use_vaapi}
BuildRequires:	libva-devel
%endif

# We don't use libvpx anymore because Chromium loves to
# use bleeding edge revisions here that break other things
# ... so we just use the bundled libvpx.
%if ! %{bundlelibwebp}
BuildRequires:	libwebp-devel
%endif

BuildRequires:	libxslt-devel
BuildRequires:	libxshmfence-devel

# Same here, it seems.
# BuildRequires: libyuv-devel
BuildRequires:	mesa-libGL-devel

%if ! %{bundleopus}
BuildRequires:	opus-devel
%endif

BuildRequires:	perl(Switch)
BuildRequires: %{chromium_pybin}

%if %{gtk3}
BuildRequires:	pkgconfig(gtk+-3.0)
%else
BuildRequires:	pkgconfig(gtk+-2.0)
%endif

BuildRequires:	python3-devel
BuildRequires: python3-zipp
BuildRequires: python3-simplejson
BuildRequires: python3-importlib-metadata


%if ! %{bundlepylibs}
BuildRequires: python3-beautifulsoup4
BuildRequires: python3-html5lib
BuildRequires: python3-markupsafe
BuildRequires: python3-ply
BuildRequires: python3-jinja2
%endif

%if ! %{bundlere2}
Requires: re2 >= 20160401
BuildRequires: re2-devel >= 20160401
%endif

%if ! %{bundlebrotli}
BuildRequires: brotli-devel
%endif

BuildRequires: speech-dispatcher-devel
BuildRequires: yasm
BuildRequires: zlib-devel

BuildRequires:	pkgconfig(gnome-keyring-1)

# using the built from source version on aarch64
BuildRequires: ninja-build

# Yes, java is needed as well..
BuildRequires:	java-1.8.0-openjdk-headless

# There is a hardcoded check for nss 3.26 in the chromium code (crypto/nss_util.cc)
Requires: nss%{_isa} >= 3.26
Requires: nss-mdns%{_isa}

# GTK modules it expects to find for some reason.
%if %{gtk3}
Requires: libcanberra-gtk3%{_isa}
%else
Requires: libcanberra-gtk2%{_isa}
%endif

%if 0%{?fedora}
# This enables support for u2f tokens
Requires: u2f-hidraw-policy
%endif

ExclusiveArch: x86_64 aarch64

# Bundled bits (I'm sure I've missed some)
Provides: bundled(angle) = 2422
Provides: bundled(bintrees) = 1.0.1
# This is a fork of openssl.
Provides: bundled(boringssl)

%if %{bundlebrotli}
Provides: bundled(brotli) = 222564a95d9ab58865a096b8d9f7324ea5f2e03e
%endif

Provides: bundled(bspatch)
Provides: bundled(cacheinvalidation) = 20150720
Provides: bundled(colorama) = 799604a104
Provides: bundled(crashpad)
Provides: bundled(dmg_fp)
Provides: bundled(expat) = 2.2.0
Provides: bundled(fdmlibm) = 5.3

# Don't get too excited. MPEG and other legally problematic stuff is stripped out.
%if %{bundleffmpegfree}
Provides: bundled(ffmpeg) = 5.1.2
%endif

%if %{bundlelibaom}
Provides: bundled(libaom)
%endif

Provides: bundled(fips181) = 2.2.3

%if %{bundlefontconfig}
Provides: bundled(fontconfig) = 2.12.6
%endif

%if %{bundlefreetype}
Provides: bundled(freetype) = 2.11.0git
%endif

Provides: bundled(gperftools) = svn144

%if %{bundleharfbuzz}
Provides: bundled(harfbuzz) = 2.4.0
%endif

Provides: bundled(hunspell) = 1.6.0
Provides: bundled(iccjpeg)

%if %{bundleicu}
Provides: bundled(icu) = 58.1
%endif

Provides: bundled(kitchensink) = 1
Provides: bundled(leveldb) = 1.20
Provides: bundled(libaddressinput) = 0

%if %{bundlelibdrm}
Provides: bundled(libdrm) = 2.4.85
%endif

Provides: bundled(libevent) = 1.4.15
Provides: bundled(libjingle) = 9564

%if %{bundlelibjpeg}
Provides: bundled(libjpeg-turbo) = 1.4.90
%endif

Provides: bundled(libphonenumber) = a4da30df63a097d67e3c429ead6790ad91d36cf4

%if %{bundlelibpng}
Provides: bundled(libpng) = 1.6.22
%endif

Provides: bundled(libsrtp) = 2cbd85085037dc7bf2eda48d4cf62e2829056e2d

%if %{bundlelibusbx}
Provides: bundled(libusbx) = 1.0.17
%endif

Provides: bundled(libvpx) = 1.6.0

%if %{bundlelibwebp}
Provides: bundled(libwebp) = 0.6.0
%endif

%if %{bundlelibxml}
# Well, it's actually newer than 2.9.4 and has code in it that has been reverted upstream... but eh.
Provides: bundled(libxml) = 2.9.4
%endif

Provides: bundled(libXNVCtrl) = 302.17
Provides: bundled(libyuv) = 1651
Provides: bundled(lzma) = 15.14
Provides: bundled(libudis86) = 1.7.1
Provides: bundled(mesa) = 9.0.3
Provides: bundled(NSBezierPath) = 1.0
Provides: bundled(mozc)

%if %{bundleopus}
Provides: bundled(opus) = 1.1.3
%endif

Provides: bundled(ots) = 8d70cffebbfa58f67a5c3ed0e9bc84dccdbc5bc0
Provides: bundled(protobuf) = 3.0.0.beta.3
Provides: bundled(qcms) = 4

%if %{bundlere2}
Provides: bundled(re2)
%endif

Provides: bundled(sfntly) = 04740d2600193b14aa3ef24cd9fbb3d5996b9f77
Provides: bundled(skia)
Provides: bundled(SMHasher) = 0
Provides: bundled(snappy) = 1.1.4-head
Provides: bundled(speech-dispatcher) = 0.7.1
Provides: bundled(sqlite) = 3.17patched
Provides: bundled(superfasthash) = 0
Provides: bundled(talloc) = 2.0.1
Provides: bundled(usrsctp) = 0
Provides: bundled(v8) = 5.9.211.31
Provides: bundled(webrtc) = 90usrsctp
Provides: bundled(woff2) = 445f541996fe8376f3976d35692fd2b9a6eedf2d
Provides: bundled(xdg-mime)
Provides: bundled(xdg-user-dirs)
# Provides: bundled(zlib) = 1.2.11

# For selinux scriptlet
Requires(post): /usr/sbin/semanage
Requires(post): /usr/sbin/restorecon

%description
%{name} is a distribution of ungoogled-chromium.

ungoogled-chromium is Chromium, sans integration with Google. It also features
some tweaks to enhance privacy, control, and transparency (almost all of which
require manual activation or enabling).

ungoogled-chromium retains the default Chromium experience as closely as
possible. Unlike other Chromium forks that have their own visions of a web
browser, ungoogled-chromium is essentially a drop-in replacement for Chromium.

# Chromium needs an explicit Requires: minizip-compat
Requires: minizip-compat%{_isa}

############################################PREP###########################################################
%prep
%setup -q -T -n ungoogled-chromium-%{ungoogled_chromium_revision} -b 300
%setup -q -n chromium-%{version}

%global ungoogled_chromium_root %{_builddir}/ungoogled-chromium-%{ungoogled_chromium_revision}

%if %{obs}
(
    cd ..
    for i in chromium-%{version}.tar.xz chromium-latest.py clean_ffmpeg.sh get_free_ffmpeg_source_files.py
    do
        j=../SOURCES/$i
        chmod +x $j
        ln -s $j $i
    done
    printf 'md5  %s\n' "$(md5sum chromium-%{version}.tar.xz)" > chromium-%{version}.tar.xz.hashes
    ./chromium-latest.py --version %{version} --ffmpegclean --ffmpegarm --prep
    rm -f *.tar.xz* *.sh *.py
)
%endif

### Chromium Fedora Patches ###
#ungoogled-chromium: this patch is included in the ungoogled-chromium patches
#%patch -P0 -p1 -b .sandboxpie
%patch -P1 -p1 -b .etc
%patch -P2 -p1 -b .gnsystem
%patch -P5 -p1 -b .nozlibmangle
%patch -P8 -p1 -b .widevine-other-locations
%patch -P9 -p1 -b .widevine-no-download
%patch -P11 -p1 -b .py3

%patch -P20 -p1 -b .disable-font-test

%if 0%{?fedora}
%patch -P52 -p1 -b .unbundle-zlib
%endif

%patch -P53 -p1 -b .limits-header
%patch -P56 -p1 -b .missing-cstdint
%patch -P57 -p1 -b .missing-cstring

%if ! %{bundleminizip}
%patch -P61 -p1 -b .system-minizip
%endif

%patch -P65 -p1 -b .java-only-allowed
%patch -P69 -p1 -b .update-rjsmin-to-1.2.0
%patch -P70 -p1 -b .update-six-to-1.16.0
%patch -P82 -p1 -b .remoting-no-tests

%if ! %{bundlebrotli}
%patch -P89 -p1 -b .system-brotli
%endif

%patch -P90 -p1 -b .disable-GlobalMediaControlsCastStartStop

%if ! %{bundleopus}
%patch -P91 -p1 -b .system-opus
%endif

%patch -P92 -p1 -b .gtk-prefers-color-scheme

%if ! %{bundleffmpegfree}
%patch -P114 -p1 -b .system-ffmppeg
%patch -P115 -p1 -b .prop-codecs
%patch -P116 -p1 -b .first_dts
%if 0%{?fedora} == 36
%patch -P117 -p1 -b .revert-new-channel-layout-api
%endif
%endif

%patch -P130 -p1 -b .VirtualCursor-std-layout

%patch -P146 -p1 -b .LargerThan4k

%patch -P122 -p1 -b .gcc13

# Feature specific patches
%if %{use_vaapi}
%patch -P202 -p1 -b .accel-mjpeg
%patch -P203 -p1 -R -b .revert
%patch -P204 -p1 -R -b .revert
%patch -P205 -p1 -b .vaapi-intel-fix
%patch -P206 -p1 -b .wayland-vaapi
%patch -P207 -p1 -b .enable-wayland-vaapi
%endif

# Always disable gnome keyring
%patch -P300 -p1 -b .disblegnomekeyring

# RPM Fusion patches [free/chromium-freeworld]:
%patch503 -p1 -b .manpage

# RPM Fusion patches [free/chromium-browser-privacy]:
%patch600 -p1 -b .default-user-dir

# ungoogled-chromium platform patches
%patch700 -p1 -b .ungoogled-pref-fix

# Change shebang in all relevant files in this directory and all subdirectories
# See `man find` for how the `-exec command {} +` syntax works
find -type f \( -iname "*.py" \) -exec sed -i '1s=^#! */usr/bin/\(python\|env python\)[23]\?=#!%{__python3}=' {} +


mkdir -p third_party/node/linux/node-linux-x64/bin
ln -s %{_bindir}/node third_party/node/linux/node-linux-x64/bin/node

# Get rid of the pre-built eu-strip binary, it is x86_64 and of mysterious origin
rm -rf buildtools/third_party/eu-strip/bin/eu-strip
  
# Replace it with a symlink to the Fedora copy
ln -s %{_bindir}/eu-strip buildtools/third_party/eu-strip/bin/eu-strip

%if %{bundlelibusbx}
# no hackity hack hack
%else
# hackity hack hack
rm -rf third_party/libusb/src/libusb/libusb.h
# we _shouldn't need to do this, but it looks like we do.
cp -a %{_includedir}/libusb-1.0/libusb.h third_party/libusb/src/libusb/libusb.h
%endif

# Hard code extra version
sed -i 's/getenv("CHROME_VERSION_EXTRA")/"Ungoogled Chromium"/' chrome/common/channel_info_posix.cc

# Fix hardcoded path in remoting code
sed -i 's|/opt/google/chrome-remote-desktop|%{crd_path}|g' remoting/host/setup/daemon_controller_delegate_linux.cc

# reduce debuginfos
sed -i 's|-g2|-g0|g' build/config/compiler/BUILD.gn

# change moc to moc-qt5 for fedora
sed -i 's|moc|moc-qt5|g' ui/qt/moc_wrapper.py

%build
# utf8 issue on epel7, Internal parsing error 'ascii' codec can't
# decode byte 0xe2 in position 474: ordinal not in range(128)
export LANG=en_US.UTF-8

# reduce warnings
%if %{clang}
FLAGS=' -Wno-deprecated-declarations -Wno-unknown-warning-option -Wno-unused-command-line-argument'
FLAGS+=' -Wno-unused-but-set-variable -Wno-unused-result -Wno-unused-function -Wno-unused-variable'
FLAGS+=' -Wno-unused-const-variable -Wno-unneeded-internal-declaration'
%endif

%if %{system_build_flags}
CFLAGS=${CFLAGS/-g }
CFLAGS=${CFLAGS/-fexceptions}
CFLAGS=${CFLAGS/-Wp,-D_GLIBCXX_ASSERTIONS}
CFLAGS=${CFLAGS/-fcf-protection}
CFLAGS=${CFLAGS/-fstack-clash-protection}
CFLAGS="$CFLAGS $FLAGS"
CXXFLAGS="$CFLAGS"
%else
# override system build flags
CFLAGS="$FLAGS"
CXXFLAGS="$FLAGS"
%endif

%if %{clang}
export CC=clang
export CXX=clang++
export AR=llvm-ar
export NM=llvm-nm
export READELF=llvm-readelf
%else
export CC=gcc
export CXX=g++ 
export AR=ar
export NM=nm
export READELF=readelf
%endif
export CFLAGS
export CXXFLAGS

%if %{ccache}
export CCACHE_CPP2=yes
export CCACHE_SLOPPINESS=time_macros
%endif

# Core defines are flags that are true for both the browser and headless.
CHROMIUM_CORE_GN_DEFINES=""
# using system toolchain
CHROMIUM_CORE_GN_DEFINES+=' custom_toolchain="//build/toolchain/linux/unbundle:default"'
CHROMIUM_CORE_GN_DEFINES+=' host_toolchain="//build/toolchain/linux/unbundle:default"'
CHROMIUM_CORE_GN_DEFINES+=' is_debug=false dcheck_always_on=false dcheck_is_configurable=false'
CHROMIUM_CORE_GN_DEFINES+=' use_goma=false'
CHROMIUM_CORE_GN_DEFINES+=' enable_nacl=false'
CHROMIUM_CORE_GN_DEFINES+=' system_libdir="%{_lib}"'

%if %{official_build}
CHROMIUM_CORE_GN_DEFINES+=' is_official_build=true use_thin_lto=false is_cfi=false chrome_pgo_phase=0 use_debug_fission=true'
sed -i 's|OFFICIAL_BUILD|GOOGLE_CHROME_BUILD|g' tools/generate_shim_headers/generate_shim_headers.py
%endif

CHROMIUM_CORE_GN_DEFINES+=' google_api_key="%{api_key}"'

CHROMIUM_CORE_GN_DEFINES+=' google_default_client_id="%{default_client_id}"'
CHROMIUM_CORE_GN_DEFINES+=' google_default_client_secret="%{default_client_secret}"'

%if %{clang}
CHROMIUM_CORE_GN_DEFINES+=' is_clang=true'
CHROMIUM_CORE_GN_DEFINES+=' clang_base_path="%{_prefix}"'
CHROMIUM_CORE_GN_DEFINES+=' clang_use_chrome_plugins=false'
CHROMIUM_CORE_GN_DEFINES+=' use_lld=true'
%else
CHROMIUM_CORE_GN_DEFINES+=' is_clang=false'
CHROMIUM_CORE_GN_DEFINES+=' use_lld=false'
%endif

CHROMIUM_CORE_GN_DEFINES+=' use_sysroot=false disable_fieldtrial_testing_config=true rtc_enable_symbol_export=true'

CHROMIUM_CORE_GN_DEFINES+=' use_gold=false'

%ifarch aarch64
CHROMIUM_CORE_GN_DEFINES+=' target_cpu="arm64"'
%endif

CHROMIUM_CORE_GN_DEFINES+=' icu_use_data_file=true'
CHROMIUM_CORE_GN_DEFINES+=' target_os="linux"'
CHROMIUM_CORE_GN_DEFINES+=' current_os="linux"'
CHROMIUM_CORE_GN_DEFINES+=' treat_warnings_as_errors=false'
CHROMIUM_CORE_GN_DEFINES+=' use_custom_libcxx=false'
CHROMIUM_CORE_GN_DEFINES+=' enable_iterator_debugging=false'
CHROMIUM_CORE_GN_DEFINES+=' enable_vr=false'
CHROMIUM_CORE_GN_DEFINES+=' build_dawn_tests=false enable_perfetto_unittests=false'
CHROMIUM_CORE_GN_DEFINES+=' disable_fieldtrial_testing_config=true'
CHROMIUM_CORE_GN_DEFINES+=' blink_symbol_level=0 symbol_level=0 v8_symbol_level=0'
CHROMIUM_CORE_GN_DEFINES+=' blink_enable_generated_code_formatting=false'
export CHROMIUM_CORE_GN_DEFINES

# browser gn defines
CHROMIUM_BROWSER_GN_DEFINES=""

# if systemwide ffmpeg free is used, the proprietary codecs can be set to true to load the codecs from ffmpeg-free
# the codecs computation is passed to ffmpeg-free in this case
%if ! %{bundleffmpegfree}
CHROMIUM_BROWSER_GN_DEFINES+=' ffmpeg_branding="Chrome" proprietary_codecs=true is_component_ffmpeg=true enable_ffmpeg_video_decoders=true media_use_ffmpeg=true'
%else
CHROMIUM_BROWSER_GN_DEFINES+=' ffmpeg_branding="Ungoogled Chromium" proprietary_codecs=false is_component_ffmpeg=false enable_ffmpeg_video_decoders=false media_use_ffmpeg=true'
%endif
CHROMIUM_BROWSER_GN_DEFINES+=' media_use_openh264=false'
CHROMIUM_BROWSER_GN_DEFINES+=' rtc_use_h264=false'
CHROMIUM_BROWSER_GN_DEFINES+=' use_kerberos=true'

CHROMIUM_BROWSER_GN_DEFINES+=' use_gnome_keyring=false'

%if %{use_qt}
CHROMIUM_BROWSER_GN_DEFINES+=' use_qt=true'
%else
CHROMIUM_BROWSER_GN_DEFINES+=' use_qt=false'
%endif

%if %{ccache}
CHROMIUM_BROWSER_GN_DEFINES+=' cc_wrapper="ccache"'
%endif

CHROMIUM_BROWSER_GN_DEFINES+=' use_gio=true use_pulseaudio=true'
CHROMIUM_BROWSER_GN_DEFINES+=' enable_hangout_services_extension=true'
CHROMIUM_BROWSER_GN_DEFINES+=' use_aura=true'
CHROMIUM_BROWSER_GN_DEFINES+=' enable_widevine=true'

%if %{use_vaapi}
CHROMIUM_BROWSER_GN_DEFINES+=' use_vaapi=true'
%else
CHROMIUM_BROWSER_GN_DEFINES+=' use_vaapi=false'
%endif

%if %{use_v4l2_codec} 
CHROMIUM_BROWSER_GN_DEFINES+=' use_v4l2_codec=true'
%endif

%if 0%{?fedora}
CHROMIUM_BROWSER_GN_DEFINES+=' rtc_use_pipewire=true rtc_link_pipewire=true'
%endif

CHROMIUM_BROWSER_GN_DEFINES+=' use_system_libffi=true'

#ungoogled-chromium: defines
CHROMIUM_BROWSER_GN_DEFINES+=' '
CHROMIUM_BROWSER_GN_DEFINES+=$(tr '\n' ' ' < %{ungoogled_chromium_root}/flags.gn)

#ungoogled-chromium: enable PGO
%if %{use_pgo}
CHROMIUM_BROWSER_GN_DEFINES+=' chrome_pgo_phase=2'
%endif

export CHROMIUM_BROWSER_GN_DEFINES

# headless gn defines
CHROMIUM_HEADLESS_GN_DEFINES=""
CHROMIUM_HEADLESS_GN_DEFINES+=' use_ozone=true ozone_auto_platforms=false ozone_platform="headless" ozone_platform_headless=true'
CHROMIUM_HEADLESS_GN_DEFINES+=' angle_enable_vulkan=true angle_enable_swiftshader=true headless_use_embedded_resources=false'
CHROMIUM_HEADLESS_GN_DEFINES+=' headless_use_prefs=false headless_use_policy=false'
CHROMIUM_HEADLESS_GN_DEFINES+=' v8_use_external_startup_data=false enable_print_preview=false enable_remoting=false'
CHROMIUM_HEADLESS_GN_DEFINES+=' use_alsa=false use_bluez=false use_cups=false use_dbus=false use_gio=false use_kerberos=false'
CHROMIUM_HEADLESS_GN_DEFINES+=' use_libpci=false use_pulseaudio=false use_udev=false rtc_use_pipewire=false'
CHROMIUM_HEADLESS_GN_DEFINES+=' v8_enable_lazy_source_positions=false use_glib=false use_gtk=false use_pangocairo=false'
CHROMIUM_HEADLESS_GN_DEFINES+=' use_qt=false is_component_build=false enable_ffmpeg_video_decoders=false media_use_ffmpeg=false'
CHROMIUM_HEADLESS_GN_DEFINES+=' media_use_libvpx=false proprietary_codecs=false'
export CHROMIUM_HEADLESS_GN_DEFINES

# ungoogled-chromium: binary pruning.
# Exclude PGO profile from binary pruning
%if %{use_pgo}
sed -i '\!chrome/build/pgo_profiles/.*!d' %{ungoogled_chromium_root}/pruning.list
%endif
python3 -B %{ungoogled_chromium_root}/utils/prune_binaries.py . %{ungoogled_chromium_root}/pruning.list || true

build/linux/unbundle/replace_gn_files.py --system-libraries \
%if ! %{bundlelibaom}
	libaom \
%endif
%if ! %{bundlebrotli}
	brotli \
%endif
%if ! %{bundlefontconfig}
	fontconfig \
%endif
%if ! %{bundleffmpegfree}
	ffmpeg \
%endif
%if ! %{bundlefreetype}
	freetype \
%endif
%if ! %{bundleharfbuzz}
	harfbuzz-ng \
%endif
%if ! %{bundleicu}
	icu \
%endif
%if ! %{bundlelibdrm}
	libdrm \
%endif
%if ! %{bundlelibjpeg}
	libjpeg \
%endif
%if ! %{bundlelibpng}
	libpng \
%endif
%if ! %{bundlelibusbx}
	libusb \
%endif
%if ! %{bundlelibwebp}
	libwebp \
%endif
%if ! %{bundlelibxml}
	libxml \
%endif
	libxslt \
%if ! %{bundleopus}
	opus \
%endif
%if ! %{bundlere2}
	re2 \
%endif
%if ! %{bundleminizip}
	zlib \
%endif
	flac

# Check that there is no system 'google' module, shadowing bundled ones:
if python3 -c 'import google ; print google.__path__' 2> /dev/null ; then \
    echo "Python 3 'google' module is defined, this will shadow modules of this build"; \
    exit 1 ; \
fi

# ungoogled-chromium: patches
python3 -B %{ungoogled_chromium_root}/utils/patches.py apply .  %{ungoogled_chromium_root}/patches

# ungoogled-chromium: domain substitution
%if %{with domain_substitution}
rm -f %{_builddir}/dsc.tar.gz
python3 -B %{ungoogled_chromium_root}/utils/domain_substitution.py apply . \
  -r %{ungoogled_chromium_root}/domain_regex.list \
  -f %{ungoogled_chromium_root}/domain_substitution.list \
  -c %{_builddir}/dsc.tar.gz
%endif

%if %{bootstrap}
tools/gn/bootstrap/bootstrap.py --gn-gen-args="$CHROMIUM_CORE_GN_DEFINES $CHROMIUM_BROWSER_GN_DEFINES"
%else
mkdir -p %{builddir} && cp -a %{_bindir}/gn %{builddir}/
%endif

%{builddir}/gn --script-executable=%{chromium_pybin} gen --args="$CHROMIUM_CORE_GN_DEFINES $CHROMIUM_BROWSER_GN_DEFINES" %{builddir}

# workaround for build dependency
%build_target %{builddir} gen/components/feed/core/proto/v2/wire/chrome_feed_response_metadata.pb.h
%build_target %{builddir} chrome
%build_target %{builddir} chrome_sandbox
%build_target %{builddir} chromedriver

%if %{build_clear_key_cdm}
%build_target %{builddir} clear_key_cdm
%endif

%build_target %{builddir} policy_templates

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_bindir} \
         %{buildroot}%{chromium_path}/locales \
         %{buildroot}%{_sysconfdir}/%{name}

# install system wide chromium config
cp -a %{SOURCE2} %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf
cp -a %{SOURCE3} %{buildroot}%{chromium_path}/%{chromium_browser_channel}.sh

%if ! %{use_vaapi}
# remove vaapi flags
echo "# system wide chromium flags" > %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf
%endif

export BUILD_TARGET=`cat /etc/redhat-release`
export CHROMIUM_PATH=%{chromium_path}
export CHROMIUM_BROWSER_CHANNEL=%{chromium_browser_channel}

sed -i "s|@@BUILD_TARGET@@|$BUILD_TARGET|g" %{buildroot}%{chromium_path}/%{chromium_browser_channel}.sh
sed -i "s|@@CHROMIUM_PATH@@|$CHROMIUM_PATH|g" %{buildroot}%{chromium_path}/%{chromium_browser_channel}.sh
sed -i "s|@@CHROMIUM_BROWSER_CHANNEL@@|$CHROMIUM_BROWSER_CHANNEL|g" %{buildroot}%{chromium_path}/%{chromium_browser_channel}.sh

%if "%{chromium_channel}" == "%{nil}"
	sed -i "s|@@EXTRA_FLAGS@@||g" %{buildroot}%{chromium_path}/%{chromium_browser_channel}.sh
%else
	# Enable debug outputs for beta and dev channels
	export EXTRA_FLAGS="--enable-logging=stderr --v=2"
	sed -i "s|@@EXTRA_FLAGS@@|$EXTRA_FLAGS|g" %{buildroot}%{chromium_path}/%{chromium_browser_channel}.sh
%endif

ln -s ../..%{chromium_path}/%{chromium_browser_channel}.sh %{buildroot}%{_bindir}/%{chromium_browser_channel}
mkdir -p %{buildroot}%{_mandir}/man1/

pushd %{builddir}
	cp -a chrom*.pak resources.pak icudtl.dat %{buildroot}%{chromium_path}
	cp -a locales/*.pak %{buildroot}%{chromium_path}/locales/
	%ifarch x86_64 aarch64
		cp -a libvk_swiftshader.so %{buildroot}%{chromium_path}
		strip %{buildroot}%{chromium_path}/libvk_swiftshader.so
		cp -a libvulkan.so.1 %{buildroot}%{chromium_path}
		strip %{buildroot}%{chromium_path}/libvulkan.so.1
		cp -a vk_swiftshader_icd.json %{buildroot}%{chromium_path}
	%endif
	cp -a chrome %{buildroot}%{chromium_path}/%{chromium_browser_channel}
	# Explicitly strip chromium-browser (since we don't use debuginfo here anyway)
	strip %{buildroot}%{chromium_path}/%{chromium_browser_channel}
	cp -a chrome_sandbox %{buildroot}%{chromium_path}/chrome-sandbox
	strip %{buildroot}%{chromium_path}/chrome-sandbox
	cp -a chrome_crashpad_handler %{buildroot}%{chromium_path}/chrome_crashpad_handler
	strip %{buildroot}%{chromium_path}/chrome_crashpad_handler
	cp -a ../../chrome/app/resources/manpage.1.in %{buildroot}%{_mandir}/man1/%{chromium_browser_channel}.1
	sed -i "s|@@PACKAGE@@|%{chromium_browser_channel}|g" %{buildroot}%{_mandir}/man1/%{chromium_browser_channel}.1
	sed -i "s|@@MENUNAME@@|%{chromium_menu_name}|g" %{buildroot}%{_mandir}/man1/%{chromium_browser_channel}.1

	# V8 initial snapshots
	# https://code.google.com/p/chromium/issues/detail?id=421063
	cp -a v8_context_snapshot.bin %{buildroot}%{chromium_path}

	# This is ANGLE, not to be confused with the similarly named files under swiftshader/
	cp -a libEGL.so libGLESv2.so %{buildroot}%{chromium_path}
	strip %{buildroot}%{chromium_path}/libEGL.so
	strip %{buildroot}%{chromium_path}/libGLESv2.so

	%if %{use_qt}
		cp -a libqt5_shim.so %{buildroot}%{chromium_path}
		strip %{buildroot}%{chromium_path}/libqt5_shim.so
	%endif

	%if %{build_clear_key_cdm}
		%ifarch x86_64
			cp -a ClearKeyCdm/_platform_specific/linux_x64/libclearkeycdm.so %{buildroot}%{chromium_path}
		%else
			%ifarch aarch64
				cp -a ClearKeyCdm/_platform_specific/linux_arm64/libclearkeycdm.so %{buildroot}%{chromium_path}
			%else
				cp -a libclearkeycdm.so %{buildroot}%{chromium_path}
			%endif
		%endif
		strip %{buildroot}%{chromium_path}/libclearkeycdm.so
	%endif

	# chromedriver
	cp -a chromedriver %{buildroot}%{chromium_path}/chromedriver
	ln -s ../..%{chromium_path}/chromedriver %{buildroot}%{_bindir}/chromedriver
popd

# Add directories for policy management
mkdir -p %{buildroot}%{_sysconfdir}/ungoogled-chromium/policies/managed
mkdir -p %{buildroot}%{_sysconfdir}/ungoogled-chromium/policies/recommended

cp -a out/Release/gen/chrome/app/policy/common/html/en-US/*.html .
cp -a out/Release/gen/chrome/app/policy/linux/examples/chrome.json .

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/256x256/apps
cp -a chrome/app/theme/chromium/product_logo_256.png %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/%{chromium_browser_channel}.png
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/128x128/apps
cp -a chrome/app/theme/chromium/product_logo_128.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{chromium_browser_channel}.png
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/64x64/apps
cp -a chrome/app/theme/chromium/product_logo_64.png %{buildroot}%{_datadir}/icons/hicolor/64x64/apps/%{chromium_browser_channel}.png
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/48x48/apps
cp -a chrome/app/theme/chromium/product_logo_48.png %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/%{chromium_browser_channel}.png
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/24x24/apps
cp -a chrome/app/theme/chromium/product_logo_24.png %{buildroot}%{_datadir}/icons/hicolor/24x24/apps/%{chromium_browser_channel}.png

# Install the master_preferences file
install -m 0644 %{SOURCE13} %{buildroot}%{_sysconfdir}/%{name}/

mkdir -p %{buildroot}%{_datadir}/applications/
desktop-file-install --dir %{buildroot}%{_datadir}/applications %{SOURCE4}

install -D -m0644 %{SOURCE22} ${RPM_BUILD_ROOT}%{_datadir}/metainfo/%{chromium_browser_channel}.appdata.xml
appstream-util validate-relax --nonet ${RPM_BUILD_ROOT}%{_datadir}/metainfo/%{chromium_browser_channel}.appdata.xml

mkdir -p %{buildroot}%{_datadir}/gnome-control-center/default-apps/
cp -a %{SOURCE9} %{buildroot}%{_datadir}/gnome-control-center/default-apps/


%post
# Set SELinux labels - semanage itself will adjust the lib directory naming
# But only do it when selinux is enabled, otherwise, it gets noisy.
if selinuxenabled; then
	semanage fcontext -a -t bin_t /usr/lib/%{chromium_browser_channel} &>/dev/null || :
	semanage fcontext -a -t bin_t /usr/lib/%{chromium_browser_channel}/%{chromium_browser_channel}.sh &>/dev/null || :
	semanage fcontext -a -t chrome_sandbox_exec_t /usr/lib/chrome-sandbox &>/dev/null || :
	restorecon -R -v %{chromium_path}/%{chromium_browser_channel} &>/dev/null || :
fi

%files
%doc AUTHORS
%doc chrome_policy_list.html *.json
%license LICENSE
%config(noreplace) %{_sysconfdir}/%{name}/ungoogled-chromium.conf
%config %{_sysconfdir}/%{name}/master_preferences
%config %{_sysconfdir}/%{name}/policies/
%{_bindir}/%{chromium_browser_channel}
%{chromium_path}/*.bin
%{chromium_path}/chrome_*.pak
%{chromium_path}/chrome_crashpad_handler
%{chromium_path}/resources.pak
%{chromium_path}/%{chromium_browser_channel}
%{chromium_path}/%{chromium_browser_channel}.sh
%attr(4755, root, root) %{chromium_path}/chrome-sandbox
%if %{use_qt}
%{chromium_path}/libqt5_shim.so
%endif
%{_mandir}/man1/%{chromium_browser_channel}.*
%{_datadir}/icons/hicolor/*/apps/%{chromium_browser_channel}.png
%{_datadir}/applications/*.desktop
%{_datadir}/metainfo/*.appdata.xml
%{_datadir}/gnome-control-center/default-apps/ungoogled-chromium.xml

%if %{build_clear_key_cdm}
%{chromium_path}/libclearkeycdm.so
%endif
%ifarch x86_64 aarch64
%{chromium_path}/libvk_swiftshader.so*
%{chromium_path}/libvulkan.so*
%{chromium_path}/vk_swiftshader_icd.json
%{chromium_path}/libEGL.so*
%{chromium_path}/libGLESv2.so*
%endif
%{chromium_path}/icudtl.dat
%dir %{chromium_path}/
%dir %{chromium_path}/locales/
%lang(af) %{chromium_path}/locales/af.pak
%lang(am) %{chromium_path}/locales/am.pak
%lang(ar) %{chromium_path}/locales/ar.pak
%lang(bg) %{chromium_path}/locales/bg.pak
%lang(bn) %{chromium_path}/locales/bn.pak
%lang(ca) %{chromium_path}/locales/ca.pak
%lang(cs) %{chromium_path}/locales/cs.pak
%lang(da) %{chromium_path}/locales/da.pak
%lang(de) %{chromium_path}/locales/de.pak
%lang(el) %{chromium_path}/locales/el.pak
%lang(en_GB) %{chromium_path}/locales/en-GB.pak
# Chromium _ALWAYS_ needs en-US.pak as a fallback
# This means we cannot apply the lang code here.
# Otherwise, it is filtered out on install.
%{chromium_path}/locales/en-US.pak
%lang(es) %{chromium_path}/locales/es.pak
%lang(es) %{chromium_path}/locales/es-419.pak
%lang(et) %{chromium_path}/locales/et.pak
%lang(fa) %{chromium_path}/locales/fa.pak
%lang(fi) %{chromium_path}/locales/fi.pak
%lang(fil) %{chromium_path}/locales/fil.pak
%lang(fr) %{chromium_path}/locales/fr.pak
%lang(gu) %{chromium_path}/locales/gu.pak
%lang(he) %{chromium_path}/locales/he.pak
%lang(hi) %{chromium_path}/locales/hi.pak
%lang(hr) %{chromium_path}/locales/hr.pak
%lang(hu) %{chromium_path}/locales/hu.pak
%lang(id) %{chromium_path}/locales/id.pak
%lang(it) %{chromium_path}/locales/it.pak
%lang(ja) %{chromium_path}/locales/ja.pak
%lang(kn) %{chromium_path}/locales/kn.pak
%lang(ko) %{chromium_path}/locales/ko.pak
%lang(lt) %{chromium_path}/locales/lt.pak
%lang(lv) %{chromium_path}/locales/lv.pak
%lang(ml) %{chromium_path}/locales/ml.pak
%lang(mr) %{chromium_path}/locales/mr.pak
%lang(ms) %{chromium_path}/locales/ms.pak
%lang(nb) %{chromium_path}/locales/nb.pak
%lang(nl) %{chromium_path}/locales/nl.pak
%lang(pl) %{chromium_path}/locales/pl.pak
%lang(pt_BR) %{chromium_path}/locales/pt-BR.pak
%lang(pt_PT) %{chromium_path}/locales/pt-PT.pak
%lang(ro) %{chromium_path}/locales/ro.pak
%lang(ru) %{chromium_path}/locales/ru.pak
%lang(sk) %{chromium_path}/locales/sk.pak
%lang(sl) %{chromium_path}/locales/sl.pak
%lang(sr) %{chromium_path}/locales/sr.pak
%lang(sv) %{chromium_path}/locales/sv.pak
%lang(sw) %{chromium_path}/locales/sw.pak
%lang(ta) %{chromium_path}/locales/ta.pak
%lang(te) %{chromium_path}/locales/te.pak
%lang(th) %{chromium_path}/locales/th.pak
%lang(tr) %{chromium_path}/locales/tr.pak
%lang(uk) %{chromium_path}/locales/uk.pak
%lang(ur) %{chromium_path}/locales/ur.pak
%lang(vi) %{chromium_path}/locales/vi.pak
%lang(zh_CN) %{chromium_path}/locales/zh-CN.pak
%lang(zh_TW) %{chromium_path}/locales/zh-TW.pak
# These are psuedolocales, not real ones.
# They only get generated when is_official_build=false
%if ! %{official_build}
%{chromium_path}/locales/ar-XB.pak
%{chromium_path}/locales/en-XA.pak
%endif

%{_bindir}/chromedriver
%{chromium_path}/chromedriver

%changelog
* Sun Feb  13 2022 wchen342 <feiyu2817@gmail.com> - 98.0.4758.80-1
- update Chromium to 98.0.4758.80

* Tue Dec  14 2021 wchen342 <feiyu2817@gmail.com> - 96.0.4664.110-1
- update Chromium to 96.0.4664.110
- Enable PGO

* Sat Dec  11 2021 wchen342 <feiyu2817@gmail.com> - 96.0.4664.93-1
- update Chromium to 96.0.4664.93

* Thu Nov  18 2021 wchen342 <feiyu2817@gmail.com> - 96.0.4664.45-1
- update Chromium to 96.0.4664.45

* Thu Nov  11 2021 wchen342 <feiyu2817@gmail.com> - 95.0.4638.69-1
- update Chromium to 95.0.4638.69
- Use clang instead of gcc
- Enable CFI

* Fri Oct  8 2021 wchen342 <feiyu2817@gmail.com> - 94.0.4606.81-1
- update Chromium to 94.0.4606.81

* Fri Oct  1 2021 wchen342 <feiyu2817@gmail.com> - 94.0.4606.71-1
- update Chromium to 94.0.4606.71

* Tue Sep 28 2021 wchen342 <feiyu2817@gmail.com> - 94.0.4606.61-1
- update Chromium to 94.0.4606.61

* Wed Sep 22 2021 wchen342 <feiyu2817@gmail.com> - 93.0.4577.82-1
- update Chromium to 93.0.4577.82

* Sat Sep  4 2021 wchen342 <feiyu2817@gmail.com> - 93.0.4577.63-1
- update Chromium to 93.0.4577.63

* Mon Aug  9 2021 wchen342 <feiyu2817@gmail.com> - 92.0.4515.131-1
- update Chromium to 92.0.4515.131

* Fri Jul 16 2021 wchen342 <feiyu2817@gmail.com> - 91.0.4472.164-1
- update Chromium to 91.0.4472.164

* Sat Jul 10 2021 wchen342 <feiyu2817@gmail.com> - 91.0.4472.114-2
- Fedora upstream update

* Sat Jun 12 2021 wchen342 <feiyu2817@gmail.com> - 91.0.4472.114-1
- update Chromium to 91.0.4472.114

* Sat Jun 12 2021 wchen342 <feiyu2817@gmail.com> - 91.0.4472.101-1
- update Chromium to 91.0.4472.101

* Sun Jun  6 2021 wchen342 <feiyu2817@gmail.com> - 91.0.4472.77-1
- update Chromium to 91.0.4472.77

* Thu May 13 2021 wchen342 <feiyu2817@gmail.com> - 90.0.4430.212-1
- update Chromium to 90.0.4430.212

* Sun May  2 2021 wchen342 <feiyu2817@gmail.com> - 90.0.4430.93-1
- update Chromium to 90.0.4430.93

* Thu Apr  1 2021 wchen342 <feiyu2817@gmail.com> - 89.0.4389.114-1
- Update Chromium to 89.0.4389.114

* Tue Mar  9 2021 wchen342 <feiyu2817@gmail.com> - 89.0.4389.82-1
- Update Chromium to 89.0.4389.82

* Sun Mar  7 2021 wchen342 <feiyu2817@gmail.com> - 89.0.4389.72-1
- Update Chromium to 89.0.4389.72

* Fri Feb 19 2021 wchen342 <feiyu2817@gmail.com> - 88.0.4324.182-1
- Update Chromium to 88.0.4234.182

* Fri Feb 05 2021 wchen342 <feiyu2817@gmail.com> - 88.0.4324.150-1
- Update Chromium to 88.0.4324.150

* Wed Feb 03 2021 wchen342 <feiyu2817@gmail.com> - 88.0.4324.146-1
- Update Chromium to 88.0.4324.146
- Update ungoogled-chromium to 88.0.4324.146-1

* Fri Jan 29 2021 wchen342 <feiyu2817@gmail.com> - 88.0.4324.104-1
- Update Chromium to 88.0.4324.104
- Update ungoogled-chromium to 88.0.4324.104-1

* Fri Jan 1 2021 wchen342 <feiyu2817@gmail.com> - 87.0.4280.141-1
- Update Chromium to 87.0.4280.141
- Update ungoogled-chromium to 87.0.4280.141-1
- Add back RHEL (CentOS) support

* Wed Dec 09 2020 wchen342 <feiyu2817@gmail.com> - 87.0.4280.88-1
- Update Chromium to 87.0.4280.88
- Update ungoogled-chromium to 87.0.4280.88-1
- Rewrite spec file with Fedora Chromium source

* Mon Sep 14 2020 qvint <dotqvint@gmail.com> - 85.0.4183.102-1
- Update Chromium to 85.0.4183.102
- Update ungoogled-chromium to 85.0.4183.102-1
- Add domain_substitution switch
- Fix manpage and desktop metadata files
- Update AppStream metadata

* Thu Aug 13 2020 qvint <dotqvint@gmail.com> - 84.0.4147.125-1
- Update Chromium to 84.0.4147.125
- Update ungoogled-chromium to 84.0.4147.125-1

* Sat Jul 18 2020 qvint <dotqvint@gmail.com> - 84.0.4147.89-1
- Update Chromium to 84.0.4147.89
- Update ungoogled-chromium to 84.0.4147.89-1

* Sat Jun 27 2020 qvint <dotqvint@gmail.com> - 83.0.4103.116-1
- Update Chromium to 83.0.4103.116
- Update ungoogled-chromium to 83.0.4103.116-1
- Try alternative locations for the Widevine CDM library

* Wed May 06 2020 qvint <dotqvint@gmail.com> - 81.0.4044.138-1
- Update Chromium to 81.0.4044.138
- Update ungoogled-chromium to 38e86b5

* Thu Apr 30 2020 qvint <dotqvint@gmail.com> - 81.0.4044.129-1
- Update Chromium to 81.0.4044.129
- Update ungoogled-chromium to 81.0.4044.129-1

* Fri Apr 10 2020 qvint <dotqvint@gmail.com> - 81.0.4044.92-1
- Update Chromium to 81.0.4044.92
- Update ungoogled-chromium to 209e24b

* Thu Feb 27 2020 qvint <dotqvint@gmail.com> - 80.0.3987.122-1
- Update Chromium to 80.0.3987.122
- Update ungoogled-chromium to 80.0.3987.122-1

* Tue Feb 04 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 79.0.3945.130-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 17 2020 qvint <dotqvint@gmail.com> - 79.0.3945.130-1
- Update Chromium to 79.0.3945.130
- Update ungoogled-chromium to 79.0.3945.130-1

* Wed Jan 08 2020 qvint <dotqvint@gmail.com> - 79.0.3945.117-1
- Update Chromium to 79.0.3945.117
- Update ungoogled-chromium to 79.0.3945.117-1

* Wed Dec 18 2019 qvint <dotqvint@gmail.com> - 79.0.3945.88-1
- Update Chromium to 79.0.3945.88
- Update ungoogled-chromium to 7ddfefb
- Sync spec and sources with free/chromium-freeworld (e472355)

* Tue Nov 19 2019 qvint <dotqvint@gmail.com> - 78.0.3904.108-1
- Update Chromium to 78.0.3904.108
- Update ungoogled-chromium to 0529d60

* Thu Nov 07 2019 qvint <dotqvint@gmail.com> - 78.0.3904.97-1
- Update Chromium to 78.0.3904.97
- Update ungoogled-chromium to 6894e44

* Sat Nov 02 2019 qvint <dotqvint@gmail.com> - 78.0.3904.87-1
- Update Chromium to 78.0.3904.87
- Update ungoogled-chromium to 78.0.3904.87-1
- Disable debuginfo to match fedora chromium

* Fri Nov 01 2019 qvint <dotqvint@gmail.com> - 78.0.3904.70-1
- Update Chromium to 78.0.3904.70
- Update ungoogled-chromium to 78.0.3904.70-1

* Mon Oct 14 2019 qvint <dotqvint@gmail.com> - 77.0.3865.120-1
- Update Chromium to 77.0.3865.120
- Update ungoogled-chromium to 99b98c5

* Wed Sep 25 2019 qvint <dotqvint@gmail.com> - 77.0.3865.90-1
- Update Chromium to 77.0.3865.90
- Update ungoogled-chromium to 77.0.3865.90-1
- Disabled Nvidia support
- Use the bundled python2 as python2 is going to be removed from Fedora

* Mon Sep 23 2019 qvint <dotqvint@gmail.com> - 76.0.3809.132-1
- Initial version based on Akarshan Biswas' <akarshanbiswas@fedoraproject.org> work
