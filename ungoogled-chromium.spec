%define _lto_cflags %{nil}

%global numjobs 14
%ifarch aarch64
%global numjobs 12
%endif

# This flag is so I can build things very fast on a giant system.
# Do not enable in Koji builds.
# Doesn't work on RHEL 7
%if 0%{?rhel} == 7
%global use_all_cpus 0
%else
%global use_all_cpus 1
%endif

%if %{use_all_cpus}
%global numjobs %{_smp_build_ncpus}
%endif

# Fancy build status, so we at least know, where we are..
# %1 where
# %2 what
%global build_target() \
	export NINJA_STATUS="[%2:%f/%t] " ; \
	../depot_tools/ninja -j %{numjobs} -C '%1' -vvv '%2'

# We'd like to always have this on...
# ... but the libva in EL7 is too old.
%if 0%{?rhel} == 7
%global use_vaapi 0
%else
%global use_vaapi 1
%endif

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
%global chromium_browser_channel %{name}%{chromium_channel}
%global chromium_path %{_libdir}/%{name}%{chromium_channel}

# We don't want any libs in these directories to generate Provides
# Requires is trickier.

# To generate this list, go into %%{buildroot}%%{chromium_path} and run
# for i in `find . -name "*.so" | sort`; do NAME=`basename -s .so $i`; printf "$NAME|"; done
# for RHEL7, append libfontconfig to the end
# make sure there is not a trailing | at the end of the list

