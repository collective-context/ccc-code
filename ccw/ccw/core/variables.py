"""CCC CODE core variable module"""
import configparser
import os
import sys
from datetime import datetime
from re import match
from socket import getfqdn
from shutil import copy2

from distro import distro, linux_distribution
from sh import git


class CCWVar():
    """Intialization of core variables"""

    # CCC CODE version
    ccw_version = "3.22.0"
    # CCC CODE packages versions
    ccw_adminer = "4.8.1"
    ccw_phpmyadmin = "5.2.0"
    ccw_extplorer = "2.1.15"
    ccw_dashboard = "1.3"

    # Get WPCLI path
    wpcli_url = "https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar"
    ccw_wpcli_path = '/usr/local/bin/wp'

    # Current date and time of System
    ccw_date = datetime.now().strftime('%d%b%Y-%H-%M-%S')

    # CCC CODE core variables
    # linux distribution
    if sys.version_info <= (3, 5):
        ccw_distro = linux_distribution(
            full_distribution_name=False)[0].lower()
        ccw_platform_version = linux_distribution(
            full_distribution_name=False)[1].lower()
        # distro codename (bionic, xenial, stretch ...)
        ccw_platform_codename = linux_distribution(
            full_distribution_name=False)[2].lower()
    else:
        ccw_distro = distro.id()
        ccw_platform_version = distro.version()
        # distro codename (bionic, xenial, stretch ...)
        ccw_platform_codename = distro.codename()

    # Get timezone of system
    if os.path.isfile('/etc/timezone'):
        with open("/etc/timezone", mode='r', encoding='utf-8') as tzfile:
            ccw_timezone = tzfile.read().replace('\n', '')
            if ccw_timezone == "Etc/UTC":
                ccw_timezone = "UTC"
    else:
        ccw_timezone = "Europe/Amsterdam"

    # Get FQDN of system
    ccw_fqdn = getfqdn()

    # CCC CODE default webroot path
    ccw_webroot = '/var/www/'

    # CCC CODE default renewal  SSL certificates path
    ccw_ssl_archive = '/etc/letsencrypt/renewal'

    # CCC CODE default live SSL certificates path
    ccw_ssl_live = '/etc/letsencrypt/live'

    # PHP user
    ccw_php_user = 'www-data'

    # CCC CODE git configuration management
    config = configparser.ConfigParser()
    config.read(os.path.expanduser("~") + '/.gitconfig')
    try:
        ccw_user = config['user']['name']
        ccw_email = config['user']['email']
    except Exception:
        print("CCC CODE (ccw) require an username & and an email "
              "address to configure Git (used to save server configurations)")
        print("Your informations will ONLY be stored locally")

        ccw_user = input("Enter your name: ")
        while ccw_user == "":
            print("Unfortunately, this can't be left blank")
            ccw_user = input("Enter your name: ")

        ccw_email = input("Enter your email: ")

        while not match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$",
                        ccw_email):
            print("Whoops, seems like you made a typo - "
                  "the e-mail address is invalid...")
            ccw_email = input("Enter your email: ")

        git.config("--global", "user.name", "{0}".format(ccw_user))
        git.config("--global", "user.email", "{0}".format(ccw_email))

    if not os.path.isfile('/root/.gitconfig'):
        copy2(os.path.expanduser("~") + '/.gitconfig', '/root/.gitconfig')

    # MySQL hostname
    ccw_mysql_host = ""
    config = configparser.RawConfigParser()
    if os.path.exists('/etc/mysql/conf.d/my.cnf'):
        cnfpath = "/etc/mysql/conf.d/my.cnf"
    else:
        cnfpath = os.path.expanduser("~") + "/.my.cnf"
    if [cnfpath] == config.read(cnfpath):
        try:
            ccw_mysql_host = config.get('client', 'host')
        except configparser.NoOptionError:
            ccw_mysql_host = "localhost"
    else:
        ccw_mysql_host = "localhost"

    # CCC CODE stack installation variables
    # Nginx repo and packages
    if ccw_distro == 'ubuntu':
        ccw_nginx_repo = "ppa:wordops/nginx-wo"

    else:
        if ccw_distro == 'debian':
            if ccw_platform_codename == 'buster':
                ccw_deb_repo = "Debian_10"
            elif ccw_platform_codename == 'bullseye':
                ccw_deb_repo = "Debian_11"
            elif ccw_platform_codename == 'bookworm':
                ccw_deb_repo = "Debian_12"
        elif ccw_distro == 'raspbian':
            if ccw_platform_codename == 'buster':
                ccw_deb_repo = "Raspbian_10"
            elif ccw_platform_codename == 'bullseye':
                ccw_deb_repo = "Raspbian_11"
            elif ccw_platform_codename == 'bookworm':
                ccw_deb_repo = "Raspbian_12"
        # debian/raspbian nginx repository
        ccw_nginx_repo = ("deb [signed-by=/usr/share/keyrings/wordops-archive-keyring.gpg] "
                         "http://download.opensuse.org"
                         f"/repositories/home:/virtubox:/WordOps/{ccw_deb_repo}/ /")
        ccw_nginx_key = (f"https://download.opensuse.org/repositories/home:virtubox:WordOps/{ccw_deb_repo}/Release.key")

    ccw_nginx = ["nginx-custom", "nginx-wo"]
    ccw_nginx_key = 'FB898660'

    ccw_php_versions = {
        'php74': '7.4',
        'php80': '8.0',
        'php81': '8.1',
        'php82': '8.2',
        'php83': '8.3',
        'php84': '8.4',
    }

    def generate_php_modules(version_prefix, version_number):
        ccw_module = ["bcmath", "cli", "common", "curl", "fpm", "gd", "igbinary",
                     "imagick", "imap", "intl", "mbstring", "memcached", "msgpack",
                     "mysql", "opcache", "readline", "redis", "soap", "xdebug",
                     "xml", "zip"]
        php_modules = ["php{0}-{1}".format(version_number, module) for module in ccw_module]

        if version_prefix == 'php74':
            php_modules.extend(["php{0}-geoip".format(version_number),
                                "php{0}-json".format(version_number)])

        return php_modules

    ccw_php74 = generate_php_modules('php74', '7.4')
    ccw_php80 = generate_php_modules('php80', '8.0')
    ccw_php81 = generate_php_modules('php81', '8.1')
    ccw_php82 = generate_php_modules('php82', '8.2')
    ccw_php83 = generate_php_modules('php83', '8.3')
    ccw_php84 = generate_php_modules('php84', '8.4')

    ccw_php_extra = ["graphviz"]

    ccw_mysql = [
        "mariadb-server", "percona-toolkit",
        "mariadb-common", "python3-mysqldb"]
    if ccw_distro == 'raspbian':
        mariadb_ver = '10.3'
    else:
        mariadb_ver = '11.4'
        ccw_mysql = ccw_mysql + ["mariadb-backup"]

    ccw_mysql_client = ["mariadb-client", "python3-mysqldb"]

    ccw_fail2ban = ["fail2ban"]
    ccw_clamav = ["clamav", "clamav-freshclam"]

    # APT repositories
    ccw_mysql_repo = ("deb [signed-by=/etc/apt/keyrings/mariadb-keyring.pgp] "
                     "http://deb.mariadb.org/"
                     f"{mariadb_ver}/{ccw_distro} {ccw_platform_codename} main")
    mariadb_repo_key = "https://mariadb.org/mariadb_release_signing_key.pgp"
    if ccw_distro == 'ubuntu':
        ccw_php_repo = "ppa:ondrej/php"
        ccw_goaccess_repo = ("ppa:alex-p/goaccess")

    else:
        ccw_php_repo = (
            "deb [signed-by=/usr/share/keyrings/deb.sury.org-php.gpg] "
            f"https://packages.sury.org/php/ {ccw_platform_codename} main")
        ccw_php_key = '95BD4743'
    ccw_redis_key_url = "https://packages.redis.io/gpg"
    ccw_redis_repo = (
        "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] "
        f"https://packages.redis.io/deb {ccw_platform_codename} main")

    ccw_redis = ['redis-server']

    netdata_script_url = "https://get.netdata.cloud/kickstart.sh"

    # Repo path
    ccw_repo_file = "ccw-repo.list"
    ccw_repo_file_path = ("/etc/apt/sources.list.d/" + ccw_repo_file)

    # Application dabase file path
    basedir = os.path.abspath(os.path.dirname('/var/lib/ccw/'))
    ccw_db_uri = 'sqlite:///' + os.path.join(basedir, 'dbase.db')

    def __init__(self):
        pass
