"""
GitHub Actions checker plugin for ccb
"""
from cement import Controller, ex
import subprocess
import json
from datetime import datetime
import os


class CheckController(Controller):
    """Controller for check commands"""
    
    class Meta:
        label = 'check'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = 'Check GitHub workflows and CI/CD status'
        
    @ex(
        help='fetch latest GitHub Actions workflow logs',
        arguments=[
            (['--save'], {
                'help': 'save logs to ./logs/ccb-debug.log',
                'action': 'store_true'
            })
        ]
    )
    def actions(self):
        """Fetch and save latest GitHub Actions workflow logs"""
        
        self.app.log.info('Fetching latest GitHub Actions workflow...')
        
        try:
            # Get latest workflow run using gh CLI
            result = subprocess.run(
                ['gh', 'run', 'list', 
                 '--repo', 'collective-context/ccc-code',
                 '--workflow', 'test-ccb.yml',
                 '--limit', '1', '--json', 
                 'databaseId,name,status,conclusion,createdAt,displayTitle,url'],
                capture_output=True, 
                text=True,
                check=True
            )
            
            runs = json.loads(result.stdout)
            
            if not runs:
                self.app.log.error('No workflow runs found')
                return
            
            latest_run = runs[0]
            run_id = latest_run['databaseId']
            
            # Build output
            output_lines = []
            output_lines.append("\n=== GITHUB ACTIONS LOGS ===")
            output_lines.append(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            output_lines.append("")
            output_lines.append(f"Workflow: {latest_run['name']}")
            output_lines.append(f"Status: {latest_run['status']} ({latest_run.get('conclusion', 'N/A')})")
            output_lines.append(f"Created: {latest_run['createdAt']}")
            output_lines.append(f"Title: {latest_run['displayTitle']}")
            output_lines.append(f"URL: {latest_run['url']}")
            output_lines.append("")
            
            # Fetch detailed logs (failed steps only if failed)
            if latest_run.get('conclusion') == 'failure':
                self.app.log.info('Fetching failed step logs...')
                logs_result = subprocess.run(
                    ['gh', 'run', 'view', str(run_id),
                     '--repo', 'collective-context/ccc-code',
                     '--log-failed'],
                    capture_output=True,
                    text=True
                )
                
                if logs_result.returncode == 0 and logs_result.stdout.strip():
                    output_lines.append("--- Failed Steps ---")
                    output_lines.append(logs_result.stdout)
            
            output_text = "\n".join(output_lines)
            
            # Print to console
            print(output_text)
            
            # Save to file if --save flag
            if self.app.pargs.save:
                log_dir = "./logs"
                log_file = f"{log_dir}/ccb-debug.log"
                
                os.makedirs(log_dir, exist_ok=True)
                
                with open(log_file, 'a') as f:
                    f.write(output_text)
                    f.write("\n")
                
                self.app.log.info(f'✓ Logs appended to {log_file}')
            
        except subprocess.CalledProcessError as e:
            self.app.log.error(f'gh CLI command failed: {e}')
            self.app.log.error('Make sure gh CLI is installed and authenticated')
            self.app.log.error('Run: gh auth login')
        except json.JSONDecodeError as e:
            self.app.log.error(f'Error parsing JSON: {e}')
        except Exception as e:
            self.app.log.error(f'Error: {e}')


def load(app):
    """Load check plugin"""
    app.handler.register(CheckController)
