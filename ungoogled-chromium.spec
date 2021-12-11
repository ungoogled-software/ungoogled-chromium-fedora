%global obs 0
%global ninja_verbose 0
%global ccache 0

%define _lto_cflags %{nil}

%global numjobs 8
%ifarch aarch64
%global numjobs 4
%endif

# official builds have less debugging and go faster... but we have to shut some things off.
%global official_build 1

# Fancy build status, so we at least know, where we are..
# %1 where
# %2 what
%if %{ninja_verbose}
%global build_target() \
	export NINJA_STATUS="[%2:%f/%t] " ; \
	../depot_tools/ninja -j %{numjobs} -C '%1' -vvv '%2'
%else
%global build_target() \
	export NINJA_STATUS="[%2:%f/%t] " ; \
	../depot_tools/ninja -j %{numjobs} -C '%1' '%2'
%endif

# Define __python2 and __python3 for OBS
%if %{obs}
%global __python2 /usr/bin/python2
%global __python3 /usr/bin/python3
%endif

# This is finally possible with Chromium 93
%global build_with_python3 1

%if 0%{?build_with_python3}
%global chromium_pybin %{__python3}
%else
%global chromium_pybin %{__python2}
%endif

%global use_vaapi 1

# 2020-08-20: F33+ aarch64 has a binutils bug trying to link clear_key_cdm
# https://bugzilla.redhat.com/show_bug.cgi?id=1869884
%global build_clear_key_cdm 1

# NEVER EVER EVER turn this on in official builds
%global freeworld 0
%if %{freeworld}
%global lsuffix freeworld
%global nsuffix -freeworld
%else
%global lsuffix fedora
%global nsuffix %{nil}
%endif

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

%global __provides_exclude_from %{chromium_path}/.*\\.so|%{chromium_path}/lib/.*\\.so|%{chromium_path}/lib/.*\\.so.*
%global privlibs libaccessibility|libandroid_mojo_bindings_shared|libanimation|libapdu|libaura|libaura_extra|libauthenticator_test_mojo_bindings_shared|libbase|libbase_i18n|libbindings|libbindings_base|libblink_common|libblink_controller|libblink_core|libblink_embedded_frame_sink_mojo_bindings_shared|libblink_features|libblink_modules|libblink_mojom_broadcastchannel_bindings_shared|libblink_platform|libbluetooth|libboringssl|libbrowser_ui_views|libcaptive_portal|libcapture_base|libcapture_lib|libcbor|libcc|libcc_animation|libcc_base|libcc_debug|libcc_ipc|libcc_mojo_embedder|libcc_paint|libcertificate_matching|libcert_verifier|libchrome_features|libchromium_sqlite3|libclearkeycdm|libclient|libcloud_policy_proto_generated_compile|libcodec|libcolor_space|libcolor_utils|libcommon|libcompositor|libcontent|libcontent_common_mojo_bindings_shared|libcontent_public_common_mojo_bindings_shared|libcontent_service_cpp|libcontent_service_mojom|libcontent_service_mojom_shared|libcontent_settings_features|libcrash_key_lib|libcrcrypto|libcrdtp|libdbus|libdevice_base|libdevice_event_log|libdevice_features|libdevice_gamepad|libdevices|libdevice_vr|libdevice_vr_mojo_bindings|libdevice_vr_mojo_bindings_blink|libdevice_vr_mojo_bindings_shared|libdevice_vr_test_mojo_bindings|libdevice_vr_test_mojo_bindings_blink|libdevice_vr_test_mojo_bindings_shared|libdiscardable_memory_client|libdiscardable_memory_common|libdiscardable_memory_service|libdisplay|libdisplay_types|libdisplay_util|libdomain_reliability|libdom_storage_mojom|libdom_storage_mojom_shared|libEGL|libEGL|libembedder|libembedder_switches|libevents|libevents_base|libevents_devices_x11|libevents_ozone_layout|libevents_x|libextras|libffmpeg|libfido|libfingerprint|libfreetype_harfbuzz|libgamepad_mojom|libgamepad_mojom_blink|libgamepad_mojom_shared|libgamepad_shared_typemap_traits|libgcm|libgeometry|libgeometry_skia|libgesture_detection|libgfx|libgfx_ipc|libgfx_ipc_buffer_types|libgfx_ipc_color|libgfx_ipc_geometry|libgfx_ipc_skia|libgfx_switches|libgfx_x11|libgin|libgles2|libgles2_implementation|libgles2_utils|libGLESv2|libGLESv2|libgl_init|libgl_in_process_context|libgl_wrapper|libgpu|libgpu_ipc_service|libgtkui|libheadless_non_renderer|libhost|libicui18n|libicuuc|libinterfaces_shared|libipc|libipc_mojom|libipc_mojom_shared|libkeycodes_x11|libkeyed_service_content|libkeyed_service_core|liblearning_common|liblearning_impl|libleveldatabase|libleveldb_proto|libmanager|libmedia|libmedia_blink|libmedia_gpu|libmedia_learning_mojo_impl|libmedia_message_center|libmedia_mojo_services|libmedia_session_base_cpp|libmedia_session_cpp|libmedia_webrtc|libmemory_instrumentation|libmenu|libmessage_center|libmessage_support|libmetrics_cpp|libmidi|libmirroring_service|libmojo_base_lib|libmojo_base_mojom|libmojo_base_mojom_blink|libmojo_base_mojom_shared|libmojo_base_shared_typemap_traits|libmojo_core_embedder|libmojo_core_embedder_internal|libmojo_core_ports|libmojo_cpp_platform|libmojom_core_shared|libmojom_mhtml_load_result_shared|libmojom_modules_shared|libmojo_mojom_bindings|libmojo_mojom_bindings_shared|libmojom_platform_shared|libmojo_public_system|libmojo_public_system_cpp|libnative_theme|libnet|libnetwork_cpp|libnetwork_cpp_base|libnetwork_service|libnetwork_session_configurator|libonc|libos_crypt|libparsers|libpdfium|libperfetto|libperformace_manager_public_mojom|libperformace_manager_public_mojom_blink|libperformace_manager_public_mojom_shared|libplatform|libplatform_window|libplatform_window_common|libplatform_window_handler_libs|libpolicy_component|libpolicy_proto|libppapi_host|libppapi_proxy|libppapi_shared|libprefs|libprinting|libproperties|libprotobuf_lite|libproxy_config|libpublic|librange|libraster|libresource_coordinator_public_mojom|libresource_coordinator_public_mojom_blink|libresource_coordinator_public_mojom_shared|libsandbox|libsandbox_services|libscheduling_metrics|libseccomp_bpf|libsecurity_state_features|libservice|libservice_manager_cpp|libservice_manager_cpp_types|libservice_manager_mojom|libservice_manager_mojom_blink|libservice_manager_mojom_constants|libservice_manager_mojom_constants_blink|libservice_manager_mojom_constants_shared|libservice_manager_mojom_shared|libservice_manager_mojom_traits|libservice_provider|libsessions|libshared_memory_support|libshared_with_blink|libshell_dialogs|libskia|libskia_shared_typemap_traits|libsnapshot|libsql|libstartup_tracing|libstorage_browser|libstorage_common|libstorage_service_public|libstub_window|libsuid_sandbox_client|libsurface|libsystem_media_controls|libtab_count_metrics|libthread_linux|libtracing|libtracing_cpp|libtracing_mojom|libtracing_mojom_shared|libui_accessibility_ax_mojom|libui_accessibility_ax_mojom_blink|libui_accessibility_ax_mojom_shared|libui_base|libui_base_clipboard|libui_base_clipboard_types|libui_base_features|libui_base_idle|libui_base_ime|libui_base_ime_init|libui_base_ime_linux|libui_base_ime_types|libui_base_x|libui_data_pack|libui_devtools|libui_message_center_cpp|libui_touch_selection|liburl|liburl_ipc|liburl_matcher|libusb_shared|libuser_manager|libuser_prefs|libv8|libv8_libbase|libv8_libplatform|libviews|libviz_common|libviz_resource_format_utils|libviz_vulkan_context_provider|libVkICD_mock_icd|libvk_swiftshader|libvr_base|libvr_common|libvulkan_info|libvulkan_init|libvulkan_wrapper|libvulkan_x11|libvulkan_ycbcr_info|libweb_bluetooth_mojo_bindings_shared|libwebdata_common|libweb_dialogs|libweb_feature_mojo_bindings_mojom|libweb_feature_mojo_bindings_mojom_blink|libweb_feature_mojo_bindings_mojom_shared|libwebgpu|libweb_modal|libwebrtc_component|libwebview|libwm|libwm_public|libwtf|libwtf_support|libx11_events_platform|libx11_window|libzygote
%global __requires_exclude ^(%{privlibs})\\.so*



