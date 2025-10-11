import subprocess
from ccc.core.logging import Log
from ccc.core.services import CCCService

class CCCNginx:
    """NGINX management for CCC CODE"""
    
    @staticmethod
    def test_config(self):
        """Test NGINX configuration"""
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
    def reload(self):
        """Reload NGINX"""
        if CCCNginx.test_config(self):
            return CCCService.reload_service(self, 'nginx')
        else:
            Log.error(self, "NGINX configuration test failed")
            return False
    
    @staticmethod
    def restart(self):
        """Restart NGINX"""
        if CCCNginx.test_config(self):
            return CCCService.restart_service(self, 'nginx')
        else:
            Log.error(self, "NGINX configuration test failed")
            return False
