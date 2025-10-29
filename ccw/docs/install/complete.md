# CCC CODE Komplette Quellcode-Analyse
## Technisches Installationshandbuch für Developer und AI-Agenten

---

## Inhaltsverzeichnis

1. [Übersicht und Architektur](#1-übersicht-und-architektur)
2. [Bash Install-Skript Analyse](#2-bash-install-skript-analyse)
3. [Python Core-Module](#3-python-core-module)
4. [Python CLI-Plugins](#4-python-cli-plugins)
5. [Stack-Management](#5-stack-management)
6. [Site-Management](#6-site-management)
7. [Sicherheit und SSL](#7-sicherheit-und-ssl)
8. [Datenbank und Persistenz](#8-datenbank-und-persistenz)
9. [Service-Management](#9-service-management)
10. [Best Practices und Patterns](#10-best-practices-und-patterns)

---

## 1. Übersicht und Architektur

### 1.1 System-Architektur

```
CCC CODE/
├── install                    # Bash-Installationsskript (Entry Point)
├── ccw/
│   ├── cli/
│   │   ├── main.py           # Cement App Haupteinstieg
│   │   ├── plugins/          # CLI-Funktionalität
│   │   └── templates/        # Mustache-Templates
│   └── core/                 # Kern-Bibliotheken
│       ├── aptget.py         # APT-Paketverwaltung
│       ├── mysql.py          # MySQL/MariaDB-Funktionen
│       ├── services.py       # Systemd-Services
│       ├── sslutils.py       # SSL/TLS-Verwaltung
│       └── variables.py      # Globale Variablen
├── tests/                    # Test-Suite
└── setup.py                  # Python-Paketierung
```

### 1.2 Technologie-Stack

- **Bash**: Installations- und Bootstrap-Prozess
- **Python 3.x**: Hauptanwendung mit Cement Framework
- **SQLAlchemy**: Datenbank-ORM für Site-Metadaten
- **Mustache**: Template-Engine für Konfigurationen
- **Git**: Versionskontrolle für Konfigurationen
- **Systemd**: Service-Management
- **acme.sh**: Let's Encrypt SSL-Zertifikate

---

## 2. Bash Install-Skript Analyse

### 2.1 Skript-Header und Globale Variablen

```bash
#!/usr/bin/env bash
# Version 3.22.0 - 2024-12-06
# wget -qO ccw ccc-code.cc && sudo -E bash ccw

# CLI-Farbkonstanten
CSI='\033['
TPUT_RESET="${CSI}0m"
TPUT_FAIL="${CSI}1;31m"    # Rot für Fehler
TPUT_ECHO="${CSI}1;36m"    # Cyan für Info
TPUT_OK="${CSI}1;32m"      # Grün für Erfolg

# Globale Konfiguration
export DEBIAN_FRONTEND=noninteractive
export LANG='en_US.UTF-8'
export LC_ALL='C.UTF-8'
```

**Analyse**:
- Nutzt ANSI-Escape-Sequenzen für farbige Ausgaben
- Setzt `DEBIAN_FRONTEND=noninteractive` für unbeaufsichtigte Installation
- Erzwingt UTF-8 Locale für konsistente String-Verarbeitung

### 2.2 Argument-Parsing

```bash
while [ "$#" -gt 0 ]; do
    case "$1" in
    -b | --branch)
        ccw_branch="$2"
        shift
        ;;
    --force)
        ccw_force_install="y"
        ;;
    --travis)
        ccw_travis="y"
        ccw_force_install="y"
        ;;
    --mainline | --beta)
        ccw_branch="mainline"
        ;;
    --purge | --uninstall)
        ccw_purge="y"
        ;;
    esac
    shift
done
```

**Patterns erkannt**:
- **Flag-Parsing**: Klassisches `while`/`case` Pattern
- **Shift-Mechanik**: Doppeltes `shift` für Argumente mit Werten
- **CI/CD-Support**: Spezieller Travis-CI-Modus

### 2.3 Sicherheitsprüfungen

```bash
# Root-Rechte prüfen
if [[ $EUID -ne 0 ]]; then
    ccw_lib_echo_fail "Sudo privilege required..."
    exit 100
fi

# Kommando-Existenz prüfen
command_exists() {
    command -v "$@" >/dev/null 2>&1
}
```

**Sicherheitsmechanismen**:
- **EUID-Check**: Verhindert Ausführung ohne Root-Rechte
- **Graceful Degradation**: `command_exists` für optionale Features

### 2.4 Distributions-Erkennung

```bash
ccw_check_distro() {
    local ccw_linux_distro=$(lsb_release -is)
    local ccw_distro_version=$(lsb_release -sc)
    
    if [ -z "$ccw_force_install" ]; then
        if [ "$ccw_linux_distro" != "Ubuntu" ] && 
           [ "$ccw_linux_distro" != "Debian" ] && 
           [ "$ccw_linux_distro" != "Raspbian" ]; then
            ccw_lib_echo_fail "CCC CODE only supports Ubuntu, Debian & Raspbian"
            exit 100
        fi
        
        # Versionsprüfung
        check_ccw_linux_distro=$(lsb_release -sc | 
            grep -E "buster|focal|jammy|bullseye|bookworm|noble")
        if [ -z "$check_ccw_linux_distro" ]; then
            ccw_lib_echo_fail "Unsupported distribution version"
            exit 100
        fi
    fi
}
```

**Unterstützte Systeme**:
- Ubuntu: 20.04 (focal), 22.04 (jammy), 24.04 (noble)
- Debian: 10 (buster), 11 (bullseye), 12 (bookworm)
- Raspbian: 10, 11, 12

### 2.5 Abhängigkeiten-Installation

```bash
ccw_install_dep() {
    local ccw_linux_distro=$(lsb_release -is)
    
    if [ "$ccw_linux_distro" == "Ubuntu" ]; then
        # Ubuntu-spezifisch
        add-apt-repository ppa:git-core/ppa -y
        apt_packages="build-essential curl gzip python3-pip python3-apt 
                     python3-venv gcc python3-dev sqlite3 git tar 
                     software-properties-common pigz gnupg2 cron ccze 
                     rsync apt-transport-https tree haveged ufw 
                     unattended-upgrades tzdata ntp zstd idn 
                     python3-distutils-extra libapt-pkg-dev bash-completion"
    else
        # Debian/Raspbian
        apt_packages="... + dirmngr sudo ca-certificates"
        # PHP Repository GPG-Schlüssel
        curl -sSLo /tmp/debsuryorg-archive-keyring.deb \
            https://packages.sury.org/debsuryorg-archive-keyring.deb
        dpkg -i /tmp/debsuryorg-archive-keyring.deb
    fi
    
    apt-get --option=Dpkg::options::=--force-confmiss \
            --option=Dpkg::options::=--force-confold \
            --assume-yes install $apt_packages
    
    locale-gen en
}
```

**Abhängigkeiten-Kategorien**:
1. **Build-Tools**: gcc, build-essential, python3-dev
2. **Python**: python3-pip, python3-venv, python3-apt
3. **Sicherheit**: gnupg2, ufw, unattended-upgrades
4. **Utilities**: git, curl, rsync, tree, ccze

### 2.6 Python Virtual Environment

```bash
ccw_install() {
    local python_ver=$(python3 -c "import sys; print(sys.version_info[1])")
    
    # Virtual Environment erstellen
    if [ ! -d /opt/ccw/lib/python3."$python_ver"/site-packages/apt ]; then
        python3 -m venv --system-site-packages /opt/ccw
    fi
    
    source /opt/ccw/bin/activate
    
    # setuptools pinning (wichtig!)
    /opt/ccw/bin/pip uninstall -yq setuptools
    /opt/ccw/bin/pip install setuptools==80.0.1
    /opt/ccw/bin/pip install -U pip wheel distro
    
    # Distro-spezifische python-apt Version
    if [ "$ccw_distro_codename" = "focal" ]; then
        /opt/ccw/bin/pip install \
            git+https://salsa.debian.org/apt-team/python-apt.git@2.0.0#egg=python-apt
    elif [ "$ccw_distro_codename" = "jammy" ]; then
        /opt/ccw/bin/pip install \
            git+https://salsa.debian.org/apt-team/python-apt.git@2.2.1#egg=python-apt
    # ... weitere Versionen
    fi
    
    # CCC CODE installieren
    if [ "$ccw_branch" = "master" ]; then
        /opt/ccw/bin/pip install -U ccc-code --upgrade-strategy=eager
    else
        /opt/ccw/bin/pip install -I \
            "git+https://github.com/collective-context/ccc-code.git@$ccw_branch#egg=ccc-code"
    fi
    
    # Symlinks erstellen
    ln -s /opt/ccw/bin/ccw /usr/local/bin/ccw
}
```

**Wichtige Details**:
- **Venv-Isolation**: `--system-site-packages` für APT-Integration
- **Setuptools-Pinning**: Version 80.0.1 für Kompatibilität
- **python-apt**: Distro-spezifische Versionen aus Git
- **Upgrade-Strategie**: `--upgrade-strategy=eager` für Dependencies

### 2.7 Migration von EasyEngine

```bash
ccw_upgrade_ee() {
    # Backup erstellen
    tar -czf "$EE_BACKUP_FILE" /etc/ee /var/lib/ee
    
    # Datenbank migrieren
    ccw_sync_db
    
    # Nginx-Konfiguration migrieren
    rsync -a --exclude="22222" /etc/nginx/ /etc/nginx.bak/
    ccw_upgrade_nginx
}

ccw_sync_db() {
    # SQLite-Schema erstellen
    echo "CREATE TABLE sites (
        id INTEGER PRIMARY KEY,
        sitename UNIQUE,
        site_type TEXT,
        cache_type TEXT,
        site_path TEXT,
        created_on TIMESTAMP,
        is_enabled INT DEFAULT '1',
        is_ssl INT DEFAULT '0',
        storage_fs TEXT,
        storage_db TEXT,
        db_name TEXT,
        db_user TEXT,
        db_password TEXT,
        db_host TEXT,
        is_hhvm INT DEFAULT '0',
        php_version TEXT
    );" | sqlite3 /var/lib/ccw/dbase.db
    
    # EE-Datenbank importieren
    for site in $(mysql -e "SELECT sitename FROM ee.sites_list"); do
        # Migration Logic
    done
}
```

---

## 3. Python Core-Module

### 3.1 ccw/core/variables.py - Globale Konfiguration

```python
class CCWVar:
    """Zentrale Konfigurationsvariablen"""
    
    # System-Erkennung
    ccw_distro = platform.linux_distribution()[0].lower()
    ccw_platform_version = platform.linux_distribution()[1]
    ccw_platform_codename = os.popen("lsb_release -sc").read().strip()
    
    # PHP-Versionen-Management
    ccw_php_versions = {
        'php74': '7.4',
        'php80': '8.0',
        'php81': '8.1',
        'php82': '8.2',
        'php83': '8.3',
        'php84': '8.4',
    }
    
    # APT-Pakete pro Stack
    ccw_nginx = ["nginx-custom", "nginx-ccw"]
    
    ccw_php74 = [
        "php7.4-fpm", "php7.4-curl", "php7.4-gd", "php7.4-imap",
        "php7.4-readline", "php7.4-common", "php7.4-redis",
        "php7.4-mysql", "php7.4-cli", "php7.4-mbstring",
        "php7.4-bcmath", "php7.4-mysql", "php7.4-opcache",
        "php7.4-zip", "php7.4-xml", "php7.4-soap", "php7.4-msgpack",
        "php7.4-igbinary", "php7.4-intl"
    ]
    
    # MariaDB-Version basierend auf Distro
    if ccw_distro == 'raspbian':
        mariadb_ver = '10.3'
    else:
        mariadb_ver = '11.4'
        
    ccw_mysql = [
        "mariadb-server", "percona-toolkit",
        "mariadb-common", "python3-mysqldb",
        "mariadb-backup"  # nur für MariaDB 10.1+
    ]
    
    # SSL-Pfade
    ccw_ssl_live = "/etc/letsencrypt/live"
    ccw_ssl_archive = "/etc/letsencrypt/renewal"
    ccw_ssl_cert = "/cert.pem"
    ccw_ssl_key = "/privkey.pem"
    
    # Repository URLs
    ccw_mysql_repo = (
        "deb [signed-by=/etc/apt/keyrings/mariadb-keyring.pgp] "
        f"http://deb.mariadb.org/{mariadb_ver}/{ccw_distro} "
        f"{ccw_platform_codename} main"
    )
    
    @staticmethod
    def generate_php_modules(version):
        """Dynamische PHP-Modul-Liste Generation"""
        base_modules = [
            'fpm', 'curl', 'gd', 'imap', 'readline', 'common',
            'redis', 'mysql', 'cli', 'mbstring', 'bcmath',
            'opcache', 'zip', 'xml', 'soap'
        ]
        
        additional = []
        if version >= '7.0':
            additional.extend(['msgpack', 'igbinary'])
        if version >= '7.1':
            additional.append('intl')
        if version >= '8.0':
            additional.append('apcu')
            
        return [f"php{version}-{mod}" for mod in base_modules + additional]
```

### 3.2 ccw/core/aptget.py - Paketverwaltung

```python
import subprocess
from ccw.core.logging import Log
from ccw.core.shellexec import CCWShellExec

class CCWAptGet:
    """APT-Paketmanagement Wrapper"""
    
    @staticmethod
    def update(self):
        """APT-Cache aktualisieren"""
        try:
            CCWShellExec.cmd_exec(
                self,
                "DEBIAN_FRONTEND=noninteractive apt-get update -qq"
            )
        except CommandExecutionError as e:
            Log.debug(self, str(e))
            Log.error(self, "apt-get update failed")
            
    @staticmethod
    def install(self, packages):
        """Pakete installieren mit Fehlerbehandlung"""
        apt_cmd = (
            "DEBIAN_FRONTEND=noninteractive "
            "apt-get install -qq "
            "--option=Dpkg::options::=--force-confmiss "
            "--option=Dpkg::options::=--force-confold "
            "--assume-yes {0}"
        )
        
        try:
            for package in packages:
                if not CCWAptGet.is_installed(self, package):
                    Log.wait(self, f"Installing {package}")
                    CCWShellExec.cmd_exec(
                        self, 
                        apt_cmd.format(package)
                    )
                    Log.valide(self, f"Installing {package}")
        except CommandExecutionError as e:
            Log.debug(self, str(e))
            Log.error(self, f"Package installation failed")
            
    @staticmethod
    def is_installed(self, package):
        """Prüft ob Paket installiert ist"""
        try:
            proc = subprocess.Popen(
                ["dpkg", "-l", package],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, stderr = proc.communicate()
            
            if proc.returncode == 0:
                return "ii" in stdout.decode('utf-8')
            return False
        except Exception as e:
            Log.debug(self, str(e))
            return False
            
    @staticmethod
    def is_exec(self, command):
        """Prüft ob Befehl ausführbar ist"""
        return shutil.which(command) is not None
```

### 3.3 ccw/core/mysql.py - Datenbank-Management

```python
import pymysql
import configparser
import subprocess
from ccw.core.logging import Log
from ccw.core.shellexec import CCWShellExec
from ccw.core.variables import CCWVar

class CCWMysql:
    """MySQL/MariaDB Verwaltung"""
    
    @staticmethod
    def dbConnection(self, db_name=None, db_user='root', 
                    db_host='localhost', db_password=None):
        """Erstellt Datenbankverbindung"""
        try:
            # Credentials aus my.cnf lesen wenn nicht angegeben
            if not db_password:
                config = configparser.ConfigParser()
                config.read('/etc/mysql/conf.d/my.cnf')
                db_password = config['client']['password']
            
            connection = pymysql.connect(
                host=db_host,
                port=3306,
                user=db_user,
                passwd=db_password,
                db=db_name,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            return connection
            
        except pymysql.err.InternalError as e:
            Log.debug(self, str(e))
            if e.args[0] == 1049:
                raise DatabaseNotExistsError
            else:
                raise MySQLConnectionError
                
    @staticmethod
    def execute(self, statement, errormsg='', log=True):
        """SQL-Statement ausführen"""
        connection = CCWMysql.dbConnection(self)
        
        try:
            with connection.cursor() as cursor:
                if log:
                    Log.debug(self, f"Executing MySQL: {statement}")
                cursor.execute(statement)
                
            # Wichtig: Commit für DDL/DML
            connection.commit()
            
        except Exception as e:
            Log.debug(self, str(e))
            if errormsg:
                Log.error(self, errormsg)
            raise StatementExecutionError
        finally:
            connection.close()
            
    @staticmethod
    def backupAll(self, fulldump=False):
        """Backup aller Datenbanken"""
        import subprocess
        
        Log.info(self, "Backing up databases to /var/lib/ccw-backup/mysql")
        
        if not os.path.exists('/var/lib/ccw-backup/mysql'):
            os.makedirs('/var/lib/ccw-backup/mysql')
            
        if not fulldump:
            # Einzelne Datenbanken
            databases = subprocess.check_output(
                ["mysql", "-Bse", "show databases"],
                universal_newlines=True
            ).split('\n')
            
            for db in databases:
                if db:
                    Log.info(self, f"Backing up {db}")
                    p1 = subprocess.Popen(
                        f"mysqldump {db} --max_allowed_packet=1024M "
                        "--single-transaction --hex-blob",
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        shell=True
                    )
                    p2 = subprocess.Popen(
                        f"zstd -c > /var/lib/ccw-backup/mysql/{db}{CCWVar.ccw_date}.sql.zst",
                        stdin=p1.stdout,
                        shell=True
                    )
                    p1.stdout.close()
                    p1.wait()
        else:
            # Full Dump
            Log.info(self, "Creating full database dump")
            p1 = subprocess.Popen(
                "mysqldump --all-databases --max_allowed_packet=1024M "
                "--hex-blob --single-transaction --events",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True
            )
            p2 = subprocess.Popen(
                f"zstd -c > /var/lib/ccw-backup/mysql/fulldump-{CCWVar.ccw_date}.sql.zst",
                stdin=p1.stdout,
                shell=True
            )
    
    @staticmethod
    def mariadb_ping(self):
        """Prüft MariaDB-Verfügbarkeit"""
        mariadb_admin = "/usr/bin/mariadb-admin" if os.path.exists("/usr/bin/mariadb-admin") \
                       else "/usr/bin/mysqladmin"
                       
        return CCWShellExec.cmd_exec(self, f"{mariadb_admin} ping")
```

### 3.4 ccw/core/services.py - Systemd Service Management

```python
import subprocess
from ccw.core.logging import Log
from ccw.core.git import CCWGit

class CCWService:
    """Systemd Service Management mit Rollback"""
    
    @staticmethod
    def start_service(self, service):
        """Service starten"""
        try:
            Log.wait(self, f"Starting {service}")
            retcode = subprocess.call(
                ["systemctl", "start", service],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            if retcode == 0:
                Log.valide(self, f"Starting {service}")
                return True
            else:
                Log.failed(self, f"Starting {service}")
                return False
                
        except Exception as e:
            Log.debug(self, str(e))
            return False
            
    @staticmethod
    def restart_service(self, service, config_paths=None):
        """Service mit Config-Rollback neustarten"""
        try:
            # Config-Check für Nginx
            if service in ['nginx', 'nginx-ccw', 'nginx-custom']:
                if not CCWService.nginx_test(self):
                    if config_paths:
                        Log.info(self, "Nginx config test failed, rolling back")
                        CCWGit.rollback(self, config_paths)
                    return False
                    
            Log.wait(self, f"Restarting {service}")
            retcode = subprocess.call(
                ["systemctl", "restart", service],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            if retcode == 0:
                Log.valide(self, f"Restarting {service}")
                return True
            else:
                Log.failed(self, f"Restarting {service}")
                # Rollback bei Fehler
                if config_paths:
                    CCWGit.rollback(self, config_paths)
                return False
                
        except Exception as e:
            Log.debug(self, str(e))
            return False
            
    @staticmethod
    def reload_service(self, service):
        """Service reload (graceful restart)"""
        try:
            # Spezialbehandlung für Nginx
            if service in ['nginx', 'nginx-ccw', 'nginx-custom']:
                if not CCWService.nginx_test(self):
                    return False
                    
            Log.wait(self, f"Reloading {service}")
            retcode = subprocess.call(
                ["systemctl", "reload", service],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            if retcode == 0:
                Log.valide(self, f"Reloading {service}")
                return True
            else:
                Log.failed(self, f"Reloading {service}")
                return False
                
        except Exception as e:
            Log.debug(self, str(e))
            return False
            
    @staticmethod
    def nginx_test(self):
        """Nginx Konfiguration testen"""
        try:
            retcode = subprocess.call(
                ["nginx", "-t"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            return retcode == 0
        except Exception:
            return False
            
    @staticmethod
    def get_service_status(self, service):
        """Service Status abfragen"""
        try:
            proc = subprocess.Popen(
                ["systemctl", "is-active", service],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, stderr = proc.communicate()
            
            return stdout.decode('utf-8').strip() == "active"
            
        except Exception as e:
            Log.debug(self, str(e))
            return False
```

---

## 4. Python CLI-Plugins

### 4.1 ccw/cli/main.py - Cement Application

```python
from cement.core.foundation import CementApp
from cement.core.controller import CementBaseController, expose
from cement.ext.ext_colorlog import ColorLogHandler
from ccw.core.logging import Log
from ccw.core.variables import CCWVar

# Konfiguration Defaults
config_defaults = {
    'ccw': {
        'debug': False,
        'plugin_dir': '/var/lib/ccw/plugins/',
        'plugin_config_dir': '/etc/ccw/plugins.d/',
        'template_dir': '/var/lib/ccw/templates/'
    },
    'log.colorlog': {
        'file': '/var/log/ccw/ccc-code.log',
        'level': 'debug',
        'to_console': False,
        'rotate': True,
        'max_bytes': 1000000,
        'max_files': 7,
        'colorize_file_log': True,
        'colorize_console_log': True
    }
}

class CCWBaseController(CementBaseController):
    class Meta:
        label = 'base'
        description = 'CCC CODE - WordPress Operations Tool'
        
    @expose(hide=True)
    def default(self):
        """Default action wenn kein Subcommand angegeben"""
        self.app.args.print_help()

class CCWApp(CementApp):
    class Meta:
        label = 'ccw'
        base_controller = 'base'
        config_defaults = config_defaults
        log_handler = ColorLogHandler
        extensions = [
            'colorlog',
            'mustache',
        ]
        hooks = [
            ('post_setup', ccw_post_setup_hook),
            ('pre_close', ccw_pre_close_hook),
        ]
        handlers = [
            CCWBaseController,
            CCWStackController,
            CCWSiteController,
            CCWDebugController,
            # ... weitere Controller
        ]
        exit_on_close = True
        
def ccw_post_setup_hook(app):
    """Nach App-Setup ausführen"""
    # Git-Config prüfen
    if not os.path.exists(f"{os.environ['HOME']}/.gitconfig"):
        import getpass
        username = getpass.getuser()
        CCWShellExec.cmd_exec(
            app,
            f'git config --global user.name "{username}"'
        )
        CCWShellExec.cmd_exec(
            app,
            f'git config --global user.email "root@{os.uname()[1]}"'
        )
        
def ccw_pre_close_hook(app):
    """Vor App-Beendigung ausführen"""
    # Cleanup Tasks
    pass

def main():
    with CCWApp() as app:
        app.run()

if __name__ == '__main__':
    main()
```

### 4.2 ccw/cli/plugins/stack.py - Stack Management

```python
from cement.core.controller import CementBaseController, expose
from ccw.cli.plugins.stack_pref import pre_pref, post_pref
from ccw.core.aptget import CCWAptGet
from ccw.core.logging import Log
from ccw.core.variables import CCWVar

class CCWStackController(CementBaseController):
    class Meta:
        label = 'stack'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = 'Stack Management'
        arguments = [
            # Stack-Argumente
            (['--all'], dict(help='Alle Stacks', action='store_true')),
            (['--nginx'], dict(help='Nginx Stack', action='store_true')),
            (['--mysql'], dict(help='MySQL Stack', action='store_true')),
            (['--redis'], dict(help='Redis Stack', action='store_true')),
            # PHP-Versionen dynamisch
        ] + [
            ([f'--{php_version}'], 
             dict(help=f'PHP {php_number} Stack', action='store_true'))
            for php_version, php_number in CCWVar.ccw_php_versions.items()
        ]
        
    @expose(help="Stack installieren")
    def install(self, packages=[], apt_packages=[]):
        """Stack-Installation mit Transaktions-Pattern"""
        pargs = self.app.pargs
        
        try:
            # Stack-Auswahl verarbeiten
            if pargs.all:
                pargs.nginx = True
                pargs.mysql = True
                pargs.php83 = True  # Default PHP
                pargs.redis = True
                
            # Nginx Stack
            if pargs.nginx:
                if not CCWAptGet.is_exec(self, 'nginx'):
                    apt_packages.extend(CCWVar.ccw_nginx)
                else:
                    Log.info(self, "Nginx bereits installiert")
                    
            # MySQL Stack
            if pargs.mysql:
                if not CCWMysql.mariadb_ping(self):
                    apt_packages.extend(CCWVar.ccw_mysql)
                    
            # PHP Stacks
            for php_version, php_number in CCWVar.ccw_php_versions.items():
                if getattr(pargs, php_version, False):
                    if not CCWAptGet.is_installed(self, f'php{php_number}-fpm'):
                        apt_packages.extend(
                            CCWVar.generate_php_modules(php_number)
                        )
                        
            # Pre-Installation Tasks
            if apt_packages:
                pre_pref(self, apt_packages)
                
            # Installation
            if apt_packages:
                Log.wait(self, "Installing packages")
                CCWAptGet.install(self, apt_packages)
                Log.valide(self, "Installing packages")
                
            # Post-Installation Tasks
            if apt_packages:
                post_pref(self, apt_packages, packages)
                
        except Exception as e:
            Log.error(self, f"Stack installation failed: {e}")
            
    @expose(help="Stack upgraden")
    def upgrade(self):
        """Stack-Upgrade mit Backup"""
        pargs = self.app.pargs
        
        # Backup vor Upgrade
        if pargs.mysql and CCWMysql.mariadb_ping(self):
            CCWMysql.backupAll(self, fulldump=True)
            
        # Upgrade-Logik
        # ...
        
    @expose(help="Stack entfernen")
    def remove(self):
        """Stack-Entfernung mit Bestätigung"""
        pargs = self.app.pargs
        
        if not pargs.force:
            confirm = input("Wirklich entfernen? [y/N]: ")
            if confirm.lower() != 'y':
                Log.error(self, "Abgebrochen")
                
        # Removal-Logik
        # ...
```

### 4.3 ccw/cli/plugins/stack_pref.py - Stack Konfiguration

```python
import configparser
import random
import string
import psutil
from ccw.core.template import CCWTemplate
from ccw.core.git import CCWGit

def pre_pref(self, apt_packages):
    """Vor-Installation Konfiguration"""
    
    # MariaDB Repository Setup
    if "mariadb-server" in apt_packages:
        if not CCWVar.ccw_distro == 'raspbian':
            Log.info(self, "MariaDB Repository hinzufügen")
            
            # APT Pinning für MariaDB
            mysql_pref = (
                "Package: *\n"
                "Pin: origin deb.mariadb.org\n"
                "Pin-Priority: 1000\n"
            )
            with open('/etc/apt/preferences.d/MariaDB.pref', 'w') as f:
                f.write(mysql_pref)
                
            # Repository hinzufügen
            CCWRepo.add(self, 
                      repo_url=CCWVar.ccw_mysql_repo,
                      repo_name="mariadb")
                      
    # MySQL Root-Passwort generieren
    if "mariadb-server" in apt_packages:
        if not os.path.exists('/etc/mysql/conf.d/my.cnf'):
            # 24 Zeichen zufälliges Passwort
            chars = ''.join(random.sample(string.ascii_letters, 24))
            
            mysql_config = f"""
            [client]
            user = root
            password = {chars}
            socket = /run/mysqld/mysqld.sock
            """
            
            with open('/etc/mysql/conf.d/my.cnf.tmp', 'w') as f:
                f.write(mysql_config)
                
            CCWFileUtils.chmod(self, '/etc/mysql/conf.d/my.cnf.tmp', 0o600)

def post_pref(self, apt_packages, packages):
    """Nach-Installation Konfiguration"""
    
    # PHP-FPM Konfiguration
    for php_version in CCWVar.ccw_php_versions.values():
        if f"php{php_version}-fpm" in apt_packages:
            Log.wait(self, f"Konfiguriere PHP {php_version}")
            
            # PHP-FPM Pool Template
            data = {
                'php_version': php_version,
                'max_children': calculate_workers(self),
                'start_servers': 4,
                'min_spare_servers': 2,
                'max_spare_servers': 6,
                'request_terminate_timeout': 300,
                'pm_max_requests': 500
            }
            
            # www.conf deployen
            CCWTemplate.deploy(
                self,
                f'/etc/php/{php_version}/fpm/pool.d/www.conf',
                'php-fpm-pool.mustache',
                data
            )
            
            # php.ini Optimierungen
            php_ini_changes = {
                'max_execution_time': 300,
                'max_input_time': 300,
                'max_input_vars': 10000,
                'memory_limit': '256M',
                'post_max_size': '100M',
                'upload_max_filesize': '100M',
                'opcache.enable': 1,
                'opcache.interned_strings_buffer': 8,
                'opcache.max_accelerated_files': 10000,
                'opcache.memory_consumption': 128,
                'opcache.save_comments': 1,
                'opcache.revalidate_freq': 2,
            }
            
            for key, value in php_ini_changes.items():
                CCWFileUtils.searchreplace(
                    self,
                    f'/etc/php/{php_version}/fpm/php.ini',
                    f';{key} =.*',
                    f'{key} = {value}'
                )
                
            # Service neustarten mit Rollback
            if not CCWService.restart_service(self, f'php{php_version}-fpm',
                                            [f'/etc/php/{php_version}']):
                CCWGit.rollback(self, [f'/etc/php/{php_version}'])
                Log.error(self, f"PHP {php_version} Start fehlgeschlagen")
            else:
                CCWGit.add(self, [f'/etc/php/{php_version}'],
                         msg=f"PHP {php_version} Konfiguration")
                Log.valide(self, f"Konfiguriere PHP {php_version}")
                
    # MariaDB Tuning
    if "mariadb-server" in apt_packages:
        Log.wait(self, "MariaDB Tuning")
        
        # RAM-basierte Konfiguration
        ccw_ram = psutil.virtual_memory().total / (1024 * 1024)
        ccw_ram_innodb = int(ccw_ram * 0.3)  # 30% für InnoDB
        ccw_ram_log_buffer = int(ccw_ram_innodb * 0.25)
        
        mariadb_config = {
            'innodb_buffer_pool_size': f'{ccw_ram_innodb}M',
            'innodb_log_buffer_size': f'{ccw_ram_log_buffer}M',
            'innodb_buffer_pool_instances': 1 if ccw_ram < 2000 else 2,
            'max_connections': 100 if ccw_ram < 2000 else 200,
            'key_buffer_size': '32M' if ccw_ram < 2000 else '128M',
            'tmp_table_size': '32M' if ccw_ram < 2000 else '64M',
            'max_heap_table_size': '32M' if ccw_ram < 2000 else '64M',
            'query_cache_size': '8M' if ccw_ram < 2000 else '16M',
            'query_cache_limit': '1M',
            'query_cache_type': 1,
            'performance_schema': 0 if ccw_ram < 2000 else 1,
        }
        
        # my.cnf Template deployen
        CCWTemplate.deploy(
            self,
            '/etc/mysql/mariadb.conf.d/50-server.cnf',
            'mariadb-server.mustache',
            mariadb_config
        )
        
        # Root-Passwort setzen
        if os.path.exists('/etc/mysql/conf.d/my.cnf.tmp'):
            config = configparser.ConfigParser()
            config.read('/etc/mysql/conf.d/my.cnf.tmp')
            root_pass = config['client']['password']
            
            CCWShellExec.cmd_exec(
                self,
                f'mysql -e "SET PASSWORD = PASSWORD(\'{root_pass}\'); '
                'FLUSH PRIVILEGES;"',
                log=False
            )
            
            CCWFileUtils.mvfile(
                self,
                '/etc/mysql/conf.d/my.cnf.tmp',
                '/etc/mysql/conf.d/my.cnf'
            )
            
        CCWService.restart_service(self, 'mariadb')
        Log.valide(self, "MariaDB Tuning")
        
def calculate_workers(self):
    """PHP-FPM Worker berechnen"""
    # Verfügbarer RAM in MB
    ram = psutil.virtual_memory().total / (1024 * 1024)
    # CPU Cores
    cores = psutil.cpu_count()
    
    # Pro Worker ~50MB RAM
    max_by_ram = int(ram / 50)
    # 4 Worker pro Core
    max_by_cpu = cores * 4
    
    # Kleinerer Wert
    return min(max_by_ram, max_by_cpu, 50)  # Max 50 Worker
```

---

## 5. Stack-Management

### 5.1 Stack-Komponenten Übersicht

```python
# Stack-Definitionen in ccw/core/variables.py
STACKS = {
    'nginx': {
        'packages': ['nginx-custom', 'nginx-ccw'],
        'services': ['nginx'],
        'config_paths': ['/etc/nginx'],
        'log_paths': ['/var/log/nginx'],
    },
    'php74': {
        'packages': CCWVar.ccw_php74,
        'services': ['php7.4-fpm'],
        'config_paths': ['/etc/php/7.4'],
        'log_paths': ['/var/log/php7.4-fpm.log'],
    },
    'mysql': {
        'packages': CCWVar.ccw_mysql,
        'services': ['mariadb', 'mysql'],
        'config_paths': ['/etc/mysql'],
        'log_paths': ['/var/log/mysql'],
    },
    'redis': {
        'packages': ['redis-server', 'redis-tools'],
        'services': ['redis-server'],
        'config_paths': ['/etc/redis'],
        'log_paths': ['/var/log/redis'],
    },
    'fail2ban': {
        'packages': ['fail2ban'],
        'services': ['fail2ban'],
        'config_paths': ['/etc/fail2ban'],
        'log_paths': ['/var/log/fail2ban.log'],
    },
}
```

### 5.2 Stack Migration Controller

```python
# ccw/cli/plugins/stack_migrate.py
class CCWStackMigrateController(CementBaseController):
    class Meta:
        label = 'migrate'
        stacked_on = 'stack'
        stacked_type = 'nested'
        
    @expose(help="MariaDB Migration")
    def migrate_mariadb(self):
        """MariaDB Version Migration"""
        
        # Backup aller Datenbanken
        CCWMysql.backupAll(self, fulldump=True)
        
        # Aktuelle Version prüfen
        current_version = CCWShellExec.cmd_exec_stdout(
            self,
            "mysql --version | awk '{print $5}' | cut -d'-' -f1"
        )
        
        # Repository updaten
        if self.app.config.has_section('mariadb'):
            new_version = self.app.config.get('mariadb', 'release')
        else:
            new_version = CCWVar.mariadb_ver
            
        if current_version != new_version:
            Log.info(self, f"Migration von {current_version} zu {new_version}")
            
            # Service stoppen
            CCWService.stop_service(self, 'mariadb')
            
            # Repository ändern
            CCWRepo.remove(self, repo_name="mariadb")
            CCWRepo.add(self, 
                      repo_url=CCWVar.ccw_mysql_repo.replace(
                          current_version, new_version
                      ),
                      repo_name="mariadb")
            
            # Upgrade
            CCWAptGet.update(self)
            CCWAptGet.install(self, ['mariadb-server'])
            
            # mysql_upgrade ausführen
            CCWShellExec.cmd_exec(self, "mysql_upgrade")
            
            # Service starten
            CCWService.start_service(self, 'mariadb')
            
    @expose(help="Nginx HTTP/3 Migration")  
    def migrate_nginx(self):
        """Nginx zu HTTP/3 QUIC Migration"""
        
        # Nginx Config Backup
        CCWFileUtils.copyfile(
            self, 
            '/etc/nginx/nginx.conf',
            f'/etc/nginx/nginx.conf.{CCWVar.ccw_date}'
        )
        
        # HTTP/3 Konfiguration
        http3_config = """
        # HTTP/3 QUIC Support
        ssl_early_data on;
        quic_retry on;
        
        # Alt-Svc Header für HTTP/3
        add_header Alt-Svc 'h3=":443"; ma=86400';
        """
        
        # Sites updaten
        sites = getAllsites(self)
        for site in sites:
            ssl_conf = f'/var/www/{site.sitename}/conf/nginx/ssl.conf'
            if os.path.exists(ssl_conf):
                # Listen-Direktive für QUIC
                CCWFileUtils.searchreplace(
                    self,
                    ssl_conf,
                    'listen 443 ssl http2;',
                    'listen 443 ssl http2;\n    listen 443 quic;'
                )
                
        # Nginx neustarten
        if not CCWService.reload_service(self, 'nginx'):
            # Rollback bei Fehler
            CCWFileUtils.mvfile(
                self,
                f'/etc/nginx/nginx.conf.{CCWVar.ccw_date}',
                '/etc/nginx/nginx.conf'
            )
            Log.error(self, "HTTP/3 Migration fehlgeschlagen")
```

---

## 6. Site-Management

### 6.1 Site Create Controller

```python
# ccw/cli/plugins/site_create.py
class CCWSiteCreateController(CementBaseController):
    class Meta:
        label = 'create'
        stacked_on = 'site'
        stacked_type = 'nested'
        arguments = [
            (['site_name'], dict(help='Domain Name')),
            (['--wp'], dict(help='WordPress', action='store_true')),
            (['--wpsc'], dict(help='WP Super Cache', action='store_true')),
            (['--wpfc'], dict(help='WP FastCGI Cache', action='store_true')),
            (['--wpredis'], dict(help='WP Redis Cache', action='store_true')),
            (['--php74'], dict(help='PHP 7.4', action='store_true')),
            # ... weitere PHP Versionen
            (['--letsencrypt'], dict(help='Let\'s Encrypt SSL')),
        ]
        
    @expose(hide=True)
    def default(self):
        """Site erstellen"""
        pargs = self.app.pargs
        
        # Domain validieren
        domain = CCWDomain.validate(self, pargs.site_name)
        
        # Prüfen ob Site existiert
        if check_domain_exists(self, domain):
            Log.error(self, f"Site {domain} existiert bereits")
            
        # Site-Typ bestimmen
        site_type = determine_site_type(pargs)
        cache_type = determine_cache_type(pargs)
        php_version = determine_php_version(pargs)
        
        try:
            # Pre-Run Checks
            pre_run_checks(self)
            
            # Domain Setup
            setupdomain(self, domain, site_type, cache_type, php_version)
            
            # WordPress Installation
            if site_type in ['wp', 'wpsubdir', 'wpsubdomain']:
                # Datenbank erstellen
                db_name, db_user, db_pass = setupdatabase(self, domain)
                
                # WordPress installieren
                setupwordpress(
                    self, domain, 
                    db_name, db_user, db_pass,
                    cache_type
                )
                
            # Berechtigungen setzen
            setwebrootpermissions(self, domain)
            
            # SSL Setup
            if pargs.letsencrypt:
                setupssl(self, domain, pargs.letsencrypt)
                
            # Site in Datenbank speichern
            addNewSite(
                self,
                domain=domain,
                site_type=site_type,
                cache_type=cache_type,
                php_version=php_version
            )
            
            # Cache-Info anzeigen
            display_cache_settings(self, domain, cache_type)
            
        except SiteError as e:
            # Cleanup bei Fehler
            Log.error(self, str(e))
            doCleanupAction(self, domain)
```

### 6.2 Site Functions

```python
# ccw/cli/plugins/site_functions.py

def setupdomain(self, domain, site_type, cache_type, php_version):
    """Nginx vHost Setup"""
    
    # Webroot erstellen
    webroot = f"/var/www/{domain}"
    CCWFileUtils.mkdir(self, f"{webroot}/htdocs")
    CCWFileUtils.mkdir(self, f"{webroot}/conf/nginx")
    CCWFileUtils.mkdir(self, f"{webroot}/logs")
    
    # Nginx Template-Daten
    data = {
        'domain': domain,
        'webroot': webroot,
        'php_version': php_version.replace('.', ''),
        'include_php': site_type in ['php', 'wp', 'wpsubdir', 'wpsubdomain'],
        'include_redis': cache_type == 'wpredis',
        'include_wpfc': cache_type == 'wpfc',
        'include_wpsc': cache_type == 'wpsc',
        'include_wpcommon': site_type.startswith('wp'),
    }
    
    # Haupt-Nginx-Config
    CCWTemplate.deploy(
        self,
        f'/etc/nginx/sites-available/{domain}',
        'nginx-site.mustache',
        data
    )
    
    # Site aktivieren
    CCWFileUtils.create_symlink(
        self,
        f'/etc/nginx/sites-available/{domain}',
        f'/etc/nginx/sites-enabled/{domain}'
    )
    
    # PHP-Config wenn benötigt
    if data['include_php']:
        CCWTemplate.deploy(
            self,
            f'{webroot}/conf/nginx/php.conf',
            'nginx-php.mustache',
            data
        )
        
def setupdatabase(self, domain):
    """MySQL Datenbank erstellen"""
    
    # Sichere Namen generieren
    db_name = domain.replace('.', '_')[:12] + \
              ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
    db_user = domain.replace('.', '_')[:12] + \
              ''.join(random.choices(string.ascii_lowercase, k=4))
    db_pass = ''.join(
        random.choices(string.ascii_letters + string.digits + '!@#$%', k=24)
    )
    
    # Datenbank erstellen
    try:
        CCWMysql.execute(
            self,
            f"CREATE DATABASE IF NOT EXISTS `{db_name}` "
            "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        )
        
        # Benutzer erstellen
        if self.app.config.has_section('mysql'):
            grant_host = self.app.config.get('mysql', 'grant-host')
        else:
            grant_host = 'localhost'
            
        CCWMysql.execute(
            self,
            f"CREATE USER '{db_user}'@'{grant_host}' "
            f"IDENTIFIED BY '{db_pass}'"
        )
        
        # Rechte vergeben
        CCWMysql.execute(
            self,
            f"GRANT ALL PRIVILEGES ON `{db_name}`.* "
            f"TO '{db_user}'@'{grant_host}'"
        )
        
        CCWMysql.execute(self, "FLUSH PRIVILEGES")
        
    except Exception as e:
        Log.error(self, f"Datenbank-Setup fehlgeschlagen: {e}")
        raise SiteError("Database creation failed")
        
    return db_name, db_user, db_pass
    
def setupwordpress(self, domain, db_name, db_user, db_pass, cache_type):
    """WordPress Installation mit WP-CLI"""
    
    webroot = f"/var/www/{domain}/htdocs"
    
    # WP-CLI Befehle
    wp_cli = "/usr/local/bin/wp --allow-root"
    
    # WordPress Download
    CCWShellExec.cmd_exec(
        self,
        f"{wp_cli} core download --path={webroot}"
    )
    
    # wp-config.php erstellen
    CCWShellExec.cmd_exec(
        self,
        f"{wp_cli} config create "
        f"--dbname='{db_name}' "
        f"--dbuser='{db_user}' "
        f"--dbpass='{db_pass}' "
        f"--dbhost='localhost' "
        f"--path={webroot}"
    )
    
    # Salts hinzufügen
    CCWShellExec.cmd_exec(
        self,
        f"{wp_cli} config shuffle-salts --path={webroot}"
    )
    
    # WordPress installieren
    if self.app.config.has_section('wordpress'):
        wp_user = self.app.config.get('wordpress', 'user')
        wp_pass = self.app.config.get('wordpress', 'password')
        wp_email = self.app.config.get('wordpress', 'email')
    else:
        wp_user = 'admin'
        wp_pass = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        wp_email = f"admin@{domain}"
        
    CCWShellExec.cmd_exec(
        self,
        f"{wp_cli} core install "
        f"--url='https://{domain}' "
        f"--title='{domain}' "
        f"--admin_user='{wp_user}' "
        f"--admin_password='{wp_pass}' "
        f"--admin_email='{wp_email}' "
        f"--path={webroot}"
    )
    
    # Cache-Plugin installieren
    if cache_type == 'wpredis':
        install_redis_cache(self, domain, webroot)
    elif cache_type == 'wpfc':
        configure_fastcgi_cache(self, domain)
    elif cache_type == 'wpsc':
        install_wp_super_cache(self, domain, webroot)
        
    # Ausgabe der Zugangsdaten
    Log.info(self, f"WordPress Admin: https://{domain}/wp-admin")
    Log.info(self, f"Username: {wp_user}")
    Log.info(self, f"Password: {wp_pass}")
```

---

## 7. Sicherheit und SSL

### 7.1 SSL/Acme Management

```python
# ccw/core/acme.py
class CCWAcme:
    """Let's Encrypt Integration mit acme.sh"""
    
    ccw_acme_exec = (
        "/etc/letsencrypt/acme.sh "
        "--config-home '/etc/letsencrypt/config'"
    )
    
    @staticmethod
    def check_acme(self):
        """acme.sh Installation prüfen"""
        if not os.path.exists('/etc/letsencrypt/acme.sh'):
            # acme.sh installieren
            CCWGit.clone(
                self,
                'https://github.com/Neilpang/acme.sh.git',
                '/opt/acme.sh'
            )
            
            CCWFileUtils.mkdir(self, '/etc/letsencrypt/config')
            CCWFileUtils.mkdir(self, '/etc/letsencrypt/renewal')
            CCWFileUtils.mkdir(self, '/etc/letsencrypt/live')
            
            CCWShellExec.cmd_exec(
                self,
                'cd /opt/acme.sh && '
                './acme.sh --install '
                '--home /etc/letsencrypt '
                '--config-home /etc/letsencrypt/config '
                '--cert-home /etc/letsencrypt/renewal'
            )
            
    @staticmethod
    def check_dns(self, domains):
        """DNS-Einträge prüfen"""
        server_ip = CCWFqdn.get_server_ip(self)
        
        for domain in domains:
            domain_ip = CCWFqdn.get_domain_ip(self, domain)
            
            if domain_ip != server_ip:
                Log.warn(
                    self,
                    f"{domain} zeigt auf {domain_ip}, "
                    f"Server-IP ist {server_ip}"
                )
                return False
        return True
        
    @staticmethod
    def setupletsencrypt(self, domains, data):
        """SSL-Zertifikat ausstellen"""
        
        CCWAcme.check_acme(self)
        
        # Acme-Befehl zusammenbauen
        acme_cmd = f"{CCWAcme.ccw_acme_exec} --issue "
        
        # Domains hinzufügen
        for domain in domains:
            acme_cmd += f"-d {domain} "
            
        # Validierungsmethode
        if data.get('dns'):
            # DNS-API Validierung
            dns_provider = data.get('dns_provider', 'dns_cf')
            acme_cmd += f"--dns {dns_provider} "
            
            # API-Credentials setzen
            if dns_provider == 'dns_cf':
                os.environ['CF_Key'] = data.get('cf_key', '')
                os.environ['CF_Email'] = data.get('cf_email', '')
        else:
            # Webroot-Validierung
            acme_cmd += f"-w /var/www/{domains[0]}/htdocs "
            
        # Keylength
        keylength = self.app.config.get('letsencrypt', 'keylength')
        if keylength == 'ec-384':
            acme_cmd += "--keylength ec-384 "
        else:
            acme_cmd += "--keylength 2048 "
            
        # Zertifikat ausstellen
        try:
            CCWShellExec.cmd_exec(self, acme_cmd)
            return True
        except CommandExecutionError as e:
            Log.error(self, f"SSL-Zertifikat konnte nicht ausgestellt werden: {e}")
            return False
            
    @staticmethod
    def deploycert(self, domain):
        """Zertifikat deployen"""
        
        cert_path = f"/etc/letsencrypt/renewal/{domain}_ecc"
        live_path = f"/etc/letsencrypt/live/{domain}"
        
        # Symlinks erstellen
        if not os.path.exists(live_path):
            os.makedirs(live_path)
            
        links = {
            'fullchain.pem': f"{cert_path}/fullchain.cer",
            'privkey.pem': f"{cert_path}/{domain}.key",
            'cert.pem': f"{cert_path}/{domain}.cer",
            'chain.pem': f"{cert_path}/ca.cer"
        }
        
        for target, source in links.items():
            if os.path.exists(source):
                CCWFileUtils.create_symlink(
                    self,
                    source,
                    f"{live_path}/{target}"
                )
                
        # SSL-Config deployen
        data = {
            'domain': domain,
            'ssl_live_path': live_path,
            'quic': True
        }
        
        CCWTemplate.deploy(
            self,
            f'/var/www/{domain}/conf/nginx/ssl.conf',
            'ssl.mustache',
            data
        )
        
        # HTTPS Redirect
        SSL.httpsredirect(self, domain, True)
        
        return True
```

### 7.2 SSL Utils

```python
# ccw/core/sslutils.py
class SSL:
    """SSL/TLS Hilfsfunktionen"""
    
    @staticmethod
    def selfsignedcert(self, backend=False, proftpd=False):
        """Selbst-signiertes Zertifikat erstellen"""
        
        selfs_tmp = "/tmp/selfssl"
        CCWFileUtils.mkdir(self, selfs_tmp)
        
        try:
            # Private Key generieren
            CCWShellExec.cmd_exec(
                self,
                f"openssl genrsa -out {selfs_tmp}/ssl.key 2048"
            )
            
            # CSR erstellen
            CCWShellExec.cmd_exec(
                self,
                f"openssl req -new -batch "
                f"-subj /commonName=localhost/ "
                f"-key {selfs_tmp}/ssl.key "
                f"-out {selfs_tmp}/ssl.csr"
            )
            
            # Selbst-signieren
            CCWShellExec.cmd_exec(
                self,
                f"openssl x509 -req -days 3652 "
                f"-in {selfs_tmp}/ssl.csr "
                f"-signkey {selfs_tmp}/ssl.key "
                f"-out {selfs_tmp}/ssl.crt"
            )
            
            # Zertifikate verschieben
            if backend:
                target_path = "/var/www/22222/cert"
            elif proftpd:
                target_path = "/etc/proftpd/ssl"
            else:
                return
                
            CCWFileUtils.mkdir(self, target_path)
            CCWFileUtils.mvfile(self, f"{selfs_tmp}/ssl.key", f"{target_path}/")
            CCWFileUtils.mvfile(self, f"{selfs_tmp}/ssl.crt", f"{target_path}/")
            
        finally:
            CCWFileUtils.rm(self, selfs_tmp)
            
    @staticmethod
    def httpsredirect(self, domain, enable=True):
        """HTTP zu HTTPS Redirect"""
        
        force_ssl_conf = f"/etc/nginx/conf.d/force-ssl-{domain}.conf"
        
        if enable:
            data = {'domain': domain}
            CCWTemplate.deploy(
                self,
                force_ssl_conf,
                'force-ssl.mustache',
                data
            )
        else:
            if os.path.exists(force_ssl_conf):
                os.remove(force_ssl_conf)
                
    @staticmethod
    def setuphsts(self, domain):
        """HSTS Header aktivieren"""
        
        ssl_conf = f"/var/www/{domain}/conf/nginx/ssl.conf"
        
        if os.path.exists(ssl_conf):
            hsts_header = (
                "add_header Strict-Transport-Security "
                '"max-age=31536000; includeSubDomains; preload";'
            )
            
            with open(ssl_conf, 'a') as f:
                f.write(f"\n{hsts_header}\n")
                
    @staticmethod
    def getexpirationdate(self, domain):
        """SSL-Zertifikat Ablaufdatum prüfen"""
        
        cert_path = f"/etc/letsencrypt/live/{domain}/cert.pem"
        
        if os.path.exists(cert_path):
            try:
                output = subprocess.check_output(
                    f"openssl x509 -enddate -noout -in {cert_path}",
                    shell=True
                ).decode('utf-8')
                
                # Parse: notAfter=Dec 31 23:59:59 2024 GMT
                date_str = output.split('=')[1].strip()
                return datetime.strptime(date_str, '%b %d %H:%M:%S %Y %Z')
                
            except Exception as e:
                Log.debug(self, str(e))
                return None
        return None
```

---

## 8. Datenbank und Persistenz

### 8.1 SQLAlchemy Models

```python
# ccw/cli/plugins/models.py
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class SiteDB(Base):
    """Site-Metadaten Modell"""
    
    __tablename__ = 'sites'
    
    id = Column(Integer, primary_key=True)
    sitename = Column(String, unique=True, nullable=False)
    site_type = Column(String)  # html, php, wp, wpsubdir, wpsubdomain
    cache_type = Column(String)  # wpsc, wpfc, wpredis
    site_path = Column(String)
    created_on = Column(DateTime, default=datetime.utcnow)
    modified_on = Column(DateTime, onupdate=datetime.utcnow)
    is_enabled = Column(Boolean, default=True)
    is_ssl = Column(Boolean, default=False)
    php_version = Column(String)
    db_name = Column(String)
    db_user = Column(String)
    db_password = Column(String)
    db_host = Column(String, default='localhost')
    
    def __repr__(self):
        return f"<Site(name='{self.sitename}', type='{self.site_type}')>"

class OptionsDB(Base):
    """Globale Optionen"""
    
    __tablename__ = 'options'
    
    id = Column(Integer, primary_key=True)
    option_name = Column(String, unique=True)
    option_value = Column(String)
    
class MigrationsDB(Base):
    """Migration Tracking"""
    
    __tablename__ = 'migrations'
    
    id = Column(Integer, primary_key=True)
    version = Column(String, unique=True)
    applied_on = Column(DateTime, default=datetime.utcnow)
```

### 8.2 Datenbank-Operationen

```python
# ccw/cli/plugins/sitedb.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ccw.cli.plugins.models import SiteDB, Base
from ccw.core.variables import CCWVar

# Session Setup
engine = create_engine(CCWVar.ccw_db_uri)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def addNewSite(self, domain, **kwargs):
    """Neue Site zur DB hinzufügen"""
    
    session = Session()
    
    try:
        new_site = SiteDB(
            sitename=domain,
            site_type=kwargs.get('site_type', 'html'),
            cache_type=kwargs.get('cache_type', 'none'),
            site_path=kwargs.get('site_path', f'/var/www/{domain}'),
            php_version=kwargs.get('php_version', CCWVar.ccw_php),
            db_name=kwargs.get('db_name'),
            db_user=kwargs.get('db_user'),
            db_password=kwargs.get('db_password'),
            db_host=kwargs.get('db_host', 'localhost'),
            is_ssl=kwargs.get('is_ssl', False)
        )
        
        session.add(new_site)
        session.commit()
        
        Log.debug(self, f"Site {domain} zur Datenbank hinzugefügt")
        
    except Exception as e:
        session.rollback()
        Log.error(self, f"Fehler beim Hinzufügen der Site: {e}")
    finally:
        session.close()
        
def getSiteInfo(self, domain):
    """Site-Informationen abrufen"""
    
    session = Session()
    
    try:
        site = session.query(SiteDB).filter_by(sitename=domain).first()
        return site
    finally:
        session.close()
        
def updateSiteInfo(self, domain, **kwargs):
    """Site-Informationen aktualisieren"""
    
    session = Session()
    
    try:
        site = session.query(SiteDB).filter_by(sitename=domain).first()
        
        if site:
            for key, value in kwargs.items():
                if hasattr(site, key):
                    setattr(site, key, value)
                    
            site.modified_on = datetime.utcnow()
            session.commit()
            
            Log.debug(self, f"Site {domain} aktualisiert")
        else:
            Log.warn(self, f"Site {domain} nicht gefunden")
            
    except Exception as e:
        session.rollback()
        Log.error(self, f"Fehler beim Aktualisieren: {e}")
    finally:
        session.close()
        
def deleteSiteInfo(self, domain):
    """Site aus DB entfernen"""
    
    session = Session()
    
    try:
        site = session.query(SiteDB).filter_by(sitename=domain).first()
        
        if site:
            session.delete(site)
            session.commit()
            Log.debug(self, f"Site {domain} aus DB entfernt")
        else:
            Log.warn(self, f"Site {domain} nicht in DB gefunden")
            
    except Exception as e:
        session.rollback()
        Log.error(self, f"Fehler beim Löschen: {e}")
    finally:
        session.close()
        
def getAllsites(self, site_type=None):
    """Alle Sites abrufen"""
    
    session = Session()
    
    try:
        query = session.query(SiteDB)
        
        if site_type:
            query = query.filter_by(site_type=site_type)
            
        return query.all()
    finally:
        session.close()
```

---

## 9. Service-Management

### 9.1 Service Status Controller

```python
# ccw/cli/plugins/stack_services.py
class CCWStackStatusController(CementBaseController):
    class Meta:
        label = 'status'
        stacked_on = 'stack'
        stacked_type = 'nested'
        
    @expose(hide=True)
    def default(self):
        """Service-Status anzeigen"""
        
        services = []
        
        # Nginx
        if CCWAptGet.is_exec(self, 'nginx'):
            services.append(('Nginx', 'nginx'))
            
        # PHP Versionen
        for php_version in CCWVar.ccw_php_versions.values():
            if CCWAptGet.is_installed(self, f'php{php_version}-fpm'):
                services.append((f'PHP {php_version}', f'php{php_version}-fpm'))
                
        # MySQL/MariaDB
        if CCWMysql.mariadb_ping(self):
            services.append(('MariaDB', 'mariadb'))
            
        # Redis
        if CCWAptGet.is_installed(self, 'redis-server'):
            services.append(('Redis', 'redis-server'))
            
        # Status-Tabelle
        print("\n{:<20} {:<15} {:<10}".format("Service", "Status", "Port"))
        print("-" * 45)
        
        for name, service in services:
            status = get_service_status(self, service)
            port = get_service_port(service)
            
            status_color = "${GREEN}" if status == "active" else "${RED}"
            print(f"{name:<20} {status_color}{status:<15}${RESET} {port:<10}")
            
def get_service_port(service):
    """Service-Port ermitteln"""
    
    port_map = {
        'nginx': '80, 443',
        'php7.4-fpm': '9000',
        'php8.0-fpm': '9000',
        'php8.1-fpm': '9000',
        'php8.2-fpm': '9000',
        'php8.3-fpm': '9000',
        'mariadb': '3306',
        'redis-server': '6379',
    }
    
    return port_map.get(service, 'N/A')
```

---

## 10. Best Practices und Patterns

### 10.1 Design Patterns

```python
"""
Verwendete Design Patterns in CCC CODE:

1. SINGLETON PATTERN - CCWVar Klasse
   - Globale Konfiguration
   - Einmalige Initialisierung

2. FACTORY PATTERN - Stack/Site Creation
   - Dynamische Objekt-Erstellung
   - Typ-basierte Instanziierung

3. STRATEGY PATTERN - Cache-Typen
   - Austauschbare Algorithmen
   - Runtime-Auswahl

4. TEMPLATE METHOD - Installation Process
   - Definierter Ablauf
   - Hook-Points für Anpassung

5. COMMAND PATTERN - CLI Controller
   - Kapselung von Aktionen
   - Undo/Rollback Fähigkeit

6. REPOSITORY PATTERN - SiteDB Operations
   - Abstraktion der Datenschicht
   - Testbarkeit
"""
```

### 10.2 Error Handling

```python
class CCWErrorHandling:
    """Best Practices für Fehlerbehandlung"""
    
    @staticmethod
    def safe_execution(func):
        """Decorator für sichere Ausführung"""
        def wrapper(self, *args, **kwargs):
            try:
                # Backup vor kritischen Operationen
                if hasattr(self, 'backup_required'):
                    create_backup(self)
                    
                # Hauptfunktion ausführen
                result = func(self, *args, **kwargs)
                
                # Erfolg loggen
                Log.debug(self, f"{func.__name__} erfolgreich")
                return result
                
            except CommandExecutionError as e:
                Log.debug(self, str(e))
                Log.error(self, f"{func.__name__} fehlgeschlagen")
                
                # Rollback wenn möglich
                if hasattr(self, 'rollback_possible'):
                    perform_rollback(self)
                    
            except Exception as e:
                Log.debug(self, f"Unerwarteter Fehler: {e}")
                Log.error(self, "Kritischer Fehler aufgetreten")
                
        return wrapper
```

### 10.3 Performance Optimierungen

```python
class PerformanceOptimizations:
    """Performance Best Practices"""
    
    # 1. Lazy Loading
    @property
    def php_versions(self):
        if not hasattr(self, '_php_versions'):
            self._php_versions = self._detect_php_versions()
        return self._php_versions
        
    # 2. Caching
    @lru_cache(maxsize=128)
    def get_site_info(self, domain):
        return getSiteInfo(self, domain)
        
    # 3. Batch-Operationen
    def install_packages(self, packages):
        # Einzeln installieren ist langsam
        # for pkg in packages:
        #     apt_install(pkg)
        
        # Batch ist schneller
        apt_install(' '.join(packages))
        
    # 4. Connection Pooling
    engine = create_engine(
        CCWVar.ccw_db_uri,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True
    )
```

### 10.4 Sicherheits-Checkliste

```yaml
# CCC CODE Sicherheits-Best-Practices

System-Level:
  - EUID Root-Check
  - Sichere Temp-Verzeichnisse
  - Dateiberechtigungen (0600 für Configs)
  - GPG-Signatur-Verifizierung

Passwörter:
  - Mindestens 24 Zeichen
  - Zufällige Generierung
  - Sichere Speicherung (my.cnf mit 0600)
  - Keine Hardcoded Credentials

Netzwerk:
  - UFW Firewall Standard
  - Fail2ban Integration
  - SSL/TLS Erzwingung
  - HSTS Headers

Datenbank:
  - Prepared Statements
  - Grant-Host Einschränkung
  - Regelmäßige Backups
  - Verschlüsselte Verbindungen

Logging:
  - Sensitive Daten maskieren
  - Log-Rotation
  - Zentrale Log-Verwaltung
  - Audit-Trail
```

### 10.5 Deployment Pipeline

```bash
# CCC CODE CI/CD Pipeline

# 1. Pre-Flight Checks
check_system_requirements() {
    check_distro
    check_dependencies
    check_disk_space
    check_network
}

# 2. Installation
install_ccc_code() {
    setup_python_venv
    install_dependencies
    configure_system
    run_tests
}

# 3. Validation
validate_installation() {
    test_nginx_config
    test_php_fpm
    test_mysql_connection
    test_ssl_issuance
}

# 4. Monitoring
setup_monitoring() {
    configure_netdata
    setup_log_rotation
    enable_alerts
}
```

---

## Zusammenfassung

Diese umfassende Analyse zeigt die komplexe aber gut strukturierte Architektur von CCC CODE:

### Stärken:
1. **Modularer Aufbau**: Klare Trennung von Concerns
2. **Robuste Fehlerbehandlung**: Rollback-Mechanismen und Git-Integration
3. **Sicherheit**: Mehrschichtige Sicherheitsmaßnahmen
4. **Automatisierung**: Minimale manuelle Eingriffe nötig
5. **Flexibilität**: Support für multiple PHP-Versionen und Cache-Typen

### Architektur-Highlights:
- **Hybrid-Ansatz**: Bash für Bootstrap, Python für Logik
- **Cement Framework**: Solide CLI-Foundation
- **Template-Engine**: Konfiguration als Code
- **Service-Orchestrierung**: Systemd-Integration

### Für Entwickler:
- Code ist gut dokumentiert und folgt Python-Standards
- Testbare Architektur mit klaren Interfaces
- Erweiterbar durch Plugin-System
- Git-basierte Konfigurationsverwaltung

### Für AI-Agenten:
- Klare Funktions-Signaturen und Typen
- Vorhersagbare Fehlerbehandlung
- Strukturierte Datenmodelle
- Konsistente Naming-Conventions

Diese Analyse bietet eine solide Grundlage für die Weiterentwicklung und Wartung des CCC CODE-Systems.

<!-- Zuletzt bearbeitet: 2025-10-30 -->