%if 0
# Chromium's fork of ICU is now something we can't unbundle.
# This is left here to ease the change if that ever switches.
BuildRequires:  libicu-devel >= 5.4
%global bundleicu 0
%else
%global bundleicu 1
%endif

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

# Chromium used to break on wayland, hidpi, and colors with gtk3 enabled.
# Hopefully it does not anymore.
%global gtk3 1


%global bundleharfbuzz 1
%global bundleopus 1
%global bundlelibusbx 0
%global bundlelibwebp 0
%global bundlelibpng 0
%global bundlelibjpeg 0
# Needs FT_ClipBox which was implemented after 2.11.0. Should be able to set this back to 0 later.
%global bundlefreetype 1
%global bundlelibdrm 0
%global bundlefontconfig 0

### Google API keys (see http://www.chromium.org/developers/how-tos/api-keys)
### Note: These are for Fedora use ONLY.
### For your own distribution, please get your own set of keys.
### http://lists.debian.org/debian-legal/2013/11/msg00006.html
%global api_key %{nil}
%global default_client_id %{nil}
%global default_client_secret %{nil}

#Build with debugging symbols
%global debug_pkg 0

%global majorversion 96
%global revision 1

# Depot tools revision
%global depot_tools_revision dc86a4b9044f9243886ca0da0c1753820ac51f45

%if %{freeworld}
Name:		ungoogled-chromium%{nsuffix}
%else
Name:		ungoogled-chromium
%endif
Version:	%{majorversion}.0.4664.93
Release:	1%{?dist}.%{revision}
%if %{?freeworld}
# chromium-freeworld
Summary:	A lightweight approach to removing Google web service dependency, built with all possible codecs
%else
Summary:	A lightweight approach to removing Google web service dependency
%endif
URL:		https://github.com/Eloston/ungoogled-chromium
License:	BSD and LGPLv2+ and ASL 2.0 and IJG and MIT and GPLv2+ and ISC and OpenSSL and (MPLv1.1 or GPLv2 or LGPLv2)

### Chromium Fedora Patches ###
# Use /etc/chromium for initial_prefs
Patch1:		chromium-91.0.4472.77-initial_prefs-etc-path.patch
# Use gn system files
Patch2:		chromium-67.0.3396.62-gn-system.patch
# Do not prefix libpng functions
Patch3:		chromium-60.0.3112.78-no-libpng-prefix.patch
# Do not mangle zlib
Patch5:		chromium-77.0.3865.75-no-zlib-mangle.patch
# Try to load widevine from other places
Patch10:	chromium-92.0.4515.107-widevine-other-locations.patch
# Tell bootstrap.py to always use the version of Python we specify
Patch11:        chromium-93.0.4577.63-py3-bootstrap.patch
# https://gitweb.gentoo.org/repo/gentoo.git/tree/www-client/chromium/files/chromium-unbundle-zlib.patch
Patch52:	chromium-81.0.4044.92-unbundle-zlib.patch
# https://github.com/stha09/chromium-patches/blob/master/chromium-96-CouponDB-include.patch
Patch59:	chromium-96-CouponDB-include.patch
# https://github.com/stha09/chromium-patches/blob/master/chromium-96-CommandLine-include.patch
Patch61:	chromium-96-CommandLine-include.patch
# https://github.com/stha09/chromium-patches/blob/master/chromium-96-RestrictedCookieManager-tuple.patch
Patch62:	chromium-96-RestrictedCookieManager-tuple.patch
# https://github.com/stha09/chromium-patches/blob/master/chromium-96-DrmRenderNodePathFinder-include.patch
Patch63:	chromium-96-DrmRenderNodePathFinder-include.patch
# Fix issue where closure_compiler thinks java is only allowed in android builds
# https://bugs.chromium.org/p/chromium/issues/detail?id=1192875
Patch65:	chromium-91.0.4472.77-java-only-allowed-in-android-builds.patch

# Work around binutils bug in aarch64 (F33+)
Patch68:	chromium-84.0.4147.125-aarch64-clearkeycdm-binutils-workaround.patch
# Rawhide (f35) glibc defines SIGSTKSZ as a long instead of a constant
Patch76:	chromium-92.0.4515.107-rawhide-gcc-std-max-fix.patch
# Do not download proprietary widevine module in the background (thanks Debian)
Patch79:	chromium-93.0.4577.63-widevine-no-download.patch

# Fix crashes with components/cast_*
# Thanks to Gentoo
Patch80:	chromium-96-EnumTable-crash.patch

# Clean up clang-format for python3
# thanks to Jon Nettleton
Patch86:	chromium-94.0.4606.81-clang-format.patch
# include full UrlResponseHead header
Patch95:	chromium-93.0.4577.63-mojo-header-fix.patch
# Fix multiple defines issue in webrtc/BUILD.gn
Patch96:	chromium-94.0.4606.54-webrtc-BUILD.gn-fix-multiple-defines.patch
# From gentoo
Patch98:	chromium-94.0.4606.71-InkDropHost-crash.patch


# VAAPI
# Upstream turned VAAPI on in Linux in 86
Patch202:	chromium-89.0.4389.72-enable-hardware-accelerated-mjpeg.patch
Patch203:	chromium-86.0.4240.75-vaapi-i686-fpermissive.patch
Patch205:	chromium-86.0.4240.75-fix-vaapi-on-intel.patch

# Apply these patches to work around EPEL8 issues
Patch300:	chromium-92.0.4515.107-rhel8-force-disable-use_gnome_keyring.patch

# Fixes from Gentoo
Patch400:   chromium-glibc-2.34.patch
Patch401:   chromium-VirtualCursor-standard-layout.patch

