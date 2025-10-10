<p align="center"><img src="https://raw.githubusercontent.com/collective-context/ccc-code/refs/heads/main/logo.png" width="400" alt="CCC CODE" /><a href="https://Collective-Context.org">

  <br>
</p>

<h2 align="center">An essential toolset that eases NGINX site and server administration</h2>

<p align="center">
<img src="https://raw.githubusercontent.com/collective-context/ccc-code/refs/heads/main/intro.gif" width="800" alt="CCC CODE Intro" />
</p>

<p align="center">
<a href="https://github.com/WordOps/WordOps/actions" target="_blank"><img src="https://github.com/WordOps/WordOps/actions/workflows/main.yml/badge.svg?branch=master" alt="CI"></a>
<img src="https://img.shields.io/github/license/wordops/wordops.svg?cacheSeconds=86400" alt="MIT">
<img src="https://img.shields.io/github/last-commit/wordops/wordops.svg?cacheSeconds=86400" alt="Commits">
<img alt="GitHub release" src="https://img.shields.io/github/release/WordOps/WordOps.svg">
<br><a href="https://pypi.org/project/wordops/" target="_blank"><img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/wordops.svg?cacheSeconds=86400"></a>
<a href="https://twitter.com/WordOps_" target="_blank"><img src="https://img.shields.io/badge/twitter-%40WordOps__-blue.svg?style=flat&logo=twitter&cacheSeconds=86400" alt="Badge Twitter" /></a>
</p>

<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#usage">Usage</a> •
  <a href="https://github.com/WordOps/WordOps/projects">RoadMap</a> •
  <a href="https://github.com/WordOps/WordOps/blob/master/CHANGELOG.md">Changelog</a> •
  <a href="#credits">Credits</a> •
  <a href="#license">License</a>
</p>
<p align="center">
<a href="https://wordops.net" target="_blank"> WordOps.net</a> •
<a href="https://docs.wordops.net" target="_blank">Documentation</a> •
<a href="https://community.wordops.net" target="_blank">Community Forum</a> •
<a href="https://demo.wordops.eu" target="_blank">Dashboard demo</a>
</p>

---

## Key Features

-   **Easy to install** : One step automated installer
-   **Fast deployment** : Fast and automated BookStack, Nginx, PHP, MySQL & Redis installation
-   **Custom Nginx build** : Nginx 1.28.0 - TLS v1.3 HTTP/3 QUIC & Brotli support
-   **Up-to-date** : PHP 7.4, 8.0, 8.1, 8.2, 8.3 & 8.4 - MySQL8 & Redis 7.0
-   **Secured** : Hardened security with strict Nginx location directives
-   **Powerful** : Optimized Nginx configurations with multiple cache backends support
-   **SSL** : Domain, Subdomain & Wildcard Let's Encrypt SSL certificates with DNS API support
-   **Modern** : Strong ciphers_suite, modern TLS protocols and HSTS support ...
-   **Monitoring** : Live Monitoring ...
-   **User Friendly** : CCC CODE dashboard with ...
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
-   Debian 13 (Noble)

## Getting Started

```bash
wget -qO wo ccc.recode.at && sudo bash ccc      # Install CCC CODE
sudo ccc site create example.com --bs           # Install required packages & setup BuckStack on example.com
```

