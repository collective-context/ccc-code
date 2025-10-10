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

