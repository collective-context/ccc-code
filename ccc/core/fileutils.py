import os
import shutil
from ccc.core.logging import Log

class CCCFileUtils:
    """File utilities for CCC CODE"""
    
    @staticmethod
    def mkdir(self, path):
        """Create directory"""
        try:
            if not os.path.exists(path):
                os.makedirs(path, mode=0o755)
                Log.debug(self, f"Created directory: {path}")
        except Exception as e:
            Log.error(self, f"Failed to create directory {path}: {e}")
    
    @staticmethod
    def create_symlink(self, source, target):
        """Create symbolic link"""
        try:
            if os.path.exists(target):
                os.remove(target)
            os.symlink(source, target)
            Log.debug(self, f"Created symlink: {source} -> {target}")
        except Exception as e:
            Log.error(self, f"Failed to create symlink: {e}")
    
    @staticmethod
    def chown(self, path, user, group, recursive=False):
        """Change file ownership"""
        try:
            import pwd
            import grp
            
            uid = pwd.getpwnam(user).pw_uid
            gid = grp.getgrnam(group).gr_gid
            
            if recursive and os.path.isdir(path):
                for root, dirs, files in os.walk(path):
                    os.chown(root, uid, gid)
                    for d in dirs:
                        os.chown(os.path.join(root, d), uid, gid)
                    for f in files:
                        os.chown(os.path.join(root, f), uid, gid)
            else:
                os.chown(path, uid, gid)
            
            Log.debug(self, f"Changed ownership of {path} to {user}:{group}")
        except Exception as e:
            Log.error(self, f"Failed to change ownership: {e}")
    
    @staticmethod
    def chmod(self, path, mode, recursive=False):
        """Change file permissions"""
        try:
            if recursive and os.path.isdir(path):
                for root, dirs, files in os.walk(path):
                    os.chmod(root, mode)
                    for d in dirs:
                        os.chmod(os.path.join(root, d), mode)
                    for f in files:
                        os.chmod(os.path.join(root, f), mode)
            else:
                os.chmod(path, mode)
            
            Log.debug(self, f"Changed permissions of {path} to {oct(mode)}")
        except Exception as e:
            Log.error(self, f"Failed to change permissions: {e}")
    
    @staticmethod
    def rm(self, path):
        """Remove file or directory"""
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
            elif os.path.exists(path):
                os.remove(path)
            Log.debug(self, f"Removed: {path}")
        except Exception as e:
            Log.error(self, f"Failed to remove {path}: {e}")
    
    @staticmethod
    def copyfile(self, source, target):
        """Copy file"""
        try:
            shutil.copy2(source, target)
            Log.debug(self, f"Copied {source} to {target}")
        except Exception as e:
            Log.error(self, f"Failed to copy file: {e}")
