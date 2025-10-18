"""Check plugin for GitHub Actions integration"""

import subprocess
import sys
from cement.core.controller import CementBaseController, expose


class CCACheckController(CementBaseController):
    """Controller for check commands"""
    
    class Meta:
        label = 'check'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = 'Check various CCA components'

    @expose(help='Check GitHub Actions status for test-cca workflow')
    def actions(self):
        """Check GitHub Actions status"""
        print("=== CCA GitHub Actions Status ===\n")
        
        save_to_log = '--save' in sys.argv
        log_content = []
        
        try:
            # Get latest workflow runs
            cmd = [
                'gh', 'run', 'list',
                '--workflow', 'test-cca.yml',
                '--repo', 'collective-context/ccc-code',
                '--limit', '5'
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False
            )
            
            if result.returncode != 0:
                error_msg = "Failed to get workflow runs: {}".format(result.stderr)
                print(error_msg)
                if save_to_log:
                    log_content.append(error_msg)
                sys.exit(1)
            
            print("Recent workflow runs:")
            print(result.stdout)
            if save_to_log:
                log_content.append("Recent workflow runs:")
                log_content.append(result.stdout)
            
            # Get details of the latest run
            lines = result.stdout.strip().split('\n')
            if len(lines) > 1:  # Skip header
                latest_run = lines[1].split('\t')
                if latest_run:
                    status = latest_run[0] if len(latest_run) > 0 else 'unknown'
                    conclusion = latest_run[1] if len(latest_run) > 1 else 'unknown'
                    run_id = latest_run[6] if len(latest_run) > 6 else None
                    
                    print("\nLatest run status: {}".format(status))
                    print("Conclusion: {}".format(conclusion))
                    
                    if save_to_log:
                        log_content.append("\nLatest run status: {}".format(status))
                        log_content.append("Conclusion: {}".format(conclusion))
                    
                    # If failed, show failed steps
                    if conclusion == 'failure' and run_id:
                        print("\n=== Failed Steps ===")
                        if save_to_log:
                            log_content.append("\n=== Failed Steps ===")
                        
                        # Get failed jobs
                        cmd_jobs = [
                            'gh', 'run', 'view', run_id,
                            '--repo', 'collective-context/ccc-code',
                            '--log-failed'
                        ]
                        
                        result_jobs = subprocess.run(
                            cmd_jobs,
                            capture_output=True,
                            text=True,
                            check=False
                        )
                        
                        if result_jobs.returncode == 0:
                            # Show first 50 lines of failed logs
                            failed_lines = result_jobs.stdout.split('\n')[:50]
                            failed_output = '\n'.join(failed_lines)
                            print(failed_output)
                            if save_to_log:
                                log_content.append(failed_output)
                        else:
                            print("Could not retrieve failed job logs")
                            if save_to_log:
                                log_content.append("Could not retrieve failed job logs")
            
            # Save to log file if requested
            if save_to_log and log_content:
                import os
                os.makedirs('logs', exist_ok=True)
                with open('logs/cca-debug.log', 'w') as f:
                    f.write('\n'.join(log_content))
                print("\n✓ Logs saved to logs/cca-debug.log")
                
        except FileNotFoundError:
            print("Error: GitHub CLI (gh) is not installed.")
            print("Please install it first: https://cli.github.com/")
            sys.exit(1)
        except Exception as e:
            print("Error checking GitHub Actions: {}".format(e))
            sys.exit(1)


def load(app):
    """Load the check plugin (required for Cement v2)"""
    app.handler.register(CCACheckController)