%global __provides_exclude_from %{chromium_path}/.*\\.so|%{chromium_path}/lib/.*\\.so|%{chromium_path}/lib/.*\\.so.*
%if 0%{?rhel} == 7
%global privlibs libaccessibility|libandroid_mojo_bindings_shared|libanimation|libapdu|libaura|libaura_extra|libauthenticator_test_mojo_bindings_shared|libbase|libbase_i18n|libbindings|libbindings_base|libblink_common|libblink_controller|libblink_core|libblink_embedded_frame_sink_mojo_bindings_shared|libblink_features|libblink_modules|libblink_mojom_broadcastchannel_bindings_shared|libblink_platform|libbluetooth|libboringssl|libbrowser_ui_views|libcaptive_portal|libcapture_base|libcapture_lib|libcbor|libcc|libcc_animation|libcc_base|libcc_debug|libcc_ipc|libcc_mojo_embedder|libcc_paint|libcertificate_matching|libcert_verifier|libchrome_features|libchromium_sqlite3|libclearkeycdm|libclient|libcloud_policy_proto_generated_compile|libcodec|libcolor_space|libcolor_utils|libcommon|libcompositor|libcontent|libcontent_common_mojo_bindings_shared|libcontent_public_common_mojo_bindings_shared|libcontent_service_cpp|libcontent_service_mojom|libcontent_service_mojom_shared|libcontent_settings_features|libcrash_key_lib|libcrcrypto|libcrdtp|libdbus|libdevice_base|libdevice_event_log|libdevice_features|libdevice_gamepad|libdevices|libdevice_vr|libdevice_vr_mojo_bindings|libdevice_vr_mojo_bindings_blink|libdevice_vr_mojo_bindings_shared|libdevice_vr_test_mojo_bindings|libdevice_vr_test_mojo_bindings_blink|libdevice_vr_test_mojo_bindings_shared|libdiscardable_memory_client|libdiscardable_memory_common|libdiscardable_memory_service|libdisplay|libdisplay_types|libdisplay_util|libdomain_reliability|libdom_storage_mojom|libdom_storage_mojom_shared|libEGL|libEGL|libembedder|libembedder_switches|libevents|libevents_base|libevents_devices_x11|libevents_ozone_layout|libevents_x|libextras|libffmpeg|libfido|libfingerprint|libfreetype_harfbuzz|libgamepad_mojom|libgamepad_mojom_blink|libgamepad_mojom_shared|libgamepad_shared_typemap_traits|libgcm|libgeometry|libgeometry_skia|libgesture_detection|libgfx|libgfx_ipc|libgfx_ipc_buffer_types|libgfx_ipc_color|libgfx_ipc_geometry|libgfx_ipc_skia|libgfx_switches|libgfx_x11|libgin|libgles2|libgles2_implementation|libgles2_utils|libGLESv2|libGLESv2|libgl_init|libgl_in_process_context|libgl_wrapper|libgpu|libgpu_ipc_service|libgtkui|libheadless_non_renderer|libhost|libicui18n|libicuuc|libinterfaces_shared|libipc|libipc_mojom|libipc_mojom_shared|libkeycodes_x11|libkeyed_service_content|libkeyed_service_core|liblearning_common|liblearning_impl|libleveldatabase|libleveldb_proto|libmanager|libmedia|libmedia_blink|libmedia_gpu|libmedia_learning_mojo_impl|libmedia_message_center|libmedia_mojo_services|libmedia_session_base_cpp|libmedia_session_cpp|libmedia_webrtc|libmemory_instrumentation|libmenu|libmessage_center|libmessage_support|libmetrics_cpp|libmidi|libmirroring_service|libmojo_base_lib|libmojo_base_mojom|libmojo_base_mojom_blink|libmojo_base_mojom_shared|libmojo_base_shared_typemap_traits|libmojo_core_embedder|libmojo_core_embedder_internal|libmojo_core_ports|libmojo_cpp_platform|libmojom_core_shared|libmojom_mhtml_load_result_shared|libmojom_modules_shared|libmojo_mojom_bindings|libmojo_mojom_bindings_shared|libmojom_platform_shared|libmojo_public_system|libmojo_public_system_cpp|libnative_theme|libnet|libnetwork_cpp|libnetwork_cpp_base|libnetwork_service|libnetwork_session_configurator|libonc|libos_crypt|libparsers|libpdfium|libperfetto|libperformace_manager_public_mojom|libperformace_manager_public_mojom_blink|libperformace_manager_public_mojom_shared|libplatform|libplatform_window|libplatform_window_common|libplatform_window_handler_libs|libpolicy_component|libpolicy_proto|libppapi_host|libppapi_proxy|libppapi_shared|libprefs|libprinting|libproperties|libprotobuf_lite|libproxy_config|libpublic|librange|libraster|libresource_coordinator_public_mojom|libresource_coordinator_public_mojom_blink|libresource_coordinator_public_mojom_shared|libsandbox|libsandbox_services|libscheduling_metrics|libseccomp_bpf|libsecurity_state_features|libservice|libservice_manager_cpp|libservice_manager_cpp_types|libservice_manager_mojom|libservice_manager_mojom_blink|libservice_manager_mojom_constants|libservice_manager_mojom_constants_blink|libservice_manager_mojom_constants_shared|libservice_manager_mojom_shared|libservice_manager_mojom_traits|libservice_provider|libsessions|libshared_memory_support|libshared_with_blink|libshell_dialogs|libskia|libskia_shared_typemap_traits|libsnapshot|libsql|libstartup_tracing|libstorage_browser|libstorage_common|libstorage_service_public|libstub_window|libsuid_sandbox_client|libsurface|libsystem_media_controls|libtab_count_metrics|libthread_linux|libtracing|libtracing_cpp|libtracing_mojom|libtracing_mojom_shared|libui_accessibility_ax_mojom|libui_accessibility_ax_mojom_blink|libui_accessibility_ax_mojom_shared|libui_base|libui_base_clipboard|libui_base_clipboard_types|libui_base_features|libui_base_idle|libui_base_ime|libui_base_ime_init|libui_base_ime_linux|libui_base_ime_types|libui_base_x|libui_data_pack|libui_devtools|libui_message_center_cpp|libui_touch_selection|liburl|liburl_ipc|liburl_matcher|libusb_shared|libuser_manager|libuser_prefs|libv8|libv8_libbase|libv8_libplatform|libviews|libviz_common|libviz_resource_format_utils|libviz_vulkan_context_provider|libVkICD_mock_icd|libvk_swiftshader|libvr_base|libvr_common|libvulkan_info|libvulkan_init|libvulkan_wrapper|libvulkan_x11|libvulkan_ycbcr_info|libweb_bluetooth_mojo_bindings_shared|libwebdata_common|libweb_dialogs|libweb_feature_mojo_bindings_mojom|libweb_feature_mojo_bindings_mojom_blink|libweb_feature_mojo_bindings_mojom_shared|libwebgpu|libweb_modal|libwebrtc_component|libwebview|libwm|libwm_public|libwtf|libwtf_support|libx11_events_platform|libx11_window|libzygote|libfontconfig
%else
%global privlibs libaccessibility|libandroid_mojo_bindings_shared|libanimation|libapdu|libaura|libaura_extra|libauthenticator_test_mojo_bindings_shared|libbase|libbase_i18n|libbindings|libbindings_base|libblink_common|libblink_controller|libblink_core|libblink_embedded_frame_sink_mojo_bindings_shared|libblink_features|libblink_modules|libblink_mojom_broadcastchannel_bindings_shared|libblink_platform|libbluetooth|libboringssl|libbrowser_ui_views|libcaptive_portal|libcapture_base|libcapture_lib|libcbor|libcc|libcc_animation|libcc_base|libcc_debug|libcc_ipc|libcc_mojo_embedder|libcc_paint|libcertificate_matching|libcert_verifier|libchrome_features|libchromium_sqlite3|libclearkeycdm|libclient|libcloud_policy_proto_generated_compile|libcodec|libcolor_space|libcolor_utils|libcommon|libcompositor|libcontent|libcontent_common_mojo_bindings_shared|libcontent_public_common_mojo_bindings_shared|libcontent_service_cpp|libcontent_service_mojom|libcontent_service_mojom_shared|libcontent_settings_features|libcrash_key_lib|libcrcrypto|libcrdtp|libdbus|libdevice_base|libdevice_event_log|libdevice_features|libdevice_gamepad|libdevices|libdevice_vr|libdevice_vr_mojo_bindings|libdevice_vr_mojo_bindings_blink|libdevice_vr_mojo_bindings_shared|libdevice_vr_test_mojo_bindings|libdevice_vr_test_mojo_bindings_blink|libdevice_vr_test_mojo_bindings_shared|libdiscardable_memory_client|libdiscardable_memory_common|libdiscardable_memory_service|libdisplay|libdisplay_types|libdisplay_util|libdomain_reliability|libdom_storage_mojom|libdom_storage_mojom_shared|libEGL|libEGL|libembedder|libembedder_switches|libevents|libevents_base|libevents_devices_x11|libevents_ozone_layout|libevents_x|libextras|libffmpeg|libfido|libfingerprint|libfreetype_harfbuzz|libgamepad_mojom|libgamepad_mojom_blink|libgamepad_mojom_shared|libgamepad_shared_typemap_traits|libgcm|libgeometry|libgeometry_skia|libgesture_detection|libgfx|libgfx_ipc|libgfx_ipc_buffer_types|libgfx_ipc_color|libgfx_ipc_geometry|libgfx_ipc_skia|libgfx_switches|libgfx_x11|libgin|libgles2|libgles2_implementation|libgles2_utils|libGLESv2|libGLESv2|libgl_init|libgl_in_process_context|libgl_wrapper|libgpu|libgpu_ipc_service|libgtkui|libheadless_non_renderer|libhost|libicui18n|libicuuc|libinterfaces_shared|libipc|libipc_mojom|libipc_mojom_shared|libkeycodes_x11|libkeyed_service_content|libkeyed_service_core|liblearning_common|liblearning_impl|libleveldatabase|libleveldb_proto|libmanager|libmedia|libmedia_blink|libmedia_gpu|libmedia_learning_mojo_impl|libmedia_message_center|libmedia_mojo_services|libmedia_session_base_cpp|libmedia_session_cpp|libmedia_webrtc|libmemory_instrumentation|libmenu|libmessage_center|libmessage_support|libmetrics_cpp|libmidi|libmirroring_service|libmojo_base_lib|libmojo_base_mojom|libmojo_base_mojom_blink|libmojo_base_mojom_shared|libmojo_base_shared_typemap_traits|libmojo_core_embedder|libmojo_core_embedder_internal|libmojo_core_ports|libmojo_cpp_platform|libmojom_core_shared|libmojom_mhtml_load_result_shared|libmojom_modules_shared|libmojo_mojom_bindings|libmojo_mojom_bindings_shared|libmojom_platform_shared|libmojo_public_system|libmojo_public_system_cpp|libnative_theme|libnet|libnetwork_cpp|libnetwork_cpp_base|libnetwork_service|libnetwork_session_configurator|libonc|libos_crypt|libparsers|libpdfium|libperfetto|libperformace_manager_public_mojom|libperformace_manager_public_mojom_blink|libperformace_manager_public_mojom_shared|libplatform|libplatform_window|libplatform_window_common|libplatform_window_handler_libs|libpolicy_component|libpolicy_proto|libppapi_host|libppapi_proxy|libppapi_shared|libprefs|libprinting|libproperties|libprotobuf_lite|libproxy_config|libpublic|librange|libraster|libresource_coordinator_public_mojom|libresource_coordinator_public_mojom_blink|libresource_coordinator_public_mojom_shared|libsandbox|libsandbox_services|libscheduling_metrics|libseccomp_bpf|libsecurity_state_features|libservice|libservice_manager_cpp|libservice_manager_cpp_types|libservice_manager_mojom|libservice_manager_mojom_blink|libservice_manager_mojom_constants|libservice_manager_mojom_constants_blink|libservice_manager_mojom_constants_shared|libservice_manager_mojom_shared|libservice_manager_mojom_traits|libservice_provider|libsessions|libshared_memory_support|libshared_with_blink|libshell_dialogs|libskia|libskia_shared_typemap_traits|libsnapshot|libsql|libstartup_tracing|libstorage_browser|libstorage_common|libstorage_service_public|libstub_window|libsuid_sandbox_client|libsurface|libsystem_media_controls|libtab_count_metrics|libthread_linux|libtracing|libtracing_cpp|libtracing_mojom|libtracing_mojom_shared|libui_accessibility_ax_mojom|libui_accessibility_ax_mojom_blink|libui_accessibility_ax_mojom_shared|libui_base|libui_base_clipboard|libui_base_clipboard_types|libui_base_features|libui_base_idle|libui_base_ime|libui_base_ime_init|libui_base_ime_linux|libui_base_ime_types|libui_base_x|libui_data_pack|libui_devtools|libui_message_center_cpp|libui_touch_selection|liburl|liburl_ipc|liburl_matcher|libusb_shared|libuser_manager|libuser_prefs|libv8|libv8_libbase|libv8_libplatform|libviews|libviz_common|libviz_resource_format_utils|libviz_vulkan_context_provider|libVkICD_mock_icd|libvk_swiftshader|libvr_base|libvr_common|libvulkan_info|libvulkan_init|libvulkan_wrapper|libvulkan_x11|libvulkan_ycbcr_info|libweb_bluetooth_mojo_bindings_shared|libwebdata_common|libweb_dialogs|libweb_feature_mojo_bindings_mojom|libweb_feature_mojo_bindings_mojom_blink|libweb_feature_mojo_bindings_mojom_shared|libwebgpu|libweb_modal|libwebrtc_component|libwebview|libwm|libwm_public|libwtf|libwtf_support|libx11_events_platform|libx11_window|libzygote
%endif
%global __requires_exclude ^(%{privlibs})\\.so*



