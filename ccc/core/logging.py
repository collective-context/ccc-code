import sys

class Log:
    """
    Logs messages with colors for different message types
    """
    
    # ANSI color codes
    RESET = '\033[0m'
    RED = '\033[1;31m'
    GREEN = '\033[1;32m'
    YELLOW = '\033[1;33m'
    CYAN = '\033[1;36m'
    
    @staticmethod
    def error(self, msg, exit=True):
        """Log error message and optionally exit"""
        print(f"{Log.RED}[ERROR] {msg}{Log.RESET}")
        if exit:
            sys.exit(1)
    
    @staticmethod
    def info(self, msg, end='\n', log=True):
        """Log info message"""
        print(f"{Log.CYAN}[INFO] {msg}{Log.RESET}", end=end)
    
    @staticmethod
    def warn(self, msg):
        """Log warning message"""
        print(f"{Log.YELLOW}[WARN] {msg}{Log.RESET}")
    
    @staticmethod
    def debug(self, msg):
        """Log debug message"""
        if hasattr(self, 'app') and hasattr(self.app, 'debug'):
            if self.app.debug:
                print(f"[DEBUG] {msg}")
        else:
            # Fallback for when app is not available
            print(f"[DEBUG] {msg}")
    
    @staticmethod
    def wait(self, msg, end='\r', log=True):
        """Log waiting message"""
        print(f"{Log.CYAN}[....] {msg}{Log.RESET}", end=end)
    
    @staticmethod
    def valide(self, msg, end='\n', log=True):
        """Log success message"""
        print(f"{Log.GREEN}[ OK ] {msg}{Log.RESET}", end=end)
    
    @staticmethod
    def failed(self, msg, end='\n', log=True):
        """Log failure message"""
        print(f"{Log.RED}[FAIL] {msg}{Log.RESET}", end=end)