# Clang 12 cflags
Patch403:   chromium-clang-12-cflags.patch
Patch404:   chromium-clang-sanitizer-cflags.patch

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
%if %{freeworld} || %{obs}
Source0:	https://commondatastorage.googleapis.com/chromium-browser-official/chromium-%{version}.tar.xz
%else
Source0:	chromium-%{version}-clean.tar.xz
%endif
# Packaged by OBS from https://chromium.googlesource.com/chromium/tools/depot_tools.git
Source2:	depot_tools-%{depot_tools_revision}.tar.xz
Source3:	ungoogled-chromium.sh
Source4:	%{chromium_browser_channel}.desktop
# Also, only used if you want to reproduce the clean tarball.
Source5:	clean_ffmpeg.sh
Source6:	chromium-latest.py
Source7:	get_free_ffmpeg_source_files.py
# Get the names of all tests (gtests) for Linux
# Usage: get_linux_tests_name.py chromium-%%{version} --spec
Source8:	get_linux_tests_names.py
# GNOME stuff
Source9:	ungoogled-chromium.xml
Source13:	master_preferences
# Unpackaged fonts
Source14:	https://fontlibrary.org/assets/downloads/gelasio/4d610887ff4d445cbc639aae7828d139/gelasio.zip
Source15:	https://download.savannah.nongnu.org/releases/freebangfont/MuktiNarrow-0.94.tar.bz2
Source16:	https://github.com/web-platform-tests/wpt/raw/master/fonts/Ahem.ttf
Source17:	GardinerModBug.ttf
Source18:	GardinerModCat.ttf
# Bring xcb-proto with us (might need more than python on EPEL?)
Source20:	https://www.x.org/releases/individual/proto/xcb-proto-1.14.tar.xz

# Add our own appdata file.
Source22:       ungoogled-chromium.appdata.xml

# ungoogled-chromium source
%global ungoogled_chromium_revision 96.0.4664.93-1
Source300:      https://github.com/Eloston/ungoogled-chromium/archive/%{ungoogled_chromium_revision}/ungoogled-chromium-%{ungoogled_chromium_revision}.tar.gz

BuildRequires:	llvm
BuildRequires:	llvm-libs
BuildRequires:	clang
BuildRequires:	clang-libs
BuildRequires:	lld
BuildRequires:	lld-libs
BuildRequires:	compiler-rt

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
%if 0%{?bundleharfbuzz}
#nothing
%else
BuildRequires:	harfbuzz-devel >= 2.4.0
%endif
BuildRequires:	libatomic
BuildRequires:	libcap-devel
BuildRequires:	libcurl-devel
%if 0%{?bundlelibdrm}
#nothing
%else
BuildRequires:	libdrm-devel
%endif
BuildRequires:	libgcrypt-devel
BuildRequires:	libudev-devel
BuildRequires:	libuuid-devel
BuildRequires:	libusb-devel
BuildRequires:	libXdamage-devel
BuildRequires:	libXtst-devel
BuildRequires:	xcb-proto
BuildRequires:	mesa-libgbm-devel
BuildRequires:	minizip-compat-devel
BuildRequires:	nodejs
BuildRequires:	nss-devel >= 3.26
BuildRequires:	pciutils-devel
BuildRequires:	pulseaudio-libs-devel

# For screen sharing on Wayland, currently Fedora only thing - no epel
%if 0%{?fedora}
BuildRequires:	pkgconfig(libpipewire-0.3)
%endif

# for /usr/bin/appstream-util
BuildRequires: libappstream-glib

# gn needs these
BuildRequires:  libstdc++-static
BuildRequires:	libstdc++-devel, openssl-devel
# Fedora tries to use system libs whenever it can.
BuildRequires:	bzip2-devel
BuildRequires:	dbus-glib-devel
# For eu-strip
BuildRequires:	elfutils
BuildRequires:	elfutils-libelf-devel
BuildRequires:	flac-devel
%if 0%{?bundlefreetype}
# nothing
%else
BuildRequires:	freetype-devel
%endif
BuildRequires:	hwdata
BuildRequires:	kernel-headers
BuildRequires:	libevent-devel
BuildRequires:	libffi-devel
%if 0%{?bundleicu}
# If this is true, we're using the bundled icu.
# We'd like to use the system icu every time, but we cannot always do that.
%else
# Not newer than 54 (at least not right now)
BuildRequires:	libicu-devel = 54.1
%endif
%if 0%{?bundlelibjpeg}
# If this is true, we're using the bundled libjpeg
# which we need to do because the RHEL 7 libjpeg doesn't work for chromium anymore
%else
BuildRequires:	libjpeg-devel
%endif
%if 0%{?bundlelibpng}
# If this is true, we're using the bundled libpng
# which we need to do because the RHEL 7 libpng doesn't work right anymore
%else
BuildRequires:	libpng-devel
%endif
%if 0
# see https://code.google.com/p/chromium/issues/detail?id=501318
BuildRequires:	libsrtp-devel >= 1.4.4
%endif
BuildRequires:	libudev-devel
%if %{bundlelibusbx}
# Do nothing
%else
%if 0%{?fedora} >= 35
Requires:	libusb1 >= 1.0.24-4
BuildRequires:	libusb1-devel >= 1.0.24-4
%else
Requires:	libusbx >= 1.0.21-0.1.git448584a
BuildRequires:	libusbx-devel >= 1.0.21-0.1.git448584a
%endif
%endif
BuildRequires:	libva-devel
# We don't use libvpx anymore because Chromium loves to
# use bleeding edge revisions here that break other things
# ... so we just use the bundled libvpx.
%if %{bundlelibwebp}
# Do nothing
%else
BuildRequires:	libwebp-devel
%endif
BuildRequires:	libxslt-devel
BuildRequires:	libxshmfence-devel
# Same here, it seems.
# BuildRequires:	libyuv-devel
BuildRequires:	mesa-libGL-devel
%if %{bundleopus}
# Do nothing
%else
BuildRequires:	opus-devel
%endif
BuildRequires:	perl(Switch)
%if 0%{gtk3}
BuildRequires:	pkgconfig(gtk+-3.0)
%else
BuildRequires:	pkgconfig(gtk+-2.0)
%endif
%if ! %{build_with_python3}
%if 0%{?fedora} >= 32
BuildRequires:	python2.7
%else
BuildRequires:	python2
BuildRequires:	python2-devel
%endif
%else
BuildRequires:  python3
BuildRequires:  python3-devel
%endif

%if 0%{?build_with_python3}
%if 0%{?bundlepylibs}
# Using bundled bits, do nothing.
%else
BuildRequires:	python3-beautifulsoup4
# BuildRequires:	python2-beautifulsoup
BuildRequires:	python3-html5lib
BuildRequires:	python3-markupsafe
BuildRequires:	python3-ply
BuildRequires:	python3-simplejson
%endif
%else
%if 0%{?bundlepylibs}
# Using bundled bits, do nothing.
%else
BuildRequires:  python2-beautifulsoup4
BuildRequires:  python2-beautifulsoup
BuildRequires:  python2-html5lib
BuildRequires:  python2-markupsafe
BuildRequires:  python2-ply
BuildRequires:  python2-simplejson
%endif
%endif


