import subprocess
from ccc.core.logging import Log
from ccc.core.shellexec import CCCShellExec

class CCCAptGet:
    """APT package management wrapper for CCC CODE"""
    
    @staticmethod
    def update(self):
        """Update APT cache"""
        try:
            Log.wait(self, "Updating APT cache...")
            CCCShellExec.cmd_exec(
                self,
                "DEBIAN_FRONTEND=noninteractive apt-get update -qq"
            )
            Log.valide(self, "APT cache updated")
        except Exception as e:
            Log.debug(self, str(e))
            Log.error(self, "APT update failed")
    
    @staticmethod
    def install(self, packages):
        """Install packages"""
        if isinstance(packages, str):
            packages = [packages]
        
        apt_cmd = (
            "DEBIAN_FRONTEND=noninteractive "
            "apt-get install -qq "
            "--option=Dpkg::options::=--force-confmiss "
            "--option=Dpkg::options::=--force-confold "
            "--assume-yes {0}"
        )
        
        try:
            for package in packages:
                if not CCCAptGet.is_installed(self, package):
                    Log.wait(self, f"Installing {package}")
                    CCCShellExec.cmd_exec(
                        self,
                        apt_cmd.format(package)
                    )
                    Log.valide(self, f"Installed {package}")
        except Exception as e:
            Log.debug(self, str(e))
            Log.error(self, "Package installation failed")
    
    @staticmethod
    def is_installed(self, package):
        """Check if package is installed"""
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
    def remove(self, packages, purge=False):
        """Remove packages"""
        if isinstance(packages, str):
            packages = [packages]
        
        cmd = "purge" if purge else "remove"
        apt_cmd = f"DEBIAN_FRONTEND=noninteractive apt-get {cmd} -qq --assume-yes {{0}}"
        
        try:
            for package in packages:
                if CCCAptGet.is_installed(self, package):
                    Log.wait(self, f"Removing {package}")
                    CCCShellExec.cmd_exec(self, apt_cmd.format(package))
                    Log.valide(self, f"Removed {package}")
        except Exception as e:
            Log.debug(self, str(e))
            Log.error(self, "Package removal failed")