%if 0
# Chromium's fork of ICU is now something we can't unbundle.
# This is left here to ease the change if that ever switches.
BuildRequires:  libicu-devel >= 5.4
%global bundleicu 0
%else
%global bundleicu 1
%endif

%if 0%{?rhel} == 7
%global bundlere2 1
%else
%global bundlere2 0
%endif

# The libxml_utils code depends on the specific bundled libxml checkout
# which is not compatible with the current code in the Fedora package as of
# 2017-06-08.
%global bundlelibxml 1

# Fedora's Python 2 stack is being removed, we use the bundled Python libraries
# This can be revisited once we upgrade to Python 3
%global bundlepylibs 1

# RHEL 7.9 dropped minizip.
# It exists everywhere else though.
%global bundleminizip 0
%if 0%{?rhel} == 7
%global bundleminizip 1
%endif

# Chromium used to break on wayland, hidpi, and colors with gtk3 enabled.
# Hopefully it does not anymore.
%global gtk3 1

%if 0%{?rhel} == 7 || 0%{?rhel} == 8
%global dts_version 9

%global bundleopus 1
%global bundlelibusbx 1
%global bundleharfbuzz 1
%global bundlelibwebp 1
%global bundlelibpng 1
%global bundlelibjpeg 1
%global bundlefreetype 1
%global bundlelibdrm 1
%global bundlefontconfig 1
%else
%global bundleharfbuzz 0
%global bundleopus 1
%global bundlelibusbx 0
%global bundlelibwebp 0
%global bundlelibpng 0
%global bundlelibjpeg 0
%global bundlefreetype 0
%global bundlelibdrm 0
%global bundlefontconfig 0
%endif

# Needs at least harfbuzz 2.4.0 now.
# 2019-09-13
%if 0%{?fedora} < 31
%global bundleharfbuzz 1
%else
%global bundleharfbuzz 0
%endif

### Google API keys (see http://www.chromium.org/developers/how-tos/api-keys)
### Note: These are for Fedora use ONLY.
### For your own distribution, please get your own set of keys.
### http://lists.debian.org/debian-legal/2013/11/msg00006.html
%global api_key %{nil}
%global default_client_id %{nil}
%global default_client_secret %{nil}

#Build with debugging symbols
%global debug_pkg 0

%global majorversion 89
%global revision 1

%if %{freeworld}
Name:		ungoogled-chromium%{nsuffix}
%else
Name:		ungoogled-chromium
%endif
Version:	%{majorversion}.0.4389.114
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
Patch1:		chromium-89.0.4389.72-initial_prefs-etc-path.patch
# Use gn system files
Patch2:		chromium-67.0.3396.62-gn-system.patch
# Do not prefix libpng functions
Patch3:		chromium-60.0.3112.78-no-libpng-prefix.patch
# Do not mangle libjpeg
Patch4:		chromium-60.0.3112.78-jpeg-nomangle.patch
# Do not mangle zlib
Patch5:		chromium-77.0.3865.75-no-zlib-mangle.patch
# Do not use unrar code, it is non-free
Patch6:		chromium-89.0.4389.72-norar.patch
# Use Gentoo's Widevine hack
# https://gitweb.gentoo.org/repo/gentoo.git/tree/www-client/chromium/files/chromium-widevine-r3.patch
Patch7:		chromium-71.0.3578.98-widevine-r3.patch
# Disable fontconfig cache magic that breaks remoting
Patch8:		chromium-83.0.4103.61-disable-fontconfig-cache-magic.patch
# drop rsp clobber, which breaks gcc9 (thanks to Jeff Law)
Patch9:	chromium-78.0.3904.70-gcc9-drop-rsp-clobber.patch
# Try to load widevine from other places
Patch10:	chromium-89.0.4389.72-widevine-other-locations.patch
# Try to fix version.py for Rawhide
Patch11:	chromium-71.0.3578.98-py2-bootstrap.patch

