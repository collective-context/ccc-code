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


class CCCVar():
    """Intialization of core variables"""

    # CCC CODE version
    ccc_version = "3.22.0"
    # CCC CODE packages versions
    ccc_adminer = "4.8.1"
    ccc_phpmyadmin = "5.2.0"
    ccc_extplorer = "2.1.15"
    ccc_dashboard = "1.3"

    # Get WPCLI path
    wpcli_url = "https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar"
    ccc_wpcli_path = '/usr/local/bin/wp'

    # Current date and time of System
    ccc_date = datetime.now().strftime('%d%b%Y-%H-%M-%S')

    # CCC CODE core variables
    # linux distribution
    if sys.version_info <= (3, 5):
        ccc_distro = linux_distribution(
            full_distribution_name=False)[0].lower()
        ccc_platform_version = linux_distribution(
            full_distribution_name=False)[1].lower()
        # distro codename (bionic, xenial, stretch ...)
        ccc_platform_codename = linux_distribution(
            full_distribution_name=False)[2].lower()
    else:
        ccc_distro = distro.id()
        ccc_platform_version = distro.version()
        # distro codename (bionic, xenial, stretch ...)
        ccc_platform_codename = distro.codename()

    # Get timezone of system
    if os.path.isfile('/etc/timezone'):
        with open("/etc/timezone", mode='r', encoding='utf-8') as tzfile:
            ccc_timezone = tzfile.read().replace('\n', '')
            if ccc_timezone == "Etc/UTC":
                ccc_timezone = "UTC"
    else:
        ccc_timezone = "Europe/Amsterdam"

    # Get FQDN of system
    ccc_fqdn = getfqdn()

    # CCC CODE default webroot path
    ccc_webroot = '/var/www/'

    # CCC CODE default renewal  SSL certificates path
    ccc_ssl_archive = '/etc/letsencrypt/renewal'

    # CCC CODE default live SSL certificates path
    ccc_ssl_live = '/etc/letsencrypt/live'

    # PHP user
    ccc_php_user = 'www-data'

    # CCC CODE git configuration management
    config = configparser.ConfigParser()
    config.read(os.path.expanduser("~") + '/.gitconfig')
    try:
        ccc_user = config['user']['name']
        ccc_email = config['user']['email']
    except Exception:
        print("CCC CODE (ccc) require an username & and an email "
              "address to configure Git (used to save server configurations)")
        print("Your informations will ONLY be stored locally")

        ccc_user = input("Enter your name: ")
        while ccc_user == "":
            print("Unfortunately, this can't be left blank")
            ccc_user = input("Enter your name: ")

        ccc_email = input("Enter your email: ")

        while not match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$",
                        ccc_email):
            print("Whoops, seems like you made a typo - "
                  "the e-mail address is invalid...")
            ccc_email = input("Enter your email: ")

        git.config("--global", "user.name", "{0}".format(ccc_user))
        git.config("--global", "user.email", "{0}".format(ccc_email))

    if not os.path.isfile('/root/.gitconfig'):
        copy2(os.path.expanduser("~") + '/.gitconfig', '/root/.gitconfig')

    # MySQL hostname
    ccc_mysql_host = ""
    config = configparser.RawConfigParser()
    if os.path.exists('/etc/mysql/conf.d/my.cnf'):
        cnfpath = "/etc/mysql/conf.d/my.cnf"
    else:
        cnfpath = os.path.expanduser("~") + "/.my.cnf"
    if [cnfpath] == config.read(cnfpath):
        try:
            ccc_mysql_host = config.get('client', 'host')
        except configparser.NoOptionError:
            ccc_mysql_host = "localhost"
    else:
        ccc_mysql_host = "localhost"

    # CCC CODE stack installation variables
    # Nginx repo and packages
    if ccc_distro == 'ubuntu':
        ccc_nginx_repo = "ppa:wordops/nginx-wo"

    else:
        if ccc_distro == 'debian':
            if ccc_platform_codename == 'buster':
                ccc_deb_repo = "Debian_10"
            elif ccc_platform_codename == 'bullseye':
                ccc_deb_repo = "Debian_11"
            elif ccc_platform_codename == 'bookworm':
                ccc_deb_repo = "Debian_12"
        elif ccc_distro == 'raspbian':
            if ccc_platform_codename == 'buster':
                ccc_deb_repo = "Raspbian_10"
            elif ccc_platform_codename == 'bullseye':
                ccc_deb_repo = "Raspbian_11"
            elif ccc_platform_codename == 'bookworm':
                ccc_deb_repo = "Raspbian_12"
        # debian/raspbian nginx repository
        ccc_nginx_repo = ("deb [signed-by=/usr/share/keyrings/wordops-archive-keyring.gpg] "
                         "http://download.opensuse.org"
                         f"/repositories/home:/virtubox:/WordOps/{ccc_deb_repo}/ /")
        ccc_nginx_key = (f"https://download.opensuse.org/repositories/home:virtubox:WordOps/{ccc_deb_repo}/Release.key")

    ccc_nginx = ["nginx-custom", "nginx-wo"]
    ccc_nginx_key = 'FB898660'

    ccc_php_versions = {
        'php74': '7.4',
        'php80': '8.0',
        'php81': '8.1',
        'php82': '8.2',
        'php83': '8.3',
        'php84': '8.4',
    }

    def generate_php_modules(version_prefix, version_number):
        ccc_module = ["bcmath", "cli", "common", "curl", "fpm", "gd", "igbinary",
                     "imagick", "imap", "intl", "mbstring", "memcached", "msgpack",
                     "mysql", "opcache", "readline", "redis", "soap", "xdebug",
                     "xml", "zip"]
        php_modules = ["php{0}-{1}".format(version_number, module) for module in ccc_module]

        if version_prefix == 'php74':
            php_modules.extend(["php{0}-geoip".format(version_number),
                                "php{0}-json".format(version_number)])

        return php_modules

    ccc_php74 = generate_php_modules('php74', '7.4')
    ccc_php80 = generate_php_modules('php80', '8.0')
    ccc_php81 = generate_php_modules('php81', '8.1')
    ccc_php82 = generate_php_modules('php82', '8.2')
    ccc_php83 = generate_php_modules('php83', '8.3')
    ccc_php84 = generate_php_modules('php84', '8.4')

    ccc_php_extra = ["graphviz"]

    ccc_mysql = [
        "mariadb-server", "percona-toolkit",
        "mariadb-common", "python3-mysqldb"]
    if ccc_distro == 'raspbian':
        mariadb_ver = '10.3'
    else:
        mariadb_ver = '11.4'
        ccc_mysql = ccc_mysql + ["mariadb-backup"]

    ccc_mysql_client = ["mariadb-client", "python3-mysqldb"]

    ccc_fail2ban = ["fail2ban"]
    ccc_clamav = ["clamav", "clamav-freshclam"]

    # APT repositories
    ccc_mysql_repo = ("deb [signed-by=/etc/apt/keyrings/mariadb-keyring.pgp] "
                     "http://deb.mariadb.org/"
                     f"{mariadb_ver}/{ccc_distro} {ccc_platform_codename} main")
    mariadb_repo_key = "https://mariadb.org/mariadb_release_signing_key.pgp"
    if ccc_distro == 'ubuntu':
        ccc_php_repo = "ppa:ondrej/php"
        ccc_goaccess_repo = ("ppa:alex-p/goaccess")

    else:
        ccc_php_repo = (
            "deb [signed-by=/usr/share/keyrings/deb.sury.org-php.gpg] "
            f"https://packages.sury.org/php/ {ccc_platform_codename} main")
        ccc_php_key = '95BD4743'
    ccc_redis_key_url = "https://packages.redis.io/gpg"
    ccc_redis_repo = (
        "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] "
        f"https://packages.redis.io/deb {ccc_platform_codename} main")

    ccc_redis = ['redis-server']

    netdata_script_url = "https://get.netdata.cloud/kickstart.sh"

    # Repo path
    ccc_repo_file = "ccc-repo.list"
    ccc_repo_file_path = ("/etc/apt/sources.list.d/" + ccc_repo_file)

    # Application dabase file path
    basedir = os.path.abspath(os.path.dirname('/var/lib/ccc/'))
    ccc_db_uri = 'sqlite:///' + os.path.join(basedir, 'dbase.db')

    def __init__(self):
        pass