%if 0%{?bundlere2}
# Using bundled bits, do nothing.
%else
Requires:	re2 >= 20160401
BuildRequires:	re2-devel >= 20160401
%endif
BuildRequires:	speech-dispatcher-devel
BuildRequires:	yasm
BuildRequires:	zlib-devel
# for third_party/test_fonts
%if %{freeworld}
# dont need fonts for this
%else
BuildRequires:	google-croscore-arimo-fonts
BuildRequires:	google-croscore-cousine-fonts
BuildRequires:	google-croscore-tinos-fonts
BuildRequires:  google-noto-sans-cjk-jp-fonts
BuildRequires:  lohit-gurmukhi-fonts
BuildRequires:	dejavu-sans-fonts
BuildRequires:	thai-scalable-garuda-fonts
BuildRequires:	lohit-devanagari-fonts
BuildRequires:	lohit-tamil-fonts
BuildRequires:	google-noto-sans-khmer-fonts
BuildRequires:	google-noto-emoji-color-fonts
BuildRequires:	google-noto-sans-symbols2-fonts
# There used to be a copy of this font file here, but it looks like NotoSansTibetan is no more.
# And yet, the chromium code still wants it.
Source115:	NotoSansTibetan-Regular.ttf
%endif
# using the built from source version on aarch64
BuildRequires:	ninja-build
# Yes, java is needed as well..
BuildRequires:	java-1.8.0-openjdk-headless
BuildRequires:	lua


# There is a hardcoded check for nss 3.26 in the chromium code (crypto/nss_util.cc)
Requires:	nss%{_isa} >= 3.26
Requires:	nss-mdns%{_isa}

# GTK modules it expects to find for some reason.
%if 0%{gtk3}
Requires:	libcanberra-gtk3%{_isa}
%else
Requires:	libcanberra-gtk2%{_isa}
%endif

%if 0%{?fedora}
# This enables support for u2f tokens
Requires:	u2f-hidraw-policy
%endif

ExclusiveArch:	x86_64 i686 aarch64

# For selinux scriptlet
Requires(post): /usr/sbin/semanage
Requires(post): /usr/sbin/restorecon

%if %{?freeworld}
%description
%{name} is a distribution of ungoogled-chromium, built with all possible codecs.

ungoogled-chromium is Chromium, sans integration with Google. It also features
some tweaks to enhance privacy, control, and transparency (almost all of which
require manual activation or enabling).

ungoogled-chromium retains the default Chromium experience as closely as
possible. Unlike other Chromium forks that have their own visions of a web
browser, ungoogled-chromium is essentially a drop-in replacement for Chromium.
%else
%description
%{name} is a distribution of ungoogled-chromium.

ungoogled-chromium is Chromium, sans integration with Google. It also features
some tweaks to enhance privacy, control, and transparency (almost all of which
require manual activation or enabling).

ungoogled-chromium retains the default Chromium experience as closely as
possible. Unlike other Chromium forks that have their own visions of a web
browser, ungoogled-chromium is essentially a drop-in replacement for Chromium.
%endif

# Chromium needs an explicit Requires: minizip-compat
Requires: minizip-compat%{_isa}

############################################PREP###########################################################
%prep
%setup -q -T -n ungoogled-chromium-%{ungoogled_chromium_revision} -b 300
%setup -q -T -n depot_tools-%{depot_tools_revision} -b 2
%setup -q -n chromium-%{version}

%global ungoogled_chromium_root %{_builddir}/ungoogled-chromium-%{ungoogled_chromium_revision}

ln -s depot_tools-%{depot_tools_revision} ../depot_tools

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
%patch1 -p1 -b .etc
%patch2 -p1 -b .gnsystem
%patch3 -p1 -b .nolibpngprefix
%patch5 -p1 -b .nozlibmangle
%patch10 -p1 -b .widevine-other-locations
%if 0%{?build_with_python3}
%patch11 -p1 -b .py3
%endif

# Short term fixes (usually gcc and backports)
%if 0%{?fedora}
%patch52 -p1 -b .unbundle-zlib
%endif
%patch59 -p1 -b .CouponDB-include
%patch61 -p1 -b .CommandLine-include
%patch62 -p1 -b .RestrictedCookieManager-tuple
%patch63 -p1 -b .DrmRenderNodePathFinder-include
%patch65 -p1 -b .java-only-allowed
# %%patch68 -p1 -b .aarch64-clearkeycdm-binutils-workaround
%if 0%{?fedora} >= 35
%patch76 -p1 -b .sigstkszfix
%endif
%patch79 -p1 -b .widevine-no-download
%patch80 -p1 -b .EnumTable-crash
%patch86 -p1 -b .clang-format-py3
%patch95 -p1 -b .mojo-header-fix
%patch96 -p1 -b .webrtc-BUILD.gn-fix-multiple-defines
%patch98 -p1 -b .InkDropHost-crash

# Feature specific patches
%if %{use_vaapi}
%patch202 -p1 -b .accel-mjpeg
%ifarch i686
%patch203 -p1 -b .i686permissive
%endif
%patch205 -p1 -b .vaapi-intel-fix
%endif

# Always disable gnome keyring
%patch300 -p1 -b .disblegnomekeyring

# glibc fix
%patch400 -p1 -b .glibc-2.34
%patch401 -p1 -b .virtualcursor

# cflags
%if 0%{?fedora} < 35
%patch403 -p1 -b .clang-12-cflags
%endif
%patch404 -p1 -b .clang-sanitizer-cflags

# RPM Fusion patches [free/chromium-freeworld]:
%patch503 -p1 -b .manpage

# RPM Fusion patches [free/chromium-browser-privacy]:
%patch600 -p1 -b .default-user-dir

# ungoogled-chromium platform patches
%patch700 -p1 -b .ungoogled-pref-fix

# Change shebang in all relevant files in this directory and all subdirectories
# See `man find` for how the `-exec command {} +` syntax works
%if 0%{?build_with_python3}
find -type f -exec sed -iE '1s=^#! */usr/bin/\(python\|env python\)[23]\?=#!%{__python3}=' {} +
%else
find -type f -exec sed -iE '1s=^#! */usr/bin/\(python\|env python\)[23]\?=#!%{__python2}=' {} +
%endif

export AR=${AR:=llvm-ar}
export NM=${NM:=llvm-nm}
export CC=${CC:=clang}
export CXX=${CXX:=clang++}
%if %{ccache}
export CCACHE_CPP2=yes
export CCACHE_SLOPPINESS=time_macros
%endif

rm -rf buildtools/third_party/libc++/BUILD.gn

# Unpack fonts
%if %{freeworld}
# no font fun needed.
%else
pushd third_party/test_fonts
mkdir test_fonts
cd test_fonts
unzip %{SOURCE14}
tar xf %{SOURCE15}
mv MuktiNarrow0.94/MuktiNarrow.ttf .
rm -rf MuktiNarrow0.94
cp %{SOURCE16} .
cp %{SOURCE17} .
cp %{SOURCE18} .
cp -a /usr/share/fonts/google-arimo-fonts/Arimo-*.ttf .
cp -a /usr/share/fonts/google-cousine-fonts/Cousine-*.ttf .
cp -a /usr/share/fonts/google-tinos-fonts/Tinos-*.ttf .
cp -a /usr/share/fonts/lohit-gurmukhi/Lohit-Gurmukhi.ttf .
cp -a /usr/share/fonts/google-noto-cjk/NotoSansCJKjp-Regular.otf .
cp -a /usr/share/fonts/dejavu-sans-fonts/DejaVuSans.ttf /usr/share/fonts/dejavu-sans-fonts/DejaVuSans-Bold.ttf .
cp -a /usr/share/fonts/thai-scalable/Garuda.otf .
sed -i 's|Garuda.ttf|Garuda.otf|g' ../BUILD.gn
cp -a /usr/share/fonts/lohit-devanagari/Lohit-Devanagari.ttf /usr/share/fonts/lohit-tamil/Lohit-Tamil.ttf .
cp -a /usr/share/fonts/google-noto/NotoSansKhmer-Regular.ttf .
cp -a /usr/share/fonts/google-noto-emoji/NotoColorEmoji.ttf .
cp -a /usr/share/fonts/google-noto/NotoSansSymbols2-Regular.ttf .
cp -a %{SOURCE115} .
popd
%endif