# Needs to be submitted..
Patch51:	chromium-76.0.3809.100-gcc-remoting-constexpr.patch
# https://gitweb.gentoo.org/repo/gentoo.git/tree/www-client/chromium/files/chromium-unbundle-zlib.patch
Patch52:	chromium-81.0.4044.92-unbundle-zlib.patch
# Needs to be submitted..
Patch53:	chromium-77.0.3865.75-gcc-include-memory.patch
# https://github.com/stha09/chromium-patches/blob/master/chromium-78-protobuf-RepeatedPtrField-export.patch
Patch55:	chromium-78-protobuf-RepeatedPtrField-export.patch
# ../../third_party/perfetto/include/perfetto/base/task_runner.h:48:55: error: 'uint32_t' has not been declared
Patch56:	chromium-80.0.3987.87-missing-cstdint-header.patch
# Missing <cstring> (thanks c++17)
Patch57:	chromium-89.0.4389.72-missing-cstring-header.patch
# prepare for using system ffmpeg (clean)
# http://svnweb.mageia.org/packages/cauldron/chromium-browser-stable/current/SOURCES/chromium-53-ffmpeg-no-deprecation-errors.patch?view=markup
Patch58:	chromium-53-ffmpeg-no-deprecation-errors.patch
# https://github.com/stha09/chromium-patches/blob/chromium-89-patchset-7/chromium-89-dawn-include.patch
Patch60:	chromium-89-dawn-include.patch
# https://github.com/stha09/chromium-patches/blob/chromium-89-patchset-7/chromium-89-quiche-dcheck.patch
Patch61:	chromium-89-quiche-dcheck.patch
# https://github.com/stha09/chromium-patches/blob/chromium-89-patchset-7/chromium-89-quiche-private.patch
Patch62:	chromium-89-quiche-private.patch
# https://github.com/stha09/chromium-patches/blob/chromium-89-patchset-7/chromium-89-skia-CropRect.patch
Patch63:	chromium-89-skia-CropRect.patch
# https://github.com/stha09/chromium-patches/blob/chromium-89-patchset-7/chromium-89-AXTreeSerializer-include.patch
Patch64:	chromium-89-AXTreeSerializer-include.patch


# Silence GCC warnings during gn compile
Patch65:	chromium-84.0.4147.105-gn-gcc-cleanup.patch
# Fix missing cstring in remoting code
Patch66:	chromium-84.0.4147.125-remoting-cstring.patch
# Apply fix_textrels hack for i686 (even without lld)
Patch67:	chromium-84.0.4147.125-i686-fix_textrels.patch
# Work around binutils bug in aarch64 (F33+)
Patch68:	chromium-84.0.4147.125-aarch64-clearkeycdm-binutils-workaround.patch
# Fix sandbox code to properly handle the new way that glibc handles fstat in Fedora 34+
# Thanks to Kevin Kofler for the fix.
Patch75:	chromium-88.0.4324.96-fstatfix.patch
# Rawhide (f35) glibc defines SIGSTKSZ as a long instead of a constant
Patch76:	chromium-88.0.4324.182-rawhide-gcc-std-max-fix.patch
# Fix symbol visibility with gcc on swiftshader's libEGL
Patch77:	chromium-88.0.4324.182-gcc-fix-swiftshader-libEGL-visibility.patch
# Include support for futex_time64 (64bit time on 32bit platforms)
# https://chromium.googlesource.com/chromium/src/+/955a586c63c4f99fb734e44221db63f5b2ca25a9%5E%21/#F0
Patch78:       chromium-89.0.4389.82-support-futex_time64.patch
# Do not download proprietary widevine module in the background (thanks Debian)
Patch79:       chromium-89.0.4389.82-widevine-no-download.patch
# Fix crashes with components/cast_*
# Thanks to Gentoo
# https://gitweb.gentoo.org/repo/gentoo.git/plain/www-client/chromium/files/chromium-89-EnumTable-crash.patch
Patch80:       chromium-89-EnumTable-crash.patch
# Fix build issues with newer libva
# https://github.com/chromium/chromium/commit/7ae60470cdb0bea4548a0f5e8271b359f9450c79.patch
Patch81:       7ae60470cdb0bea4548a0f5e8271b359f9450c79.patch

# Use lstdc++ on EPEL7 only
Patch101:	chromium-75.0.3770.100-epel7-stdc++.patch
# el7 only patch
Patch102:	chromium-80.0.3987.132-el7-noexcept.patch
# No linux/kcmp.h on EPEL7
Patch103:	chromium-86.0.4240.75-epel7-no-kcmp-h.patch
# Use old cups (chromium's code workaround breaks on gcc)
# Revert: https://github.com/chromium/chromium/commit/c3213f8779ddc427e89d982514185ed5e4c94e91
Patch104:	chromium-84.0.4147.89-epel7-old-cups.patch
# Still not wrong, but it seems like only EL needs it
Patch106:	chromium-77-clang.patch
# ARM failures on el8 related to int clashes
# error: incompatible types when initializing type 'int64_t' {aka 'long int'} using type 'int64x1_t'
# note: expected 'int8x16_t' but argument is of type 'uint8x16_t'
# Patch107:	chromium-84.0.4147.89-el8-arm-incompatible-ints.patch
# libdrm on EL7 is rather old and chromium assumes newer
# This gets us by for now
Patch108:	chromium-85.0.4183.83-el7-old-libdrm.patch
# EL-7 does not have sys/random.h
Patch109:	chromium-87.0.4280.66-el7-no-sys-random.patch

# VAAPI
# Upstream turned VAAPI on in Linux in 86
Patch202:	chromium-89.0.4389.72-enable-hardware-accelerated-mjpeg.patch
Patch203:	chromium-86.0.4240.75-vaapi-i686-fpermissive.patch
Patch205:	chromium-86.0.4240.75-fix-vaapi-on-intel.patch

