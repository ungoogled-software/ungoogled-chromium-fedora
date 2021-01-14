# ungoogled-chromium-fedora

Fedora/RHEL/CentOS packaging for [ungoogled-chromium](//github.com/Eloston/ungoogled-chromium).

## Downloads

Pre-built binary rpm files can be found on OBS:
  * Direct Download
    - [OBS download page](https://software.opensuse.org//download.html?project=home%3Awchen342%3Aungoogled-chromium-fedora&package=ungoogled-chromium)

  * RPM repository
    - OBS (Fedora 33)
      ```sh
      # dnf config-manager --add-repo https://download.opensuse.org/repositories/home:wchen342:ungoogled-chromium-fedora/Fedora_33/home:wchen342:ungoogled-chromium-fedora.repo
      # dnf install ungoogled-chromium
      ```
    - OBS (Fedora 32)
      ```sh
      # dnf config-manager --add-repo https://download.opensuse.org/repositories/home:wchen342:ungoogled-chromium-fedora/Fedora_32/home:wchen342:ungoogled-chromium-fedora.repo
      # dnf install ungoogled-chromium
      ```
    - OBS (CentOS 8)
      ```sh
      # cd /etc/yum.repos.d/
      # wget https://download.opensuse.org/repositories/home:wchen342:ungoogled-chromium-fedora/CentOS_8/home:wchen342:ungoogled-chromium-fedora.repo
      # yum install ungoogled-chromium
      ```
    - OBS (CentOS 7)
      ```sh
      # cd /etc/yum.repos.d/
      # wget https://download.opensuse.org/repositories/home:wchen342:ungoogled-chromium-fedora/CentOS_7/home:wchen342:ungoogled-chromium-fedora.repo
      # yum install ungoogled-chromium
      ```

## Building
The following steps are for Fedora. For CentOS, extra files are needed. See `sources`.

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
