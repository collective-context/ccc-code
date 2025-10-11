from cement.core.controller import CementBaseController, expose
from ccc.core.logging import Log
from ccc.core.variables import CCCVar
from ccc.core.aptget import CCCAptGet
from ccc.core.services import CCCService

class CCCStackController(CementBaseController):
    class Meta:
        label = 'stack'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = 'Stack Management for NGINX, PHP, Redis, and MySQL'
        arguments = [
            (['--all'], dict(help='Install all stacks', action='store_true')),
            (['--nginx'], dict(help='Install NGINX', action='store_true')),
            (['--php'], dict(help='Install PHP', action='store_true')),
            (['--mysql'], dict(help='Install MySQL 8', action='store_true')),
            (['--redis'], dict(help='Install Redis', action='store_true')),
            (['--force'], dict(help='Force installation', action='store_true')),
        ]
    
    @expose(help="Install stacks")
    def install(self):
        """Install server stacks"""
        pargs = self.app.pargs
        apt_packages = []
        
        if pargs.all:
            pargs.nginx = True
            pargs.php = True
            pargs.mysql = True
            pargs.redis = True
        
        # NGINX Installation
        if pargs.nginx:
            Log.info(self, "Installing NGINX...")
            if not CCCAptGet.is_installed(self, 'nginx'):
                apt_packages.extend(CCCVar.ccc_nginx)
            else:
                Log.info(self, "NGINX is already installed")
        
        # PHP Installation
        if pargs.php:
            Log.info(self, f"Installing PHP {CCCVar.ccc_php}...")
            php_packages = CCCVar.generate_php_modules(CCCVar.ccc_php)
            for pkg in php_packages:
                if not CCCAptGet.is_installed(self, pkg):
                    apt_packages.append(pkg)
        
        # MySQL 8 Installation
        if pargs.mysql:
            Log.info(self, "Installing MySQL 8...")
            apt_packages.extend(CCCVar.ccc_mysql)
        
        # Redis Installation
        if pargs.redis:
            Log.info(self, "Installing Redis...")
            apt_packages.extend(CCCVar.ccc_redis)
        
        # Install packages
        if apt_packages:
            Log.wait(self, "Installing packages...")
            CCCAptGet.update(self)
            CCCAptGet.install(self, apt_packages)
            Log.valide(self, "Package installation completed")
        
        # Start services
        if pargs.nginx:
            CCCService.start_service(self, 'nginx')
        if pargs.php:
            CCCService.start_service(self, f'php{CCCVar.ccc_php}-fpm')
        if pargs.mysql:
            CCCService.start_service(self, 'mysql')
        if pargs.redis:
            CCCService.start_service(self, 'redis-server')
    
    @expose(help="Upgrade stacks")
    def upgrade(self):
        """Upgrade server stacks"""
        Log.info(self, "Upgrading stacks...")
        CCCAptGet.update(self)
        # Upgrade logic here
        Log.valide(self, "Stack upgrade completed")
    
    @expose(help="Remove stacks")
    def remove(self):
        """Remove server stacks"""
        Log.warn(self, "Stack removal is not yet implemented")
    
    @expose(help="Restart stack services")
    def restart(self):
        """Restart stack services"""
        pargs = self.app.pargs
        
        if pargs.nginx:
            CCCService.restart_service(self, 'nginx')
        if pargs.php:
            CCCService.restart_service(self, f'php{CCCVar.ccc_php}-fpm')
        if pargs.mysql:
            CCCService.restart_service(self, 'mysql')
        if pargs.redis:
            CCCService.restart_service(self, 'redis-server')
    
    @expose(help="Show stack status")
    def status(self):
        """Show status of installed stacks"""
        services = [
            ('NGINX', 'nginx'),
            (f'PHP {CCCVar.ccc_php}', f'php{CCCVar.ccc_php}-fpm'),
            ('MySQL 8', 'mysql'),
            ('Redis', 'redis-server'),
        ]
        
        print("\n{:<20} {:<15}".format("Service", "Status"))
        print("-" * 35)
        
        for name, service in services:
            if CCCService.get_service_status(self, service):
                status = "Active"
                print(f"{name:<20} \033[1;32m{status:<15}\033[0m")
            else:
                status = "Inactive"
                print(f"{name:<20} \033[1;31m{status:<15}\033[0m")
