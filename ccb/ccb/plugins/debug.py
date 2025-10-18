"""Debug plugin for ccb - aggregate all logs"""
from cement import Controller, ex
import subprocess
import os
from datetime import datetime


class DebugController(Controller):
    """Debug controller for log aggregation"""
    
    class Meta:
        label = 'debug'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = 'Debug and analyze ccb development'
    
    @ex(help='run all tests and aggregate logs')
    def run(self):
        """Run local tests + fetch GitHub Actions + aggregate everything"""
        log_dir = "./logs"
        log_file = f"{log_dir}/ccb-debug.log"
        
        print("🔍 Running comprehensive debug analysis...")
        print(f"📝 Log file: {log_file}")
        print("")
        
        # Run local tests (writes to log automatically)
        print("1️⃣ Running local tests...")
        result = subprocess.run(['bash', 'tests-ccb/travis.sh'])
        
        if result.returncode != 0:
            print("⚠️  Some local tests failed (see log)")
        
        # Fetch GitHub Actions (append to same log)
        print("")
        print("2️⃣ Fetching GitHub Actions logs...")
        subprocess.run(['ccb', 'check', 'actions', '--save'])
        
        # Show summary
        print("")
        print("✅ Debug analysis complete!")
        print(f"📄 Full log: {log_file}")
        print("")
        print("To view log:")
        print(f"  cat {log_file}")
        print("")
        print("To see summary:")
        print(f"  ccb debug summary")
    
    @ex(help='show summary of debug log')
    def summary(self):
        """Show summary from debug log"""
        log_file = "./logs/ccb-debug.log"
        
        if not os.path.exists(log_file):
            print("❌ No debug log found.")
            print("Run: ccb debug run")
            return
        
        with open(log_file, 'r') as f:
            content = f.read()
        
        # Count results
        passes = content.count('✓')
        fails = content.count('✗')
        
        print("\n=== DEBUG SUMMARY ===")
        print(f"✓ Passed: {passes}")
        print(f"✗ Failed: {fails}")
        print("")
        
        # Show failed tests
        if fails > 0:
            print("Failed Tests:")
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if '✗' in line:
                    print(f"  {line.strip()}")
                    # Show error details if available
                    if i + 1 < len(lines) and 'Error:' in lines[i + 1]:
                        print(f"    {lines[i + 1].strip()}")
        
        print(f"\nFull log: {log_file}")
        print("")


def load(app):
    """Load debug plugin"""
    app.handler.register(DebugController)
