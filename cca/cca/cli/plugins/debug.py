"""Debug plugin for test aggregation and analysis"""

import subprocess
import os
from cement.core.controller import CementBaseController, expose


class CCADebugController(CementBaseController):
    """Controller for debug commands"""
    
    class Meta:
        label = 'debug'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = 'Debug and diagnostic tools for CCA'

    @expose(help='Run all CCA tests and collect results')
    def run(self):
        """Run comprehensive test suite"""
        print("=== CCA Debug Test Run ===\n")
        
        # Create logs directory
        os.makedirs('logs', exist_ok=True)
        log_file = 'logs/cca-debug.log'
        
        with open(log_file, 'w') as f:
            f.write("=== CCA Debug Log ===\n\n")
            
            # Test 1: Run bash tests
            print("1. Running bash tests...")
            f.write("=== Bash Tests ===\n")
            try:
                result = subprocess.run(
                    ['bash', 'tests-cca/travis.sh'],
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                f.write("Exit code: {}\n".format(result.returncode))
                f.write("STDOUT:\n{}\n".format(result.stdout))
                f.write("STDERR:\n{}\n".format(result.stderr))
                
                if result.returncode == 0:
                    print("   ✓ Bash tests passed")
                else:
                    print("   ✗ Bash tests failed (exit code: {})".format(result.returncode))
            except subprocess.TimeoutExpired:
                print("   ✗ Bash tests timed out")
                f.write("ERROR: Bash tests timed out\n")
            except Exception as e:
                print("   ✗ Bash tests error: {}".format(e))
                f.write("ERROR: {}\n".format(e))
            
            # Test 2: Check GitHub Actions
            print("2. Checking GitHub Actions...")
            f.write("\n=== GitHub Actions Status ===\n")
            try:
                result = subprocess.run(
                    ['cca', 'check', 'actions'],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                f.write(result.stdout)
                if result.stderr:
                    f.write("STDERR:\n{}\n".format(result.stderr))
                print("   ✓ GitHub Actions check completed")
            except Exception as e:
                print("   ✗ GitHub Actions check failed: {}".format(e))
                f.write("ERROR: {}\n".format(e))
            
            print("\n✓ Debug log saved to {}".format(log_file))
            print("Run 'cca debug summary' to see test results summary")

    @expose(help='Show test summary from debug log')
    def summary(self):
        """Display test results summary"""
        print("=== CCA Test Summary ===\n")
        
        log_file = 'logs/cca-debug.log'
        if not os.path.exists(log_file):
            print("No debug log found. Run 'cca debug run' first.")
            return
        
        with open(log_file, 'r') as f:
            content = f.read()
        
        # Count test results
        passed = content.count('✓')
        failed = content.count('✗')
        
        print("Tests Passed: {}".format(passed))
        print("Tests Failed: {}".format(failed))
        
        if failed > 0:
            print("\n=== Failed Tests ===")
            for line in content.split('\n'):
                if '✗' in line:
                    print("  {}".format(line.strip()))
        
        # Check for GitHub Actions status
        if 'Conclusion: success' in content:
            print("\n✓ GitHub Actions: SUCCESS")
        elif 'Conclusion: failure' in content:
            print("\n✗ GitHub Actions: FAILURE")
            
        print("\nFull log available at: {}".format(log_file))


def load(app):
    """Load the debug plugin (required for Cement v2)"""
    app.handler.register(CCADebugController)
