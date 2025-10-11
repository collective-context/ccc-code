import platform
import os

class CCCVar:
    """Central configuration variables for CCC CODE"""
    
    # System detection
    try:
        import distro
        ccc_distro = distro.id().lower()
        ccc_platform_version = distro.version()
        ccc_platform_codename = distro.codename()
    except:
        # Fallback for older systems
        ccc_distro = 'unknown'
        ccc_platform_version = '0'
        ccc_platform_codename = os.popen("lsb_release -sc 2>/dev/null").read().strip()
    
    # Version
    ccc_version = '1.0.0'
    
    # Paths
    ccc_log_dir = '/var/log/ccc'
    ccc_lib_dir = '/var/lib/ccc'
    ccc_config_dir = '/etc/ccc'
    ccc_backup_dir = '/var/lib/ccc-backup'
    ccc_webroot_dir = '/var/www'
    
    # Database
    ccc_db_path = '/var/lib/ccc/dbase.db'
    ccc_db_uri = f'sqlite:///{ccc_db_path}'
    
    # PHP Versions (for future use with BookStack)
    ccc_php_versions = {
        'php74': '7.4',
        'php80': '8.0',
        'php81': '8.1',
        'php82': '8.2',
        'php83': '8.3',
        'php84': '8.4',
    }
    
    # Default PHP version
    ccc_php = '8.3'
    
    # NGINX packages
    ccc_nginx = ["nginx-custom", "nginx-wo"]
    
    # Redis packages
    ccc_redis = ["redis-server", "redis-tools"]
    
    # MySQL 8 packages (for future BookStack support)
    ccc_mysql = [
        "mysql-server-8.0",
        "mysql-client-8.0",
        "python3-mysqldb"
    ]
    
    # SSL paths
    ccc_ssl_live = "/etc/letsencrypt/live"
    ccc_ssl_archive = "/etc/letsencrypt/renewal"
    ccc_ssl_cert = "/cert.pem"
    ccc_ssl_key = "/privkey.pem"
    
    # Repository URLs
    ccc_nginx_repo = "http://download.opensuse.org/repositories/home:/virtubox:/WordOps"
    
    @staticmethod
    def generate_php_modules(version):
        """Generate PHP module list dynamically"""
        base_modules = [
            'fpm', 'curl', 'gd', 'imap', 'readline', 'common',
            'redis', 'mysql', 'cli', 'mbstring', 'bcmath',
            'opcache', 'zip', 'xml', 'soap', 'intl'
        ]
        
        return [f"php{version}-{mod}" for mod in base_modules]
