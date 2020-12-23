# ungoogled-chromium-fedora

Fedora packaging for [ungoogled-chromium](//github.com/Eloston/ungoogled-chromium).

## Downloads

Pre-built binary rpm files can be found on OBS:

* OBS (Fedora 33)
  ```sh
  # dnf config-manager --add-repo https://download.opensuse.org/repositories/home:wchen342:ungoogled-chromium-fedora/Fedora_33/home:wchen342:ungoogled-chromium-fedora.repo
  # dnf install ungoogled-chromium
  ```
* OBS (Fedora 32)
  ```sh
  # dnf config-manager --add-repo https://download.opensuse.org/repositories/home:wchen342:ungoogled-chromium-fedora/Fedora_32/home:wchen342:ungoogled-chromium-fedora.repo
  # dnf install ungoogled-chromium
  ```

## Building

1. Clone this repository

2. Create a build folder following [https://rpm-packaging-guide.github.io/#rpm-packaging-workspace](https://rpm-packaging-guide.github.io/#rpm-packaging-workspace)

3. Copy `ungoogled-chromium.spec` into `SPECS`

4. Copy all other files into `SOURCES`

5. Prepare the following files and copy them into `SOURCES`:
    * chromium source tarball
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
