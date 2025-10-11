from cement.core.controller import CementBaseController, expose
from ccc.core.logging import Log
from ccc.core.variables import CCCVar
from ccc.core.fileutils import CCCFileUtils
from ccc.core.nginx import CCCNginx
import os

class CCCSiteController(CementBaseController):
    class Meta:
        label = 'site'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = 'Site Management for NGINX'
        arguments = [
            (['site_name'], dict(help='Site domain name', nargs='?')),
        ]
    
    @expose(help="Create a new site")
    def create(self):
        """Create a new NGINX site"""
        pargs = self.app.pargs
        
        if not pargs.site_name:
            Log.error(self, "Please provide a site name")
        
        domain = pargs.site_name
        webroot = f"{CCCVar.ccc_webroot_dir}/{domain}"
        
        # Create webroot directory
        Log.info(self, f"Creating site: {domain}")
        CCCFileUtils.mkdir(self, f"{webroot}/htdocs")
        CCCFileUtils.mkdir(self, f"{webroot}/logs")
        CCCFileUtils.mkdir(self, f"{webroot}/conf/nginx")
        
        # Create NGINX configuration
        nginx_conf = f"""server {{
    listen 80;
    listen [::]:80;
    server_name {domain} www.{domain};
    
    root {webroot}/htdocs;
    index index.html index.htm index.php;
    
    access_log {webroot}/logs/access.log;
    error_log {webroot}/logs/error.log;
    
    location / {{
        try_files $uri $uri/ =404;
    }}
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
}}"""
        
        # Write NGINX configuration
        nginx_conf_path = f"/etc/nginx/sites-available/{domain}"
        with open(nginx_conf_path, 'w') as f:
            f.write(nginx_conf)
        
        # Enable site
        CCCFileUtils.create_symlink(
            self,
            nginx_conf_path,
            f"/etc/nginx/sites-enabled/{domain}"
        )
        
        # Create default index.html
        index_html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Welcome to {domain}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            text-align: center;
            padding: 50px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}
        h1 {{ font-size: 3em; }}
        p {{ font-size: 1.2em; }}
    </style>
</head>
<body>
    <h1>Welcome to {domain}</h1>
    <p>Your site has been successfully created with CCC CODE</p>
    <p><small>Powered by NGINX</small></p>
</body>
</html>"""
        
        with open(f"{webroot}/htdocs/index.html", 'w') as f:
            f.write(index_html)
        
        # Set permissions
        CCCFileUtils.chown(self, webroot, 'www-data', 'www-data', recursive=True)
        
        # Test and reload NGINX
        if CCCNginx.test_config(self):
            CCCNginx.reload(self)
            Log.valide(self, f"Site {domain} created successfully")
            Log.info(self, f"Webroot: {webroot}")
            Log.info(self, f"Access URL: http://{domain}")
        else:
            Log.error(self, "NGINX configuration test failed")
    
    @expose(help="Delete a site")
    def delete(self):
        """Delete an existing site"""
        pargs = self.app.pargs
        
        if not pargs.site_name:
            Log.error(self, "Please provide a site name")
        
        domain = pargs.site_name
        
        # Confirm deletion
        confirm = input(f"Are you sure you want to delete {domain}? [y/N]: ")
        if confirm.lower() != 'y':
            Log.info(self, "Deletion cancelled")
            return
        
        # Remove NGINX configuration
        if os.path.exists(f"/etc/nginx/sites-enabled/{domain}"):
            os.remove(f"/etc/nginx/sites-enabled/{domain}")
        if os.path.exists(f"/etc/nginx/sites-available/{domain}"):
            os.remove(f"/etc/nginx/sites-available/{domain}")
        
        # Remove webroot
        webroot = f"{CCCVar.ccc_webroot_dir}/{domain}"
        if os.path.exists(webroot):
            CCCFileUtils.rm(self, webroot)
        
        # Reload NGINX
        CCCNginx.reload(self)
        Log.valide(self, f"Site {domain} deleted successfully")
    
    @expose(help="List all sites")
    def list(self):
        """List all configured sites"""
        sites_dir = "/etc/nginx/sites-available"
        if os.path.exists(sites_dir):
            sites = [f for f in os.listdir(sites_dir) if f != 'default']
            
            if sites:
                print("\nConfigured sites:")
                print("-" * 40)
                for site in sorted(sites):
                    enabled = "✓" if os.path.exists(f"/etc/nginx/sites-enabled/{site}") else "✗"
                    print(f"  [{enabled}] {site}")
            else:
                Log.info(self, "No sites configured")
        else:
            Log.error(self, "NGINX sites directory not found")
    
    @expose(help="Enable a site")
    def enable(self):
        """Enable a disabled site"""
        pargs = self.app.pargs
        
        if not pargs.site_name:
            Log.error(self, "Please provide a site name")
        
        domain = pargs.site_name
        available = f"/etc/nginx/sites-available/{domain}"
        enabled = f"/etc/nginx/sites-enabled/{domain}"
        
        if not os.path.exists(available):
            Log.error(self, f"Site {domain} does not exist")
        
        if os.path.exists(enabled):
            Log.info(self, f"Site {domain} is already enabled")
            return
        
        CCCFileUtils.create_symlink(self, available, enabled)
        CCCNginx.reload(self)
        Log.valide(self, f"Site {domain} enabled")
    
    @expose(help="Disable a site")
    def disable(self):
        """Disable an enabled site"""
        pargs = self.app.pargs
        
        if not pargs.site_name:
            Log.error(self, "Please provide a site name")
        
        domain = pargs.site_name
        enabled = f"/etc/nginx/sites-enabled/{domain}"
        
        if not os.path.exists(enabled):
            Log.info(self, f"Site {domain} is not enabled")
            return
        
        os.remove(enabled)
        CCCNginx.reload(self)
        Log.valide(self, f"Site {domain} disabled")
