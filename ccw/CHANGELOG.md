# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),

## Releases

### v3.22.0 - [Unreleased]

#### Added

-   Add PHP 8.4 support by @VirtuBox

#### Changed

-   Default PHP version bumped to 8.3 by @VirtuBox

#### Fixed

-   Fix html site creation by @VirtuBox in #703

### v3.21.3 - 2024-06-14

#### Added

-   Add Ubuntu 24.04 LTS support

#### Changed

-   Use MariaDB dynamic mirror by @VirtuBox in #673

#### Fixed

-   Fix mariadb repo migration by @VirtuBox in #668

### v3.21.2 - 2024-06-11

#### Added

-   "$http3" variable in access_logs

#### Fixed

-   $host variable for fastcgi_params et proxy_params

### v3.21.1 - 2024-06-11

#### Fixed

-   `wo stack migrate --nginx` when using wildcard certificate

### v3.21.0 - 2024-06-10

#### Added

-   New Nginx package with HTTP/3 QUIC support
-   `wo stack install/remove --brotli` to enable/disable brotli compression
-   `wo stack migrate --nginx` to upgrade Nginx configuration with HTTP/3 QUIC

#### Changed

-   Bump MariaDB release to v11.4
-   Remove php72 and php73 stacks
-   All APT repositories are properly signed with gpg keys
-   Netdata is installed from debian packages when available
-   Less logs in acme.sh operation
-   Migrate all repositories in /etc/apt/sources.list.d/wo-repo.list in indivual files like mariadb.list, redis.list, wordops.list

#### Fixed

-   wo info php versions display
-   Repositories's gpg keys are not managed with apt-key anymore
-   `wo site update site.tld --hsts` errors
-   `wo site update site.tld --ngxblocker` errors
-   Netdata install and upgrade
-   22222 Backend not secure with valid SSL certificate

#### Security