# Apply these patches to work around EPEL8 issues
Patch300:	chromium-89.0.4389.82-rhel8-force-disable-use_gnome_keyring.patch

# And fixes for new compilers
Patch400:       chromium-gcc11.patch

# RPM Fusion patches [free/chromium-freeworld]:
Patch503:       chromium-manpage.patch

# RPM Fusion patches [free/chromium-browser-privacy]:
Patch600:       chromium-default-user-data-dir.patch

# Additional patches:
Patch700:       chromium-missing-std-vector.patch

# Use chromium-latest.py to generate clean tarball from released build tarballs, found here:
# http://build.chromium.org/buildbot/official/
# For Chromium Fedora use chromium-latest.py --stable --ffmpegclean --ffmpegarm
# If you want to include the ffmpeg arm sources append the --ffmpegarm switch
# https://commondatastorage.googleapis.com/chromium-browser-official/chromium-%%{version}.tar.xz
%if %{freeworld}
Source0:	https://commondatastorage.googleapis.com/chromium-browser-official/chromium-%{version}.tar.xz
%else
Source0:	chromium-%{version}-clean.tar.xz
%endif
# https://chromium.googlesource.com/chromium/tools/depot_tools.git/+archive/7e7a454f9afdddacf63e10be48f0eab603be654e.tar.gz
Source2:	depot_tools.git-master.tar.gz
Source3:	%{name}.sh
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
# RHEL 7 needs newer nodejs
%if 0%{?rhel} == 7
Source19:	https://nodejs.org/dist/v10.15.3/node-v10.15.3-linux-x64.tar.gz
%endif
# Bring xcb-proto with us (might need more than python on EPEL?)
Source20:	https://www.x.org/releases/individual/proto/xcb-proto-1.14.tar.xz

# Add our own appdata file.
Source21:       %{name}.appdata.xml

# ungoogled-chromium source
%global ungoogled_chromium_revision 89.0.4389.114-1
Source300:      https://github.com/Eloston/ungoogled-chromium/archive/%{ungoogled_chromium_revision}/ungoogled-chromium-%{ungoogled_chromium_revision}.tar.gz

# We can assume gcc and binutils.
BuildRequires:	gcc-c++

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
# Old Fedora (before 30) uses the 1.2 minizip by default.
# Newer Fedora needs to use the compat package
%if 0%{?fedora} >= 30
BuildRequires:	minizip-compat-devel
%else
# RHEL 8 needs to use the compat-minizip (provided by minizip1.2)
%if 0%{?rhel} >= 8
BuildRequires:	minizip-compat-devel
%else
# RHEL 7 used to have minizip, but as of 7.9, it does not.
# BuildRequires:	minizip-devel
%endif
%endif
# RHEL 7's nodejs is too old
%if 0%{?rhel} == 7
# Use bundled.
%else
BuildRequires:	nodejs
%endif
BuildRequires:	nss-devel >= 3.26
BuildRequires:	pciutils-devel
BuildRequires:	pulseaudio-libs-devel

# For screen sharing on Wayland, currently Fedora only thing - no epel
%if 0%{?fedora}
BuildRequires:	pkgconfig(libpipewire-0.2)
%endif

# for /usr/bin/appstream-util
BuildRequires: libappstream-glib

# gn needs these
BuildRequires:  libstdc++-static
BuildRequires:	libstdc++-devel, openssl-devel
# Fedora tries to use system libs whenever it can.
BuildRequires:	bzip2-devel
BuildRequires:	dbus-glib-devel
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
Requires:	libusbx >= 1.0.21-0.1.git448584a
BuildRequires:	libusbx-devel >= 1.0.21-0.1.git448584a
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
BuildRequires:  libxshmfence-devel
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
BuildRequires:  python3
%if 0%{?fedora} >= 32
BuildRequires:	python2.7
%else
BuildRequires:	python2
BuildRequires:	python2-devel
%endif
%if 0%{?bundlepylibs}
# Using bundled bits, do nothing.
%else
%if 0%{?fedora}
BuildRequires:	python2-beautifulsoup4
BuildRequires:	python2-beautifulsoup
BuildRequires:	python2-html5lib
BuildRequires:	python2-markupsafe
BuildRequires:	python2-ply
%else
BuildRequires:	python-beautifulsoup4
BuildRequires:	python-BeautifulSoup
BuildRequires:	python-html5lib
BuildRequires:	python-markupsafe
BuildRequires:	python-ply
%endif
BuildRequires:	python2-simplejson
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
%if 0%{?rhel} >= 7
Source100:	https://github.com/googlefonts/Arimo/raw/master/fonts/ttf/Arimo-Bold.ttf
Source101:	https://github.com/googlefonts/Arimo/raw/master/fonts/ttf/Arimo-BoldItalic.ttf
Source102:	https://github.com/googlefonts/Arimo/raw/master/fonts/ttf/Arimo-Italic.ttf
Source103:	https://github.com/googlefonts/Arimo/raw/master/fonts/ttf/Arimo-Regular.ttf
Source104:	https://github.com/google/fonts/raw/master/apache/cousine/Cousine-Bold.ttf
Source105:	https://github.com/google/fonts/raw/master/apache/cousine/Cousine-BoldItalic.ttf
Source106:	https://github.com/google/fonts/raw/master/apache/cousine/Cousine-Italic.ttf
Source107:	https://github.com/google/fonts/raw/master/apache/cousine/Cousine-Regular.ttf
Source108:	https://github.com/google/fonts/raw/master/apache/tinos/Tinos-Bold.ttf
Source109:	https://github.com/google/fonts/raw/master/apache/tinos/Tinos-BoldItalic.ttf
Source110:	https://github.com/google/fonts/raw/master/apache/tinos/Tinos-Italic.ttf
Source111:	https://github.com/google/fonts/raw/master/apache/tinos/Tinos-Regular.ttf
%else
BuildRequires:	google-croscore-arimo-fonts
BuildRequires:	google-croscore-cousine-fonts
BuildRequires:	google-croscore-tinos-fonts
%endif
%if 0%{?rhel} == 7
Source112:	https://releases.pagure.org/lohit/lohit-gurmukhi-ttf-2.91.2.tar.gz
Source113:	https://noto-website-2.storage.googleapis.com/pkgs/NotoSansCJKjp-hinted.zip
%else
BuildRequires:  google-noto-sans-cjk-jp-fonts
BuildRequires:  lohit-gurmukhi-fonts
%endif
BuildRequires:	dejavu-sans-fonts
BuildRequires:	thai-scalable-garuda-fonts
BuildRequires:	lohit-devanagari-fonts
BuildRequires:	lohit-tamil-fonts
BuildRequires:	google-noto-sans-khmer-fonts
BuildRequires:	google-noto-emoji-color-fonts
%if 0%{?fedora} >= 30
BuildRequires:	google-noto-sans-symbols2-fonts
BuildRequires:	google-noto-sans-tibetan-fonts
%else
Source114:	https://github.com/googlefonts/noto-fonts/raw/master/unhinted/ttf/NotoSansSymbols2/NotoSansSymbols2-Regular.ttf
Source115:	NotoSansTibetan-Regular.ttf
%endif
%endif
# using the built from source version on aarch64
BuildRequires:	ninja-build
# Yes, java is needed as well..
BuildRequires:	java-1.8.0-openjdk-headless
BuildRequires:	lua