# Core defines are flags that are true for both the browser and headless.
UNGOOGLED_CHROMIUM_GN_DEFINES=''
UNGOOGLED_CHROMIUM_GN_DEFINES+=' is_debug=false is_unsafe_developer_build=false dcheck_always_on=false'
%ifarch x86_64 aarch64
UNGOOGLED_CHROMIUM_GN_DEFINES+=' system_libdir="lib64" clang_base_path="/usr"'
%endif
%if %{official_build}
UNGOOGLED_CHROMIUM_GN_DEFINES+=' is_official_build=true use_thin_lto=true is_cfi=true'
sed -i 's|OFFICIAL_BUILD|GOOGLE_CHROME_BUILD|g' tools/generate_shim_headers/generate_shim_headers.py
%endif
UNGOOGLED_CHROMIUM_GN_DEFINES+=' google_api_key="%{api_key}" google_default_client_id="%{default_client_id}" google_default_client_secret="%{default_client_secret}"'
UNGOOGLED_CHROMIUM_GN_DEFINES+=' is_clang=true clang_use_chrome_plugins=false use_sysroot=false disable_fieldtrial_testing_config=true use_lld=true rtc_enable_symbol_export=true'
UNGOOGLED_CHROMIUM_GN_DEFINES+=' use_gold=false'

%if %{freeworld}
UNGOOGLED_CHROMIUM_GN_DEFINES+=' ffmpeg_branding="ChromeOS" proprietary_codecs=true'
%else
UNGOOGLED_CHROMIUM_GN_DEFINES+=' ffmpeg_branding="Chromium" proprietary_codecs=false'
%endif
UNGOOGLED_CHROMIUM_GN_DEFINES+=' treat_warnings_as_errors=false'
UNGOOGLED_CHROMIUM_GN_DEFINES+=' use_custom_libcxx=false'
%ifarch aarch64
UNGOOGLED_CHROMIUM_GN_DEFINES+=' target_cpu="arm64"'
%endif
UNGOOGLED_CHROMIUM_GN_DEFINES+=' use_gnome_keyring=false'
UNGOOGLED_CHROMIUM_GN_DEFINES+=' use_gio=true use_pulseaudio=true icu_use_data_file=true'
UNGOOGLED_CHROMIUM_GN_DEFINES+=' enable_nacl=false'
UNGOOGLED_CHROMIUM_GN_DEFINES+=' is_component_ffmpeg=false is_component_build=false'
UNGOOGLED_CHROMIUM_GN_DEFINES+=' enable_hangout_services_extension=false'
%if %{debug_pkg}
UNGOOGLED_CHROMIUM_GN_DEFINES+=' blink_symbol_level=1 symbol_level=1 exclude_unwind_tables=false'
%else
UNGOOGLED_CHROMIUM_GN_DEFINES+=' blink_symbol_level=0 symbol_level=0 exclude_unwind_tables=true'
%endif
UNGOOGLED_CHROMIUM_GN_DEFINES+=' enable_widevine=true'
%if %{use_vaapi}
UNGOOGLED_CHROMIUM_GN_DEFINES+=' use_vaapi=true'
%else
UNGOOGLED_CHROMIUM_GN_DEFINES+=' use_vaapi=false'
%endif
UNGOOGLED_CHROMIUM_GN_DEFINES+=' rtc_use_pipewire=true rtc_link_pipewire=true'
%if %{ccache}
UNGOOGLED_CHROMIUM_GN_DEFINES+=' cc_wrapper="ccache"'
%endif
UNGOOGLED_CHROMIUM_GN_DEFINES+=' chrome_pgo_phase=0 enable_js_type_check=false enable_mse_mpeg2ts_stream_parser=true enable_nacl_nonsfi=false enable_one_click_signin=false enable_reading_list=false enable_remoting=false enable_reporting=false enable_service_discovery=false safe_browsing_mode=0'
export UNGOOGLED_CHROMIUM_GN_DEFINES

# ungoogled-chromium: binary pruning.
python3 -B %{ungoogled_chromium_root}/utils/prune_binaries.py . %{ungoogled_chromium_root}/pruning.list || true

mkdir -p third_party/node/linux/node-linux-x64/bin
ln -s %{_bindir}/node third_party/node/linux/node-linux-x64/bin/node

