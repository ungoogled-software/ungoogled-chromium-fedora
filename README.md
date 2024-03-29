# ungoogled-chromium-fedora

Fedora packaging for [ungoogled-chromium](//github.com/Eloston/ungoogled-chromium).

*CentOS 7 has reached EOL and CentOS 8 will reach EOL at the end of 2021, thus CentOS builds will no longer be provided. aarch64 builds are provided on a best-effort basis.*

**!!!WARNING: For legal reasons, the binaries we provide on OBS do not contain proprietary codecs. This includes MPEG families, H264 and other common codecs. If you wish to use those codecs, either compile yourself or use the Flatpak package instead!!!**

## Downloads

Pre-built binary rpm files can be found on OBS:
  * Direct Download
    - [OBS Production Project](https://build.opensuse.org/project/show/home:ungoogled_chromium)
    - [OBS Development Project](https://build.opensuse.org/project/show/home:ungoogled_chromium:testing)

  * RPM repository
    - OBS (Fedora 35)
      ```sh
      # dnf config-manager --add-repo https://download.opensuse.org/repositories/home:/ungoogled_chromium/Fedora_35/home:ungoogled_chromium.repo
      # dnf install ungoogled-chromium
      ```
    - OBS (Fedora 34)
      ```sh
      # dnf config-manager --add-repo https://download.opensuse.org/repositories/home:/ungoogled_chromium/Fedora_34/home:ungoogled_chromium.repo
      # dnf install ungoogled-chromium
      ```

## Building
The following steps are for Fedora. For CentOS, extra files are needed. See `sources`.

1. Clone this repository

2. Create a build folder following [https://rpm-packaging-guide.github.io/#rpm-packaging-workspace](https://rpm-packaging-guide.github.io/#rpm-packaging-workspace)

3. Copy `ungoogled-chromium.spec` into `SPECS`

4. Copy all other files into `SOURCES`

5. Prepare the following files and copy them into `SOURCES`:
    * chromium source tarball:
      * If you set `%global freeworld` to 1, get the tarball from `https://commondatastorage.googleapis.com/chromium-browser-official/chromium-%{version}.tar.xz`
      * If `%global freeworld` is 0 (the default), generate the tarball by running `./chromium-latest.py --version %{version} --ffmpegclean --ffmpegarm`
      * *Note: DO NOT use the source from Github chromium mirror! The tarball you get will lack files you need to successfully build chromium!*
    * `ungoogled-chromium` src from the corresponding tag ([https://github.com/Eloston/ungoogled-chromium/archive/%{ungoogled_chromium_revision}/ungoogled-chromium-%{ungoogled_chromium_revision}.tar.gz](https://github.com/Eloston/ungoogled-chromium/archive/%{ungoogled_chromium_revision}/ungoogled-chromium-%{ungoogled_chromium_revision}.tar.gz))
    * `depot_tools` src tarball ([https://chromium.googlesource.com/chromium/tools/depot_tools.git](https://chromium.googlesource.com/chromium/tools/depot_tools.git))
    * Fonts:
      - [https://github.com/web-platform-tests/wpt/raw/master/fonts/Ahem.ttf](https://github.com/web-platform-tests/wpt/raw/master/fonts/Ahem.ttf)
      - [https://fontlibrary.org/assets/downloads/gelasio/4d610887ff4d445cbc639aae7828d139/gelasio.zip](https://fontlibrary.org/assets/downloads/gelasio/4d610887ff4d445cbc639aae7828d139/gelasio.zip)
      - [https://download.savannah.nongnu.org/releases/freebangfont/MuktiNarrow-0.94.tar.bz2](https://download.savannah.nongnu.org/releases/freebangfont/MuktiNarrow-0.94.tar.bz2)
    * [https://www.x.org/releases/individual/proto/xcb-proto-1.14.tar.xz](https://www.x.org/releases/individual/proto/xcb-proto-1.14.tar.xz)  

6. Build
    * For binary package (.rpm)
      ```
      rpmbuild -bb SPECS/ungoogled-chromium.spec
      ```

      The RPM file will appear in `RPMS` after a successful build.
    * For source package (.srpm)
      ```
      rpmbuild -bs SPECS/ungoogled-chromium.spec
      ```
      
      The SRPM file will appear in `SRPMS` after a successful build.
    
## License

See [LICENSE](LICENSE)