%if 0%{?rhel} == 7
BuildRequires: devtoolset-%{dts_version}-toolchain, devtoolset-%{dts_version}-libatomic-devel
%endif

# We need to workaround a gcc 8 bug
# https://gcc.gnu.org/bugzilla/show_bug.cgi?id=94929
# https://bugs.gentoo.org/726604
%if 0%{?rhel} == 8
BuildRequires: gcc-toolset-%{dts_version}-toolchain, gcc-toolset-%{dts_version}-libatomic-devel
%endif

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

%if 0%{?rhel} == 7
ExclusiveArch:  x86_64 i686
%else
ExclusiveArch:	x86_64 i686 aarch64
%endif

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
%if 0%{?fedora} >= 30
Requires: minizip-compat%{_isa}
%else
%if %{?rhel} == 7
# Do nothing
%else
Requires: minizip%{_isa}
%endif
%endif

############################################PREP###########################################################
%prep
%setup -q -T -n ungoogled-chromium-%{ungoogled_chromium_revision} -b 300
%setup -q -T -c -n depot_tools -a 2
%setup -q -n chromium-%{version}

%global ungoogled_chromium_root %{_builddir}/ungoogled-chromium-%{ungoogled_chromium_revision}

### Chromium Fedora Patches ###
%patch1 -p1 -b .etc
%patch2 -p1 -b .gnsystem
%patch3 -p1 -b .nolibpngprefix
# Upstream accidentally made the same change in 89, but they've already reverted it for 90+ so this patch will return
# %%patch4 -p1 -b .nolibjpegmangle
%patch5 -p1 -b .nozlibmangle
# Conflict with unrar.patch in ungoogled-chromium
# %%patch6 -p1 -b .nounrar
%patch7 -p1 -b .widevine-hack
%patch8 -p1 -b .nofontconfigcache
%patch9 -p1 -b .gcc9
%patch10 -p1 -b .widevine-other-locations
%patch11 -p1 -b .py2

# Short term fixes (usually gcc and backports)
%patch51 -p1 -b .gcc-remoting-constexpr
%if 0%{?fedora} || 0%{?rhel} >= 8
%patch52 -p1 -b .unbundle-zlib
%endif
%patch53 -p1 -b .gcc-include-memory
%patch55 -p1 -b .protobuf-export
%patch56 -p1 -b .missing-cstdint
%patch57 -p1 -b .missing-cstring
%patch58 -p1 -b .ffmpeg-deprecations
%patch60 -p1 -b .dawn-include
%patch61 -p1 -b .quiche-dcheck
%patch62 -p1 -b .quiche-private
%patch63 -p1 -b .skia-CropRect
%patch64 -p1 -b .AXTreeSerializer-include
%patch65 -p1 -b .gn-gcc-cleanup
%patch66 -p1 -b .remoting-cstring
%patch67 -p1 -b .i686-textrels
# %%patch68 -p1 -b .aarch64-clearkeycdm-binutils-workaround
%patch75 -p1 -b .fstatfix
%if 0%{?fedora} >= 35
%patch76 -p1 -b .sigstkszfix
%endif
%patch77 -p1 -b .gcc-swiftshader-visibility
%patch78 -p1 -b .futex-time64
%patch79 -p1 -b .widevine-no-download
%patch80 -p1 -b .EnumTable-crash
%patch81 -p1 -b .libva-forward-compat


# EPEL specific patches
%if 0%{?rhel} == 7
# %%patch101 -p1 -b .epel7
# %%patch102 -p1 -b .el7-noexcept
%patch103 -p1 -b .epel7-kcmp
%patch104 -p1 -b .el7cups
%patch108 -p1 -b .el7-old-libdrm
%patch109 -p1 -b .el7-no-sys-random
%endif

%if 0%{?rhel} == 8
# %%patch107 -p1 -b .el8-arm-incompatible-ints
%endif

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

%patch400 -p1 -b .gcc11

# RPM Fusion patches [free/chromium-freeworld]:
%patch503 -p1 -b .manpage

# RPM Fusion patches [free/chromium-browser-privacy]:
%patch600 -p1 -b .default-user-dir

# Additional patches:
%patch700 -p1 -b .missing-std-vector

# Change shebang in all relevant files in this directory and all subdirectories
# See `man find` for how the `-exec command {} +` syntax works
find -type f -exec sed -iE '1s=^#! */usr/bin/\(python\|env python\)[23]\?=#!%{__python2}=' {} +