# Remove most of the bundled libraries. Libraries specified below (taken from
# Gentoo's Chromium ebuild) are the libraries that needs to be preserved.
build/linux/unbundle/remove_bundled_libraries.py \
	'base/third_party/cityhash' \
	'base/third_party/cityhash_v103' \
	'base/third_party/double_conversion' \
	'base/third_party/dynamic_annotations' \
	'base/third_party/icu' \
	'base/third_party/libevent' \
	'base/third_party/nspr' \
	'base/third_party/superfasthash' \
	'base/third_party/symbolize' \
	'base/third_party/valgrind' \
	'base/third_party/xdg_mime' \
	'base/third_party/xdg_user_dirs' \
	'buildtools/third_party/eu-strip' \
	'buildtools/third_party/libc++' \
	'buildtools/third_party/libc++abi' \
	'chrome/third_party/mozilla_security_manager' \
	'courgette/third_party' \
	'net/third_party/mozilla_security_manager' \
	'net/third_party/nss' \
	'net/third_party/quiche' \
	'net/third_party/uri_template' \
	'third_party/abseil-cpp' \
	'third_party/angle' \
	'third_party/angle/src/common/third_party/base' \
	'third_party/angle/src/common/third_party/smhasher' \
	'third_party/angle/src/common/third_party/xxhash' \
	'third_party/angle/src/third_party/libXNVCtrl' \
	'third_party/angle/src/third_party/trace_event' \
	'third_party/angle/src/third_party/volk' \
	'third_party/apple_apsl' \
	'third_party/axe-core' \
	'third_party/blanketjs' \
	'third_party/blink' \
	'third_party/boringssl' \
	'third_party/boringssl/src/third_party/fiat' \
	'third_party/breakpad' \
	'third_party/breakpad/breakpad/src/third_party/curl' \
	'third_party/brotli' \
	'third_party/catapult' \
	'third_party/catapult/common/py_vulcanize/third_party/rcssmin' \
	'third_party/catapult/common/py_vulcanize/third_party/rjsmin' \
	'third_party/catapult/third_party/beautifulsoup4' \
	'third_party/catapult/third_party/google-endpoints' \
	'third_party/catapult/third_party/html5lib-python' \
	'third_party/catapult/third_party/polymer' \
	'third_party/catapult/third_party/six' \
	'third_party/catapult/tracing/third_party/d3' \
	'third_party/catapult/tracing/third_party/gl-matrix' \
	'third_party/catapult/tracing/third_party/jpeg-js' \
	'third_party/catapult/tracing/third_party/jszip' \
	'third_party/catapult/tracing/third_party/mannwhitneyu' \
	'third_party/catapult/tracing/third_party/oboe' \
	'third_party/catapult/tracing/third_party/pako' \
    'third_party/ced' \
	'third_party/cld_3' \
	'third_party/closure_compiler' \
	'third_party/crashpad' \
	'third_party/crashpad/crashpad/third_party/lss' \
	'third_party/crashpad/crashpad/third_party/zlib/' \
	'third_party/crc32c' \
	'third_party/cros_system_api' \
	'third_party/dav1d' \
	'third_party/dawn' \
	'third_party/dawn/third_party/khronos' \
    'third_party/dawn/third_party/tint' \
	'third_party/depot_tools' \
	'third_party/devscripts' \
	'third_party/devtools-frontend' \
	'third_party/devtools-frontend/src/third_party/typescript' \
	'third_party/devtools-frontend/src/front_end/third_party/acorn' \
	'third_party/devtools-frontend/src/front_end/third_party/axe-core' \
	'third_party/devtools-frontend/src/front_end/third_party/chromium' \
	'third_party/devtools-frontend/src/front_end/third_party/codemirror' \
	'third_party/devtools-frontend/src/front_end/third_party/diff' \
	'third_party/devtools-frontend/src/front_end/third_party/i18n' \
	'third_party/devtools-frontend/src/front_end/third_party/intl-messageformat' \
	'third_party/devtools-frontend/src/front_end/third_party/lighthouse' \
	'third_party/devtools-frontend/src/front_end/third_party/lit-html' \
	'third_party/devtools-frontend/src/front_end/third_party/lodash-isequal' \
	'third_party/devtools-frontend/src/front_end/third_party/marked' \
	'third_party/devtools-frontend/src/front_end/third_party/puppeteer' \
	'third_party/devtools-frontend/src/front_end/third_party/wasmparser' \
	'third_party/devtools-frontend/src/test/unittests/front_end/third_party/i18n' \
	'third_party/devtools-frontend/src/third_party' \
	'third_party/distributed_point_functions' \
	'third_party/dom_distiller_js' \
	'third_party/eigen3' \
	'third_party/emoji-segmenter' \
	'third_party/expat' \
	'third_party/farmhash' \
	'third_party/fdlibm' \
	'third_party/ffmpeg' \
	'third_party/fft2d' \
	'third_party/flac' \
    'third_party/flatbuffers' \
	'third_party/fontconfig' \
	'third_party/freetype' \
	'third_party/fusejs' \
	'third_party/gemmlowp' \
	'third_party/google_input_tools' \
	'third_party/google_input_tools/third_party/closure_library' \
	'third_party/google_input_tools/third_party/closure_library/third_party/closure' \
	'third_party/google_trust_services' \
	'third_party/googletest' \
	'third_party/grpc' \
	'third_party/harfbuzz-ng' \
	'third_party/highway' \
	'third_party/hunspell' \
	'third_party/iccjpeg' \
	'third_party/icu' \
	'third_party/inspector_protocol' \
	'third_party/jinja2' \
	'third_party/jsoncpp' \
	'third_party/jstemplate' \
	'third_party/khronos' \
	'third_party/leveldatabase' \
	'third_party/libXNVCtrl' \
	'third_party/libaddressinput' \
	'third_party/libaom' \
	'third_party/libaom/source/libaom/third_party/fastfeat' \
	'third_party/libaom/source/libaom/third_party/vector' \
	'third_party/libaom/source/libaom/third_party/x86inc' \
	'third_party/libavif' \
	'third_party/libdrm' \
	'third_party/libgav1' \
	'third_party/libgifcodec' \
	'third_party/libjingle' \
	'third_party/libjpeg_turbo' \
	'third_party/libjxl' \
	'third_party/libphonenumber' \
	'third_party/libpng' \
	'third_party/libsecret' \
    'third_party/libsrtp' \
	'third_party/libsync' \
	'third_party/libudev' \
	'third_party/liburlpattern' \
	'third_party/libusb' \
	'third_party/libva_protected_content' \
	'third_party/libvpx' \
	'third_party/libvpx/source/libvpx/third_party/x86inc' \
	'third_party/libwebm' \
	'third_party/libwebp' \
	'third_party/libx11' \
	'third_party/libxcb-keysyms' \
	'third_party/libxml' \
	'third_party/libxml/chromium' \
	'third_party/libxslt' \
	'third_party/libyuv' \
	'third_party/libzip' \
	'third_party/lottie' \
	'third_party/lss' \
	'third_party/lzma_sdk' \
	'third_party/mako' \
	'third_party/maldoca' \
	'third_party/maldoca/src/third_party/tensorflow_protos' \
	'third_party/maldoca/src/third_party/zlibwrapper' \
	'third_party/markupsafe' \
	'third_party/mesa' \
	'third_party/metrics_proto' \
	'third_party/minigbm' \
	'third_party/modp_b64' \
	'third_party/nasm' \
	'third_party/nearby' \
    'third_party/neon_2_sse' \
	'third_party/node' \
	'third_party/node/node_modules/polymer-bundler/lib/third_party/UglifyJS2' \
	'third_party/one_euro_filter' \
	'third_party/opencv' \
%if %{freeworld}
	'third_party/openh264' \
%endif
	'third_party/openscreen' \
	'third_party/openscreen/src/third_party/mozilla' \
	'third_party/openscreen/src/third_party/tinycbor' \
	'third_party/opus' \
	'third_party/ots' \
	'third_party/pdfium' \
	'third_party/pdfium/third_party/agg23' \
	'third_party/pdfium/third_party/base' \
	'third_party/pdfium/third_party/bigint' \
	'third_party/pdfium/third_party/freetype' \
	'third_party/pdfium/third_party/lcms' \
	'third_party/pdfium/third_party/libopenjpeg20' \
    'third_party/pdfium/third_party/libpng16' \
    'third_party/pdfium/third_party/libtiff' \
	'third_party/pdfium/third_party/skia_shared' \
	'third_party/perfetto' \
	'third_party/perfetto/protos/third_party/chromium' \
	'third_party/pffft' \
    'third_party/ply' \
	'third_party/polymer' \
	'third_party/private-join-and-compute' \
	'third_party/private_membership' \
	'third_party/protobuf' \
	'third_party/protobuf/third_party/six' \
	'third_party/pyjson5' \
	'third_party/qcms' \
	'third_party/qunit' \
%if 0%{?bundlere2}
	'third_party/re2' \