Detailed Getting Started guide with additional installation methods can be found in [the documentation](https://docs.wordops.net/getting-started/installation-guide/).

## Usage

### Standard BookStack sites

```bash
ccc site create example.com --bs                # install BookStack with [Current supported PHP release](https://endoflife.date/php) without any page caching
ccc site create example.com --bs  --php84       # install BookStack with PHP 8.4  without any page caching
ccc site create example.com --bsfc              # install BookStack + nginx fastcgi_cache
ccc site create example.com --bsredis           # install BookStack + nginx redis_cache
ccc site create example.com --bsrocket          # install BookStack with BS-Rocket plugin
ccc site create example.com --bsce              # install BookStack with Cache-enabler plugin
ccc site create example.com --bssc              # install BookStack with bs-super-cache plugin
```

### BookStack multisite with subdirectory

```bash
ccc site create example.com --bssubdir            # install bsmu-subdirectory without any page caching
ccc site create example.com --bssubdir --bssc     # install bsmu-subdirectory with BS-super-cache plugin
ccc site create example.com --bssubdir --bsfc     # install bsmu-subdirectory + nginx fastcgi_cache
ccc site create example.com --bssubdir --bsredis  # install bsmu-subdirectory + nginx redis_cache
ccc site create example.com --bssubdir --bsrocket # install bsmu-subdirectory + BS-Rocket plugin
ccc site create example.com --bssubdir --bsce     # install bsmu-subdirectory + Cache-Enabler plugin
```

### BookStack multisite with subdomain

```bash
ccc site create example.com --bssubdomain            # install bsmu-subdomain without any page caching
ccc site create example.com --bssubdomain --bssc     # install bsmu-subdomain with BS-super-cache plugin
ccc site create example.com --bssubdomain --bsfc     # install bsmu-subdomain + nginx fastcgi_cache
ccc site create example.com --bssubdomain --bsredis  # install bsmu-subdomain + nginx redis_cache
ccc site create example.com --bssubdomain --bsrocket # install bsmu-subdomain + BS-Rocket plugin
ccc site create example.com --bssubdomain --bsce     # install bsmu-subdomain + Cache-Enabler plugin
```

### Non-BookStack sites

```bash
ccc site create example.com --html     # create example.com for static/html sites
ccc site create example.com --php      # create example.com with [Current supported PHP release](https://endoflife.date/php)
ccc site create example.com --php81      # create example.com with php 8.1 support
ccc site create example.com --php82      # create example.com with php 8.2 support
ccc site create example.com --php84      # create example.com with php 8.4 support
ccc site create example.com --mysql    # create example.com with php 8.2 & mysql support
ccc site create example.com --mysql --php83   # create example.com with php 8.3 & mysql support
ccc site create example.com --proxy=127.0.0.1:3000 #  create example.com with nginx as reverse-proxy
```

### Switch between PHP versions

```bash
ccc site update example.com --php74 # switch to PHP 7.4
ccc site update example.com --php80 # switch to PHP 8.0
ccc site update example.com --php81 # switch to PHP 8.1
ccc site update example.com --php82 # switch to PHP 8.2
ccc site update example.com --php83 # switch to PHP 8.3
ccc site update example.com --php84 # switch to PHP 8.4
```

### Sites secured with Let's Encrypt

```bash
ccc site create example.com --bs -le #  BookStack & Letsencrypt
ccc site create sub.example.com --bs -le # BookStack & Letsencrypt subdomain
ccc site create example.com --bs --letsencrypt --hsts # BookStack & Letsencrypt with HSTS
ccc site create example.com --bs -le=wildcard --dns=dns_cf # BookStack & Wildcard SSL certificate with Cloudflare DNS API
```

## Update CCC CODE

```bash
ccc update
```

## Support

If you feel there is a bug directly related to WordOps, or if you want to suggest new features for WordOps, feel free to open an issue.
For any other questions about WordOps or if you need support, please use the [Community Forum](https://community.wordops.net/).

## Contributing

If you'd like to contribute, please fork the repository and make changes as you'd like. Pull requests are warmly welcome.
There is no need to be a developer or a system administrator to contribute to WordOps project. You can still contribute by helping us to improve [WordOps documentation](https://github.com/WordOps/docs.wordops.net).
Otherwise, you can still contribute to the project by making a donation on [Ko-Fi](https://ko-fi.com/wordops).

## Sponsors

Thanks to our generous sponsors for supporting the development of WordOps:

| [Liquid Web](https://www.liquidweb.com/)                                                                                                               |
| ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| <a href="https://www.liquidweb.com/" target="_blank"><img src="https://docs.wordops.net/images/liquid-web.png" alt="Liquid Web logo" width="200"/></a> |

## Credits

-   Source : [EasyEngine](https://github.com/easyengine/easyengine)

Apps & Tools shipped with CCC CODE :

-   [Acme.sh](https://github.com/Neilpang/acme.sh)
-   [BS-CLI](https://github.com/BS-cli/BS-cli)
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

-   [Nginx-wo by CCC CODE](https://build.opensuse.org/package/show/home:virtubox:WordOps/nginx)
-   [PHP by Ondřej Surý](https://launchpad.net/~ondrej/+archive/ubuntu/php)
-   [Redis](https://redis.io/docs/getting-started/installation/install-redis-on-linux/)

Cache Plugins supported by CCC CODE :

-   [Nginx-helper](https://github.com/rtCamp/nginx-helper)
-   [Cache-Enabler](https://github.com/keycdn/cache-enabler)
-   [Redis-object-cache](https://github.com/tillkruss/redis-cache)
-   [BS-Super-Cache](https://github.com/Automattic/BS-super-cache)
-   [BS-Rocket](https://github.com/BS-media/BS-rocket)

## License

-   [MIT](http://opensource.org/licenses/MIT) © [WordOps](https://wordops.net)
-   [MIT](http://opensource.org/licenses/MIT) © [recode@ /CCC](https://Collective-Context.org)