export CC="gcc"
export CXX="g++"
export AR="ar"
export RANLIB="ranlib"

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
%if 0%{?rhel} >= 7
cp %{SOURCE100} .
cp %{SOURCE101} .
cp %{SOURCE102} .
cp %{SOURCE103} .
cp %{SOURCE104} .
cp %{SOURCE105} .
cp %{SOURCE106} .
cp %{SOURCE107} .
cp %{SOURCE108} .
cp %{SOURCE109} .
cp %{SOURCE110} .
cp %{SOURCE111} .
%else
%if 0%{?fedora} >= 33
cp -a /usr/share/fonts/google-arimo-fonts/Arimo-*.ttf .
cp -a /usr/share/fonts/google-cousine-fonts/Cousine-*.ttf .
cp -a /usr/share/fonts/google-tinos-fonts/Tinos-*.ttf .
%else
cp -a /usr/share/fonts/google-croscore/Arimo-*.ttf .
cp -a /usr/share/fonts/google-croscore/Cousine-*.ttf .
cp -a /usr/share/fonts/google-croscore/Tinos-*.ttf .
%endif
%endif
%if 0%{?rhel} == 7
tar xf %{SOURCE112}
mv lohit-gurmukhi-ttf-2.91.2/Lohit-Gurmukhi.ttf .
rm -rf lohit-gurmukhi-ttf-2.91.2
unzip %{SOURCE113}
%else
cp -a /usr/share/fonts/lohit-gurmukhi/Lohit-Gurmukhi.ttf .
cp -a /usr/share/fonts/google-noto-cjk/NotoSansCJKjp-Regular.otf .
%endif
%if 0%{?fedora} >= 32
cp -a /usr/share/fonts/dejavu-sans-fonts/DejaVuSans.ttf /usr/share/fonts/dejavu-sans-fonts/DejaVuSans-Bold.ttf .
%else
cp -a /usr/share/fonts/dejavu/DejaVuSans.ttf /usr/share/fonts/dejavu/DejaVuSans-Bold.ttf .
%endif
%if 0%{?fedora} >= 33
cp -a /usr/share/fonts/thai-scalable/Garuda.otf .
sed -i 's|Garuda.ttf|Garuda.otf|g' ../BUILD.gn
%else
cp -a /usr/share/fonts/thai-scalable/Garuda.ttf .
%endif
cp -a /usr/share/fonts/lohit-devanagari/Lohit-Devanagari.ttf /usr/share/fonts/lohit-tamil/Lohit-Tamil.ttf .
cp -a /usr/share/fonts/google-noto/NotoSansKhmer-Regular.ttf .
cp -a /usr/share/fonts/google-noto-emoji/NotoColorEmoji.ttf .
%if 0%{?fedora} >= 30
cp -a /usr/share/fonts/google-noto/NotoSansSymbols2-Regular.ttf /usr/share/fonts/google-noto/NotoSansTibetan-Regular.ttf .
%else
cp -a %{SOURCE114} %{SOURCE115} .
%endif
popd
%endif

# Core defines are flags that are true for both the browser and headless.
UNGOOGLED_CHROMIUM_GN_DEFINES=""
UNGOOGLED_CHROMIUM_GN_DEFINES+=' is_debug=false is_official_build=false'
%ifarch x86_64 aarch64
UNGOOGLED_CHROMIUM_GN_DEFINES+=' system_libdir="lib64"'
%endif
UNGOOGLED_CHROMIUM_GN_DEFINES+=' google_api_key="%{api_key}" google_default_client_id="%{default_client_id}" google_default_client_secret="%{default_client_secret}"'
UNGOOGLED_CHROMIUM_GN_DEFINES+=' is_clang=false use_sysroot=false fieldtrial_testing_like_official_build=true use_lld=false rtc_enable_symbol_export=true'
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
UNGOOGLED_CHROMIUM_GN_DEFINES+=' use_gnome_keyring=false use_glib=true'
UNGOOGLED_CHROMIUM_GN_DEFINES+=' use_gio=true use_pulseaudio=true icu_use_data_file = true'
UNGOOGLED_CHROMIUM_GN_DEFINES+=' enable_nacl=false'
UNGOOGLED_CHROMIUM_GN_DEFINES+=' is_component_ffmpeg=false is_component_build=false'
UNGOOGLED_CHROMIUM_GN_DEFINES+=' enable_hangout_services_extension=false'
%if %{debug_pkg}
UNGOOGLED_CHROMIUM_GN_DEFINES+=' blink_symbol_level=1 symbol_level=1'
%else
UNGOOGLED_CHROMIUM_GN_DEFINES+=' blink_symbol_level=0 symbol_level=0'
%endif
UNGOOGLED_CHROMIUM_GN_DEFINES+=' enable_widevine=true'
%if %{use_vaapi}
%if 0%{?fedora} >= 28
UNGOOGLED_CHROMIUM_GN_DEFINES+=' use_vaapi=true'
%endif
%else
UNGOOGLED_CHROMIUM_GN_DEFINES+=' use_vaapi=false'
%endif
%if 0%{?fedora}
UNGOOGLED_CHROMIUM_GN_DEFINES+=' rtc_use_pipewire=true rtc_link_pipewire=true'
%endif
UNGOOGLED_CHROMIUM_GN_DEFINES+=' chrome_pgo_phase=0 enable_js_type_check=false enable_mse_mpeg2ts_stream_parser=true enable_nacl_nonsfi=false enable_one_click_signin=false enable_reading_list=false enable_remoting=false enable_reporting=false enable_service_discovery=false exclude_unwind_tables=true safe_browsing_mode=0'
export UNGOOGLED_CHROMIUM_GN_DEFINES

# ungoogled-chromium: binary pruning.
python3 -B %{ungoogled_chromium_root}/utils/prune_binaries.py . %{ungoogled_chromium_root}/pruning.list || true