%endif
	'third_party/rnnoise' \
	'third_party/ruy' \
	'third_party/s2cellid' \
	'third_party/securemessage' \
	'third_party/shell-encryption' \
	'third_party/simplejson' \
	'third_party/sinonjs' \
	'third_party/skia' \
	'third_party/skia/include/third_party/skcms' \
	'third_party/skia/include/third_party/vulkan' \
	'third_party/skia/third_party/skcms' \
	'third_party/skia/third_party/vulkan' \
	'third_party/smhasher' \
	'third_party/snappy' \
	'third_party/speech-dispatcher' \
	'third_party/sqlite' \
	'third_party/swiftshader' \
	'third_party/swiftshader/third_party/astc-encoder' \
	'third_party/swiftshader/third_party/llvm-subzero' \
	'third_party/swiftshader/third_party/llvm-10.0' \
	'third_party/swiftshader/third_party/marl' \
	'third_party/swiftshader/third_party/subzero' \
	'third_party/swiftshader/third_party/SPIRV-Headers' \
	'third_party/tcmalloc' \
	'third_party/tensorflow-text' \
	'third_party/test_fonts' \
	'third_party/tflite' \
	'third_party/tflite/src/third_party/eigen3' \
	'third_party/tflite/src/third_party/fft2d' \
	'third_party/tflite_support' \
	'third_party/ukey2' \
    'third_party/usb_ids' \
	'third_party/usrsctp' \
	'third_party/utf' \
	'third_party/vulkan' \
	'third_party/wayland' \
	'third_party/web-animations-js' \
	'third_party/webdriver' \
	'third_party/webgpu-cts' \
	'third_party/webrtc' \
	'third_party/webrtc/common_audio/third_party/ooura' \
	'third_party/webrtc/common_audio/third_party/spl_sqrt_floor' \
	'third_party/webrtc/modules/third_party/fft' \
	'third_party/webrtc/modules/third_party/g711' \
	'third_party/webrtc/modules/third_party/g722' \
	'third_party/webrtc/rtc_base/third_party/base64' \
	'third_party/webrtc/rtc_base/third_party/sigslot' \
	'third_party/widevine' \
    'third_party/woff2' \
	'third_party/wuffs' \
	'third_party/x11proto' \
	'third_party/xcbproto' \
    'third_party/xdg-utils' \
	'third_party/zxcvbn-cpp' \
    'third_party/zlib' \
	'third_party/zlib/google' \
	'tools/gn/src/base/third_party/icu' \
	'url/third_party/mozilla' \
	'v8/src/third_party/siphash' \
	'v8/src/third_party/utf8-decoder' \
	'v8/src/third_party/valgrind' \
	'v8/third_party/v8' \
	'v8/third_party/inspector_protocol' \
	--do-remove

export PATH=$PATH:%{_builddir}/depot_tools

build/linux/unbundle/replace_gn_files.py --system-libraries \
%if 0%{?bundlefontconfig}
%else
	fontconfig \
%endif
%if 0%{?bundlefreetype}
%else
	freetype \
%endif
%if 0%{?bundleharfbuzz}
%else
	harfbuzz-ng \
%endif
%if 0%{?bundleicu}
%else
	icu \
%endif
%if %{bundlelibdrm}
%else
	libdrm \
%endif
%if %{bundlelibjpeg}
%else
	libjpeg \
%endif
%if %{bundlelibpng}
%else
	libpng \
%endif
%if %{bundlelibusbx}
%else
	libusb \
%endif
%if %{bundlelibwebp}
%else
	libwebp \
%endif
%if %{bundlelibxml}
%else
	libxml \
%endif
	libxslt \
%if %{bundleopus}
%else
	opus \
%endif
%if 0%{?bundlere2}
%else
	re2 \
%endif
%if 0%{?bundleminizip}
%else
	zlib \
%endif
	flac

# fix arm gcc
sed -i 's|arm-linux-gnueabihf-|arm-linux-gnu-|g' build/toolchain/linux/BUILD.gn

%ifarch aarch64
# We don't need to cross compile while building on an aarch64 system.
sed -i 's|aarch64-linux-gnu-||g' build/toolchain/linux/BUILD.gn

# Correct the ninja file to check for aarch64, not just x86.
sed -i '/${LONG_BIT}/ a \      aarch64)\' ../depot_tools/ninja
sed -i '/aarch64)/ a \        exec "/usr/bin/ninja-build" "$@";;\' ../depot_tools/ninja
%endif
sed -i 's|exec "${THIS_DIR}/ninja-linux${LONG_BIT}"|exec "/usr/bin/ninja-build"|g' ../depot_tools/ninja

# Get rid of the pre-built eu-strip binary, it is x86_64 and of mysterious origin
rm -rf buildtools/third_party/eu-strip/bin/eu-strip
# Replace it with a symlink to the Fedora copy
ln -s %{_bindir}/eu-strip buildtools/third_party/eu-strip/bin/eu-strip

# Check that there is no system 'google' module, shadowing bundled ones:
%if 0%{?build_with_python3}
if python3 -c 'import google ; print google.__path__' 2> /dev/null ; then \
    echo "Python 3 'google' module is defined, this will shadow modules of this build"; \
%else
if python2 -c 'import google ; print google.__path__' 2> /dev/null ; then \
    echo "Python 2 'google' module is defined, this will shadow modules of this build"; \
%endif
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

tools/gn/bootstrap/bootstrap.py --gn-gen-args="$UNGOOGLED_CHROMIUM_GN_DEFINES"
%{builddir}/gn --script-executable=%{chromium_pybin} gen --args="$UNGOOGLED_CHROMIUM_GN_DEFINES" %{builddir}

%if %{bundlelibusbx}
# no hackity hack hack
%else
# hackity hack hack
rm -rf third_party/libusb/src/libusb/libusb.h
# we _shouldn't need to do this, but it looks like we do.
cp -a %{_includedir}/libusb-1.0/libusb.h third_party/libusb/src/libusb/libusb.h
%endif

# Hard code extra version
FILE=chrome/common/channel_info_posix.cc
sed -i.orig -e 's/getenv("CHROME_VERSION_EXTRA")/"Ungoogled Chromium"/' $FILE

%build
# Turning the buildsystem up to 11.
ulimit -n 4096

# unpack a local copy of the xcb-proto bits
tar xf %{SOURCE20}

# export PYTHONPATH="../../third_party/pyjson5/src:../../third_party/catapult/third_party/google-endpoints:../../xcb-proto-1.14"
export PYTHONPATH="../../third_party/pyjson5/src:../../xcb-proto-1.14:../../third_party/catapult/third_party/html5lib-1.1"

echo
# Now do the full browser
%build_target %{builddir} chrome
%build_target %{builddir} chrome_sandbox
%build_target %{builddir} chromedriver
%if %{build_clear_key_cdm}
%build_target %{builddir} clear_key_cdm
%endif
%build_target %{builddir} policy_templates

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{chromium_path}
cp -a %{SOURCE3} %{buildroot}%{chromium_path}/%{chromium_browser_channel}.sh
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

ln -s %{chromium_path}/%{chromium_browser_channel}.sh %{buildroot}%{_bindir}/%{chromium_browser_channel}
mkdir -p %{buildroot}%{_mandir}/man1/

