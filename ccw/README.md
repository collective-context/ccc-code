<p align="center"><img src="https://raw.githubusercontent.com/collective-context/ccc-code/master/logo.png" width="400" alt="CCC CODE" /><a href="https://collective-context.org">

  <br>
</p>

<h2 align="center">An essential toolset that eases CCC CODE site and server administration</h2>

<p align="center">
<img src="https://docs.collective-context.org/images/ccc-code-intro.gif" width="800" alt="CCC CODE" />
</p>

<p align="center">
<a href="https://github.com/collective-context/ccc-code/actions" target="_blank"><img src="https://github.com/collective-context/ccc-code/actions/workflows/main.yml/badge.svg?branch=refactor-wo-to-ccw" alt="CI"></a>
<img src="https://img.shields.io/github/license/collective-context/ccc-code.svg?cacheSeconds=86400" alt="MIT">
<img src="https://img.shields.io/github/last-commit/collective-context/ccc-code.svg?cacheSeconds=86400" alt="Commits">
<img alt="GitHub release" src="https://img.shields.io/github/release/collective-context/ccc-code.svg">
<br><a href="https://pypi.org/project/ccc-code/" target="_blank"><img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/ccc-code.svg?cacheSeconds=86400"></a>
<a href="https://twitter.com/collective_context" target="_blank"><img src="https://img.shields.io/badge/twitter-%40collective_context-blue.svg?style=flat&logo=twitter&cacheSeconds=86400" alt="Badge Twitter" /></a>
</p>

<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#usage">Usage</a> •
  <a href="https://github.com/collective-context/ccc-code/projects">RoadMap</a> •
  <a href="https://github.com/collective-context/ccc-code/blob/refactor-wo-to-ccw/CHANGELOG.md">Changelog</a> •
  <a href="#credits">Credits</a> •
  <a href="#license">License</a>
</p>
<p align="center">
<a href="https://collective-context.org" target="_blank"> CCC-CODE.org</a> •
<a href="https://docs.collective-context.org" target="_blank">Documentation</a> •
<a href="https://community.collective-context.org" target="_blank">Community Forum</a> •
<a href="https://demo.collective-context.org" target="_blank">Dashboard demo</a>
</p>

---

## Key Features

