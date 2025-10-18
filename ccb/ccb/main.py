"""Main application entry point"""
from cement import App, Controller, ex
from ccb.core.version import get_version

VERSION_BANNER = """
CCC Beta (ccb) v%s
Experimental tools for CCC CODE development
https://collective-context.org
""" % get_version()


class Base(Controller):
    """Base controller for ccb"""
    
    class Meta:
        label = 'base'
        description = 'CCC Beta - Experimental CCC CODE Tools'
        arguments = [
            (['-v', '--version'], {
                'action': 'version',
                'version': VERSION_BANNER
            }),
        ]
    
    def _default(self):
        """Default command (shows help)"""
        self.app.args.print_help()
    
    @ex(
        help='show ccb version and info',
        description='Display version and available commands'
    )
    def info(self):
        """Display ccb version information"""
        print(f'CCC Beta (ccb) v{get_version()}')
        print('Experimental tools for CCC CODE development')
        print('')
        print('Available commands:')
        print('  ccb info              - Show this information')
        print('  ccb check actions     - Fetch GitHub Actions logs')
        print('  ccb debug run         - Run all tests and aggregate logs')
        print('  ccb debug summary     - Show debug log summary')
        print('  ccb --help            - Display help')
        print('  ccb --version         - Display version')


class CCB(App):
    """CCC Beta application"""
    
    class Meta:
        label = 'ccb'
        
        # Handlers
        handlers = [
            Base
        ]
        
        # Extensions
        extensions = ['colorlog']
        
        # Logging
        log_handler = 'colorlog'
        
        # Plugin directories (für Phase 4)
        plugin_dirs = ['ccb/plugins']


def main():
    """Main entry point"""
    with CCB() as app:
        # Load plugins
        from ccb.plugins import load_plugins
        load_plugins(app)
        
        try:
            app.run()
        except AssertionError as e:
            print(f'AssertionError: {e}')
            app.exit_code = 1
        except KeyboardInterrupt:
            print('\nInterrupted')
            app.exit_code = 130


if __name__ == '__main__':
    main()