%if 0%{?rhel} == 7
pushd third_party/node/linux
tar xf %{SOURCE19}
mv node-v10.15.3-linux-x64 node-linux-x64
popd
%else
mkdir -p third_party/node/linux/node-linux-x64/bin
ln -s %{_bindir}/node third_party/node/linux/node-linux-x64/bin/node
%endif

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
	'third_party/angle/src/third_party/compiler' \
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
	'third_party/depot_tools' \
	'third_party/devscripts' \
	'third_party/devtools-frontend' \
	'third_party/devtools-frontend/src/third_party/typescript' \
	'third_party/devtools-frontend/src/front_end/third_party/acorn' \
	'third_party/devtools-frontend/src/front_end/third_party/axe-core' \
	'third_party/devtools-frontend/src/front_end/third_party/chromium' \
	'third_party/devtools-frontend/src/front_end/third_party/codemirror' \
	'third_party/devtools-frontend/src/front_end/third_party/fabricjs' \
	'third_party/devtools-frontend/src/front_end/third_party/i18n' \
	'third_party/devtools-frontend/src/front_end/third_party/intl-messageformat' \
	'third_party/devtools-frontend/src/front_end/third_party/lighthouse' \
	'third_party/devtools-frontend/src/front_end/third_party/lit-html' \
	'third_party/devtools-frontend/src/front_end/third_party/lodash-isequal' \
	'third_party/devtools-frontend/src/front_end/third_party/marked' \
	'third_party/devtools-frontend/src/front_end/third_party/puppeteer' \
	'third_party/devtools-frontend/src/front_end/third_party/wasmparser' \
	'third_party/dom_distiller_js' \
	'third_party/emoji-segmenter' \
	'third_party/expat' \
	'third_party/ffmpeg' \
	'third_party/flac' \
    'third_party/flatbuffers' \
	'third_party/fontconfig' \
	'third_party/freetype' \
	'third_party/fusejs' \
	'third_party/google_input_tools' \
	'third_party/google_input_tools/third_party/closure_library' \
	'third_party/google_input_tools/third_party/closure_library/third_party/closure' \
	'third_party/google_trust_services' \
	'third_party/googletest' \
	'third_party/grpc' \
	'third_party/harfbuzz-ng' \
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
	'third_party/libaom/source/libaom/third_party/vector' \
	'third_party/libaom/source/libaom/third_party/x86inc' \
	'third_party/libavif' \
	'third_party/libdrm' \
	'third_party/libgifcodec' \
	'third_party/libjingle' \
	'third_party/libjpeg_turbo' \
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
	'third_party/lottie' \
	'third_party/lss' \
	'third_party/lzma_sdk' \
	'third_party/mako' \
%if 0%{?bundlepylibs}
	'third_party/markupsafe' \
%endif
	'third_party/mesa' \
	'third_party/metrics_proto' \
	'third_party/minigbm' \
	'third_party/modp_b64' \
	'third_party/nasm' \
	'third_party/nearby' \
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
	'third_party/perfetto/protos/third_party/pprof' \
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
	'third_party/s2cellid' \
	'third_party/schema_org' \
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
	'third_party/test_fonts' \
	'third_party/ukey2' \
    'third_party/usb_ids' \
	'third_party/usrsctp' \
	'third_party/vulkan' \
	'third_party/wayland' \
	'third_party/web-animations-js' \
	'third_party/webdriver' \
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
	'tools/grit/third_party/six' \
	'url/third_party/mozilla' \
	'v8/src/third_party/siphash' \
	'v8/src/third_party/utf8-decoder' \
	'v8/src/third_party/valgrind' \
	'v8/third_party/v8' \
	'v8/third_party/inspector_protocol' \
	--do-remove

%if ! 0%{?bundlepylibs}
# Look, I don't know. This package is spit and chewing gum. Sorry.
rm -rf third_party/markupsafe
ln -s %{python2_sitearch}/markupsafe third_party/markupsafe
# We should look on removing other python2 packages as well i.e. ply
%endif

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

%if 0%{?rhel} == 7
. /opt/rh/devtoolset-%{dts_version}/enable
%endif

%if 0%{?rhel} == 8
. /opt/rh/gcc-toolset-%{dts_version}/enable
%endif

# Check that there is no system 'google' module, shadowing bundled ones:
if python2 -c 'import google ; print google.__path__' 2> /dev/null ; then \
    echo "Python 2 'google' module is defined, this will shadow modules of this build"; \
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
%{builddir}/gn --script-executable=%{__python2} gen --args="$UNGOOGLED_CHROMIUM_GN_DEFINES" %{builddir}

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

%if 0%{?rhel} == 7
. /opt/rh/devtoolset-%{dts_version}/enable
%endif

%if 0%{?rhel} == 8
. /opt/rh/gcc-toolset-%{dts_version}/enable
%endif

export PYTHONPATH="../../third_party/pyjson5/src:../../third_party/catapult/third_party/google-endpoints:../../xcb-proto-1.14"

echo
# Now do the full browser
%if 0%{freeworld}
%build_target %{builddir} media
%else
%build_target %{builddir} chrome
%build_target %{builddir} chrome_sandbox
%build_target %{builddir} chromedriver
%if %{build_clear_key_cdm}
%build_target %{builddir} clear_key_cdm
%endif
%build_target %{builddir} policy_templates
%endif

%install
rm -rf %{buildroot}

%if 0%{freeworld}
	mkdir -p %{buildroot}%{chromium_path}

	pushd %{builddir}
		cp -a libffmpeg.so* %{buildroot}%{chromium_path}
		cp -a libmedia.so* %{buildroot}%{chromium_path}
		mv %{buildroot}%{chromium_path}/libffmpeg.so{,.%{lsuffix}}
		mv %{buildroot}%{chromium_path}/libffmpeg.so.TOC{,.%{lsuffix}}
		mv %{buildroot}%{chromium_path}/libmedia.so{,.%{lsuffix}}
		mv %{buildroot}%{chromium_path}/libmedia.so.TOC{,.%{lsuffix}}
	popd
%else
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

	install -D -m0644 %{SOURCE21} ${RPM_BUILD_ROOT}%{_datadir}/metainfo/%{chromium_browser_channel}.appdata.xml
	appstream-util validate-relax --nonet ${RPM_BUILD_ROOT}%{_datadir}/metainfo/%{chromium_browser_channel}.appdata.xml

	mkdir -p %{buildroot}%{_datadir}/gnome-control-center/default-apps/
	cp -a %{SOURCE9} %{buildroot}%{_datadir}/gnome-control-center/default-apps/

# freeworld conditional
%endif

%post
# Set SELinux labels - semanage itself will adjust the lib directory naming
# But only do it when selinux is enabled, otherwise, it gets noisy.
if selinuxenabled; then
	semanage fcontext -a -t bin_t /usr/lib/%{chromium_browser_channel} &>/dev/null || :
	semanage fcontext -a -t bin_t /usr/lib/%{chromium_browser_channel}/%{chromium_browser_channel}.sh &>/dev/null || :
	semanage fcontext -a -t chrome_sandbox_exec_t /usr/lib/chrome-sandbox &>/dev/null || :
	restorecon -R -v %{chromium_path}/%{chromium_browser_channel} &>/dev/null || :
fi

%if 0%{freeworld}
# We only build libs-media-freeworld.
%else

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

%{_bindir}/chromedriver
%{chromium_path}/chromedriver

%endif

%changelog
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