pushd %{builddir}
    cp -a *.pak locales resources icudtl.dat %{buildroot}%{chromium_path}
    %ifarch x86_64 i686 aarch64
        cp -a swiftshader %{buildroot}%{chromium_path}
    %endif
    cp -a chrome %{buildroot}%{chromium_path}/%{chromium_browser_channel}
    cp -a chrome_sandbox %{buildroot}%{chromium_path}/chrome-sandbox
    cp -a chrome_crashpad_handler %{buildroot}%{chromium_path}/chrome_crashpad_handler
    cp -a ../../chrome/app/resources/manpage.1.in %{buildroot}%{_mandir}/man1/%{chromium_browser_channel}.1
    sed -i "s|@@PACKAGE@@|%{chromium_browser_channel}|g" %{buildroot}%{_mandir}/man1/%{chromium_browser_channel}.1
    sed -i "s|@@MENUNAME@@|%{chromium_menu_name}|g" %{buildroot}%{_mandir}/man1/%{chromium_browser_channel}.1
    # V8 initial snapshots
    # https://code.google.com/p/chromium/issues/detail?id=421063
    cp -a snapshot_blob.bin %{buildroot}%{chromium_path}
    cp -a v8_context_snapshot.bin %{buildroot}%{chromium_path}
    cp -a xdg-mime xdg-settings %{buildroot}%{chromium_path}
    # This is ANGLE, not to be confused with the similarly named files under swiftshader/
    cp -a libEGL.so* libGLESv2.so* %{buildroot}%{chromium_path}

    %if %{build_clear_key_cdm}
        %ifarch i686
            cp -a ClearKeyCdm/_platform_specific/linux_x86/libclearkeycdm.so %{buildroot}%{chromium_path}
        %else
            %ifarch x86_64
                cp -a ClearKeyCdm/_platform_specific/linux_x64/libclearkeycdm.so %{buildroot}%{chromium_path}
            %else
                %ifarch aarch64
                    cp -a ClearKeyCdm/_platform_specific/linux_arm64/libclearkeycdm.so %{buildroot}%{chromium_path}
                %else
                    cp -a libclearkeycdm.so %{buildroot}%{chromium_path}
                %endif
            %endif
        %endif
    %endif

    # chromedriver
    cp -a chromedriver %{buildroot}%{chromium_path}/chromedriver
    ln -s %{chromium_path}/chromedriver %{buildroot}%{_bindir}/chromedriver
popd

# Add directories for policy management
mkdir -p %{buildroot}%{_sysconfdir}/chromium/policies/managed
mkdir -p %{buildroot}%{_sysconfdir}/chromium/policies/recommended

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
mkdir -p %{buildroot}%{_sysconfdir}/%{name}
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
%config %{_sysconfdir}/%{name}/
# %%dir %%{_sysconfdir}/%%{name}/native-messaging-hosts
%{_bindir}/%{chromium_browser_channel}
%dir %{chromium_path}
%{chromium_path}/*.bin
%{chromium_path}/chrome_*.pak
%{chromium_path}/chrome_crashpad_handler
%{chromium_path}/resources.pak
%{chromium_path}/icudtl.dat
%{chromium_path}/%{chromium_browser_channel}
%attr(0755, root, root) %{chromium_path}/%{chromium_browser_channel}.sh
%{chromium_path}/libEGL.so*
%{chromium_path}/libGLESv2.so*
%ifarch x86_64 i686 aarch64
%{chromium_path}/swiftshader/
%endif
%attr(4755, root, root) %{chromium_path}/chrome-sandbox
%{chromium_path}/xdg-mime
%{chromium_path}/xdg-settings
%{_mandir}/man1/%{chromium_browser_channel}.*
%{_datadir}/icons/hicolor/*/apps/%{chromium_browser_channel}.png
%{_datadir}/applications/*.desktop
%{_datadir}/metainfo/*.appdata.xml
%{_datadir}/gnome-control-center/default-apps/ungoogled-chromium.xml

%{chromium_path}/headless_*.pak
%if %{build_clear_key_cdm}
%{chromium_path}/libclearkeycdm.so
%endif
%{chromium_path}/resources/
%dir %{chromium_path}/locales/
%lang(am) %{chromium_path}/locales/am.pak*
%lang(ar) %{chromium_path}/locales/ar.pak*
%lang(bg) %{chromium_path}/locales/bg.pak*
%lang(bn) %{chromium_path}/locales/bn.pak*
%lang(ca) %{chromium_path}/locales/ca.pak*
%lang(cs) %{chromium_path}/locales/cs.pak*
%lang(da) %{chromium_path}/locales/da.pak*
%lang(de) %{chromium_path}/locales/de.pak*
%lang(el) %{chromium_path}/locales/el.pak*
%lang(en_GB) %{chromium_path}/locales/en-GB.pak*
# Chromium _ALWAYS_ needs en-US.pak as a fallback
# This means we cannot apply the lang code here.
# Otherwise, it is filtered out on install.
%{chromium_path}/locales/en-US.pak*
%lang(es) %{chromium_path}/locales/es.pak*
%lang(es) %{chromium_path}/locales/es-419.pak*
%lang(et) %{chromium_path}/locales/et.pak*
%lang(fa) %{chromium_path}/locales/fa.pak*
%lang(fi) %{chromium_path}/locales/fi.pak*
%lang(fil) %{chromium_path}/locales/fil.pak*
%lang(fr) %{chromium_path}/locales/fr.pak*
%lang(gu) %{chromium_path}/locales/gu.pak*
%lang(he) %{chromium_path}/locales/he.pak*
%lang(hi) %{chromium_path}/locales/hi.pak*
%lang(hr) %{chromium_path}/locales/hr.pak*
%lang(hu) %{chromium_path}/locales/hu.pak*
%lang(id) %{chromium_path}/locales/id.pak*
%lang(it) %{chromium_path}/locales/it.pak*
%lang(ja) %{chromium_path}/locales/ja.pak*
%lang(kn) %{chromium_path}/locales/kn.pak*
%lang(ko) %{chromium_path}/locales/ko.pak*
%lang(lt) %{chromium_path}/locales/lt.pak*
%lang(lv) %{chromium_path}/locales/lv.pak*
%lang(ml) %{chromium_path}/locales/ml.pak*
%lang(mr) %{chromium_path}/locales/mr.pak*
%lang(ms) %{chromium_path}/locales/ms.pak*
%lang(nb) %{chromium_path}/locales/nb.pak*
%lang(nl) %{chromium_path}/locales/nl.pak*
%lang(pl) %{chromium_path}/locales/pl.pak*
%lang(pt_BR) %{chromium_path}/locales/pt-BR.pak*
%lang(pt_PT) %{chromium_path}/locales/pt-PT.pak*
%lang(ro) %{chromium_path}/locales/ro.pak*
%lang(ru) %{chromium_path}/locales/ru.pak*
%lang(sk) %{chromium_path}/locales/sk.pak*
%lang(sl) %{chromium_path}/locales/sl.pak*
%lang(sr) %{chromium_path}/locales/sr.pak*
%lang(sv) %{chromium_path}/locales/sv.pak*
%lang(sw) %{chromium_path}/locales/sw.pak*
%lang(ta) %{chromium_path}/locales/ta.pak*
%lang(te) %{chromium_path}/locales/te.pak*
%lang(th) %{chromium_path}/locales/th.pak*
%lang(tr) %{chromium_path}/locales/tr.pak*
%lang(uk) %{chromium_path}/locales/uk.pak*
%lang(vi) %{chromium_path}/locales/vi.pak*
%lang(zh_CN) %{chromium_path}/locales/zh-CN.pak*
%lang(zh_TW) %{chromium_path}/locales/zh-TW.pak*
# These are psuedolocales, not real ones.
# They only get generated when is_official_build=false
%if !%{official_build}
%{chromium_path}/locales/ar-XB.pak*
%{chromium_path}/locales/en-XA.pak*
%endif

%{_bindir}/chromedriver
%{chromium_path}/chromedriver

%changelog
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
