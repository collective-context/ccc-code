import subprocess
from ccc.core.logging import Log

class CCCService:
    """Systemd service management for CCC CODE"""
    
    @staticmethod
    def start_service(self, service):
        """Start a service"""
        try:
            Log.wait(self, f"Starting {service}")
            retcode = subprocess.call(
                ["systemctl", "start", service],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            if retcode == 0:
                Log.valide(self, f"Started {service}")
                return True
            else:
                Log.failed(self, f"Failed to start {service}")
                return False
        except Exception as e:
            Log.debug(self, str(e))
            return False
    
    @staticmethod
    def stop_service(self, service):
        """Stop a service"""
        try:
            Log.wait(self, f"Stopping {service}")
            retcode = subprocess.call(
                ["systemctl", "stop", service],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            if retcode == 0:
                Log.valide(self, f"Stopped {service}")
                return True
            else:
                Log.failed(self, f"Failed to stop {service}")
                return False
        except Exception as e:
            Log.debug(self, str(e))
            return False
    
    @staticmethod
    def restart_service(self, service):
        """Restart a service"""
        try:
            Log.wait(self, f"Restarting {service}")
            retcode = subprocess.call(
                ["systemctl", "restart", service],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            if retcode == 0:
                Log.valide(self, f"Restarted {service}")
                return True
            else:
                Log.failed(self, f"Failed to restart {service}")
                return False
        except Exception as e:
            Log.debug(self, str(e))
            return False
    
    @staticmethod
    def reload_service(self, service):
        """Reload a service"""
        try:
            Log.wait(self, f"Reloading {service}")
            retcode = subprocess.call(
                ["systemctl", "reload", service],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            if retcode == 0:
                Log.valide(self, f"Reloaded {service}")
                return True
            else:
                Log.failed(self, f"Failed to reload {service}")
                return False
        except Exception as e:
            Log.debug(self, str(e))
            return False
    
    @staticmethod
    def get_service_status(self, service):
        """Get service status"""
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