-   Fix [CVE-2024-34528](https://github.com/advisories/GHSA-23qq-p4gq-gc2g)

### v3.20.0 - 2024-04-21

#### Added

-   Create subsite by @doofusdavid in [PR #598](https://github.com/WordOps/WordOps/pull/598)

#### Fixed

-   Fix PHP{version}-FPM is not installed and fix support for php 8.3 by @gabrielgiordan in [PR #604](https://github.com/WordOps/WordOps/pull/604)
-   do not cache wishlist by @admarty in [PR #608](https://github.com/WordOps/WordOps/pull/608)
-   Update install by @michaelangelocobo in [PR #628](https://github.com/WordOps/WordOps/pull/628)
-   Fix WordOps server ip check in Nginx stack install
-   Fix WordOps create new site duration

### v3.19.1 - 2023-12-03

#### Fixed

-   fix missing braces on force-ssl.mustache [PR #593](https://github.com/WordOps/WordOps/pull/593) @janiosarmento

### v3.19.0 - 2023-12-01

#### Added

-   PHP 8.3 support
-   force-ssl-{domain}.conf now available as a mustache template

#### Changed

-   Default PHP version bump to 8.2

#### Fixed

-   wo site update --phpXX errors in some case

#### Fixed

### v3.18.1 - 2023-09-26

#### Fixed

-   `wo site update` not changing site's php version
-   Netdata install with a remote MySQL server
-   Remove outdated Anemometer package
-   Update bash_completion

### v3.18.0 - 2023-08-28

#### Added

-   Alias site support with `wo site create site.tld --alias othersite.tld`
-   MariaDB version choice in `/etc/wo/wo.conf` (before install or before `wo stack migrate` usage)

#### Changed

-   Improve php versions management to support next php releases
-   Refactor WordOps code to make it simpler and easier to edit
-   Update ProFTPd umask to avoid permission issues
-   Deploy ssl.conf from a mustache template to allow customization
-   Do not cache requests with Authorization header set [PR #548](https://github.com/WordOps/WordOps/pull/548) @nylen

#### Fixed

-   Netdata install and upgrade
-   `wo site create site.tld --proxy` not working with `-le`
-   `wo stack migrate --mariadb` version detection
-   Ability to set default php version in `/etc/wo/wo.conf` not working as expected

### v3.17.0 - 2023-08-04

#### Added

-   Debian 12 support

#### Changed

-   MariaDB default version is now 10.11
-   `wo stack migrate --mariadb` improved to properly upgrade mariadb
-   New Nginx package based on latest Nginx stable release 1.24.0
-   Update memory limit to WooCommerce recommended requirements ([PR #512](https://github.com/WordOps/WordOps/pull/512)) @yogeshbeniwal

### v3.16.3 - 2023-01-29

#### Fixed

-   SQLAlchemy version locked

### v3.16.2 - 2023-01-21

#### Changed

-   Allow all Communications Between Jetpack and WordPress.com ([PR #494](https://github.com/WordOps/WordOps/pull/494)) @ihfbib

#### Fixed

-   GPG keys for Nginx repository on Debian
-   Extplorer update for PHP 8.x

### v3.16.1 - 2022-12-26

#### Fixed

-   PHP 8.2 install not working with `wo site update` ([PR #487](https://github.com/WordOps/WordOps/pull/487)) @janiosarmento

### v3.16.0 - 2022-12-22

#### Added

-   Add PHP 8.2 support ([PR #482](https://github.com/WordOps/WordOps/pull/483)) @janiosarmento
-   Prompt user before WordOps update with `wo update`

#### Changed

-   Default PHP version bumped to 8.1

#### Fixed

-   psutil dependency upgrade
-   Fix wrong else statements in stack_services.py ([PR #475](https://github.com/WordOps/WordOps/pull/475)) @stodorovic

### v3.15.4 - 2022-10-25

#### Fixed

-   Nginx prefetch-proxy configuration
-   Linux distribution variable not set properly

### v3.15.3 - 2022-10-24

#### Added

-   Support for Debian 10/11

#### Changed

-   Install redis from official repository
-   Redis version bump to 7.0.5
-   WP-CLI version bump to 2.7.1
-   Remove outdated Nginx directives
-   Updated repository GPG Key
-   UFW stack detect proftpd during install

#### Fixed

-   Netdata upgrade failure on old servers
-   MariaDB service disabled after upgrade with `wo stack migrate --mariadb`
-   Proftpd install on Ubuntu 22.04 and Debian 11

### v3.15.2 - 2022-09-23

#### Added

-   Add support for Chrome Privacy Preserving Prefetch Proxy [Issue 440](https://github.com/WordOps/WordOps/issues/440)

#### Changed

-   Cloudflare IP script for Nginx now fetch Cloudflare IPs using the API

#### Fixed

-   wo secure --auth on Ubuntu 22.04

### v3.15.1 - 2022-09-09

#### Fixed

-   Hotfix outdated python distro package cause issues on some servers

### v3.15.0 - 2022-09-09

#### Added

-   Ubuntu 22.04 LTS Support

#### Changed

-   New Nginx package based on latest Nginx stable release 1.22.2
-   Better Referrer-Policy ([PR #434](https://github.com/WordOps/WordOps/pull/434))
-   MariaDB default version is now 10.6

#### Fixed

-   `wo log reset --all` ([PR #438](https://github.com/WordOps/WordOps/pull/438))
-   Outdated Nginx directives
-   Netdata stack upgrade([PR #439](https://github.com/WordOps/WordOps/pull/439))

### v3.14.2 - 2022-04-29

#### Fixed

-   Git unsafe directories issue
-   WP_DEBUG variable in wp-config.php

### v3.14.1 - 2022-02-16

#### Fixed

-   Cloudflare IP range script ([PR #422](https://github.com/WordOps/WordOps/pull/422))
-   Netdata stack installation
-   Missing php upstream in WordOps backend

### v3.14.0 - 2022-01-26

#### Added

-   PHP 8.0 and 8.1 support ([PR #413](https://github.com/WordOps/WordOps/pull/413))
-   Support arm64 architecture ([PR #392](https://github.com/WordOps/WordOps/pull/392))

#### Changed

-   Update WP-CLI to v2.6.0 with PHP 8.0/8.1 support
-   Update adminer to v4.8.1
-   Update Redis repository ([PR #377](https://github.com/WordOps/WordOps/pull/377))
-   Set PHP 8.0 as default PHP version. Can be changed in `/etc/wo/wo.conf`

#### Fixed

-   WordOps install script issues
-   acme.sh issues with zero-ssl CA

