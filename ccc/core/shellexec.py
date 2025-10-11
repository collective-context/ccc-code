import subprocess
from ccc.core.logging import Log

class CCCShellExec:
    """Shell command execution for CCC CODE"""
    
    @staticmethod
    def cmd_exec(self, command, errormsg='', log=True):
        """Execute shell command"""
        try:
            if log:
                Log.debug(self, f"Executing: {command}")
            
            proc = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, stderr = proc.communicate()
            
            if proc.returncode != 0:
                if errormsg:
                    Log.error(self, errormsg)
                raise Exception(stderr.decode('utf-8'))
            
            return True
        except Exception as e:
            Log.debug(self, str(e))
            if errormsg:
                Log.error(self, errormsg)
            raise
    
    @staticmethod
    def cmd_exec_stdout(self, command, errormsg='', log=True):
        """Execute shell command and return stdout"""
        try:
            if log:
                Log.debug(self, f"Executing: {command}")
            
            proc = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, stderr = proc.communicate()
            
            if proc.returncode != 0:
                if errormsg:
                    Log.error(self, errormsg)
                raise Exception(stderr.decode('utf-8'))
            
            return stdout.decode('utf-8').strip()
        except Exception as e:
            Log.debug(self, str(e))
            if errormsg:
                Log.error(self, errormsg)
            return None