-   **Easy to install** : One step automated installer with migration from EasyEngine v3 support
-   **Fast deployment** : Fast and automated CCC CODE, Nginx, PHP, MySQL & Redis installation
-   **Custom Nginx build** : Nginx 1.28.0 - TLS v1.3 HTTP/3 QUIC & Brotli support
-   **Up-to-date** : PHP 7.4, 8.0, 8.1, 8.2, 8.3 & 8.4 - MariaDB 11.4 LTS & Redis 7.0
-   **Secured** : Hardened CCC CODE security with strict Nginx location directives
-   **Powerful** : Optimized Nginx configurations with multiple cache backends support
-   **SSL** : Domain, Subdomain & Wildcard Let's Encrypt SSL certificates with DNS API support
-   **Modern** : Strong ciphers_suite, modern TLS protocols and HSTS support (Grade A+ on [ssllabs](https://www.ssllabs.com/ssltest/analyze.html?d=demo.collective-context.org&latest))
-   **Monitoring** : Live Nginx vhost traffic with ngx_vts_module and server monitoring with Netdata
-   **User Friendly** : CCC CODE dashboard with server status/monitoring and tools ([demo](https://demo.collective-context.org))
-   **Release cycle** : CCC CODE stable releases are published in June and December.

---

## Requirements

### Operating System

#### Recommended

-   Ubuntu 24.04 LTS (Noble)
-   Ubuntu 22.04 LTS (Jammy)
-   Ubuntu 20.04 LTS (Focal)

#### Also compatible

-   Debian 11 (Bullseye)
-   Debian 12 (Bookworm)

#### For testing purpose only

-   Raspbian 11 (Bullseye)

## Getting Started

```bash
wget -qO ccw ccw.cc && sudo bash ccw      # Install CCC CODE
sudo ccw site create example.com --wp     # Install required packages & setup CCC CODE on example.com
```

Detailed Getting Started guide with additional installation methods can be found in [the documentation](https://docs.collective-context.org/getting-started/installation-guide/).

## Usage

### Standard CCC CODE sites

```bash
ccw site create example.com --wp                # install ccc-code with [Current supported PHP release](https://endoflife.date/php) without any page caching
ccw site create example.com --wp  --php84       # install ccc-code with PHP 8.4  without any page caching
ccw site create example.com --wpfc              # install ccc-code + nginx fastcgi_cache
ccw site create example.com --wpredis           # install ccc-code + nginx redis_cache
ccw site create example.com --wprocket          # install ccc-code with WP-Rocket plugin
ccw site create example.com --wpce              # install ccc-code with Cache-enabler plugin
ccw site create example.com --wpsc              # install ccc-code with wp-super-cache plugin
```

### CCC CODE multisite with subdirectory

```bash
ccw site create example.com --wpsubdir            # install wpmu-subdirectory without any page caching
ccw site create example.com --wpsubdir --wpsc     # install wpmu-subdirectory with wp-super-cache plugin
ccw site create example.com --wpsubdir --wpfc     # install wpmu-subdirectory + nginx fastcgi_cache
ccw site create example.com --wpsubdir --wpredis  # install wpmu-subdirectory + nginx redis_cache
ccw site create example.com --wpsubdir --wprocket # install wpmu-subdirectory + WP-Rocket plugin
ccw site create example.com --wpsubdir --wpce     # install wpmu-subdirectory + Cache-Enabler plugin
```

### CCC CODE multisite with subdomain

```bash
ccw site create example.com --wpsubdomain            # install wpmu-subdomain without any page caching
ccw site create example.com --wpsubdomain --wpsc     # install wpmu-subdomain with wp-super-cache plugin
ccw site create example.com --wpsubdomain --wpfc     # install wpmu-subdomain + nginx fastcgi_cache
ccw site create example.com --wpsubdomain --wpredis  # install wpmu-subdomain + nginx redis_cache
ccw site create example.com --wpsubdomain --wprocket # install wpmu-subdomain + WP-Rocket plugin
ccw site create example.com --wpsubdomain --wpce     # install wpmu-subdomain + Cache-Enabler plugin
```

### Non-CCC CODE sites

```bash
ccw site create example.com --html     # create example.com for static/html sites
ccw site create example.com --php      # create example.com with [Current supported PHP release](https://endoflife.date/php)
ccw site create example.com --php81      # create example.com with php 8.1 support
ccw site create example.com --php82      # create example.com with php 8.2 support
ccw site create example.com --php84      # create example.com with php 8.4 support
ccw site create example.com --mysql    # create example.com with php 8.2 & mysql support
ccw site create example.com --mysql --php83   # create example.com with php 8.3 & mysql support
ccw site create example.com --proxy=127.0.0.1:3000 #  create example.com with nginx as reverse-proxy
```

### Switch between PHP versions

```bash
ccw site update example.com --php74 # switch to PHP 7.4
ccw site update example.com --php80 # switch to PHP 8.0
ccw site update example.com --php81 # switch to PHP 8.1
ccw site update example.com --php82 # switch to PHP 8.2
ccw site update example.com --php83 # switch to PHP 8.3
ccw site update example.com --php84 # switch to PHP 8.4
```

### Sites secured with Let's Encrypt

```bash
ccw site create example.com --wp -le #  ccc-code & letsencrypt
ccw site create sub.example.com --wp -le # ccc-code & letsencrypt subdomain
ccw site create example.com --wp --letsencrypt --hsts # ccc-code & letsencrypt with HSTS
ccw site create example.com --wp -le=wildcard --dns=dns_cf # ccc-code & wildcard SSL certificate with Cloudflare DNS API
```

## Update CCC CODE

```bash
ccw update
```

## Support

If you feel there is a bug directly related to CCC CODE, or if you want to suggest new features for CCC CODE, feel free to open an issue.
For any other questions about CCC CODE or if you need support, please use the [Community Forum](https://community.collective-context.org/).

## Contributing

If you'd like to contribute, please fork the repository and make changes as you'd like. Pull requests are warmly welcome.
There is no need to be a developer or a system administrator to contribute to CCC CODE project. You can still contribute by helping us to improve [CCC CODE documentation](https://github.com/collective-context/docs.collective-context.org).
Otherwise, you can still contribute to the project by making a donation on [Ko-Fi](https://ko-fi.com/collective-context).

## Sponsors

Thanks to our generous sponsors for supporting the development of CCC CODE:

| [Liquid Web](https://www.liquidweb.com/)                                                                                                               |
| ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| <a href="https://www.liquidweb.com/" target="_blank"><img src="https://docs.collective-context.org/images/liquid-web.png" alt="Liquid Web logo" width="200"/></a> |

## Credits

-   Source : [EasyEngine](https://github.com/easyengine/easyengine)

Apps & Tools shipped with CCC CODE :

-   [Acme.sh](https://github.com/Neilpang/acme.sh)
-   [WP-CLI](https://github.com/wp-cli/wp-cli)
-   [Netdata](https://github.com/netdata/netdata)
-   [phpMyAdmin](https://www.phpmyadmin.net/)
-   [Composer](https://github.com/composer/composer)
-   [Adminer](https://www.adminer.org/)
-   [phpRedisAdmin](https://github.com/erikdubbelboer/phpRedisAdmin)
-   [opcacheGUI](https://github.com/amnuts/opcache-gui)
-   [eXtplorer](https://github.com/soerennb/extplorer)
-   [Webgrind](https://github.com/jokkedk/webgrind)
-   [MySQLTuner](https://github.com/major/MySQLTuner-perl)
-   [Fail2Ban](https://github.com/fail2ban/fail2ban)
-   [ClamAV](https://github.com/Cisco-Talos/clamav-devel)
-   [cheat.sh](https://github.com/chubin/cheat.sh)
-   [ProFTPd](https://github.com/proftpd/proftpd)
-   [Nginx-ultimate-bad-bot-blocker](https://github.com/mitchellkrogza/nginx-ultimate-bad-bot-blocker/)
-   [Nanorc](https://github.com/scopatz/nanorc)

Third-party debian packages shipped with CCC CODE :

-   [Nginx-ccw by CCC CODE](https://build.opensuse.org/package/show/home:virtubox:CCC-CODE/nginx)
-   [PHP by Ondřej Surý](https://launchpad.net/~ondrej/+archive/ubuntu/php)
-   [Redis](https://redis.io/docs/getting-started/installation/install-redis-on-linux/)

CCC CODE Cache Plugins supported by CCC CODE :

-   [Nginx-helper](https://github.com/rtCamp/nginx-helper)
-   [Cache-Enabler](https://github.com/keycdn/cache-enabler)
-   [Redis-object-cache](https://github.com/tillkruss/redis-cache)
-   [WP-Super-Cache](https://github.com/Automattic/wp-super-cache)
-   [WP-Rocket](https://github.com/wp-media/wp-rocket)

## License

-   [MIT](http://opensource.org/licenses/MIT) © [CCC CODE](https://collective-context.org)

<!-- Zuletzt bearbeitet: 2025-10-27 -->
