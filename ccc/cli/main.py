from cement.core.foundation import CementApp
from cement.core.controller import CementBaseController, expose
from cement.ext.ext_colorlog import ColorLogHandler
from ccc.core.logging import Log
from ccc.core.variables import CCCVar
import os
import sys

# Configuration Defaults
config_defaults = {
    'ccc': {
        'debug': False,
        'plugin_dir': '/var/lib/ccc/plugins/',
        'plugin_config_dir': '/etc/ccc/plugins.d/',
        'template_dir': '/var/lib/ccc/templates/'
    },
    'log.colorlog': {
        'file': '/var/log/ccc/ccc.log',
        'level': 'debug',
        'to_console': False,
        'rotate': True,
        'max_bytes': 1000000,
        'max_files': 7,
        'colorize_file_log': True,
        'colorize_console_log': True
    }
}

class CCCBaseController(CementBaseController):
    class Meta:
        label = 'base'
        description = 'CCC CODE - Collective Context Commander for NGINX Administration'
        
    @expose(hide=True)
    def default(self):
        """Default action when no subcommand is given"""
        print("\nCCC CODE - Collective Context Commander")
        print("========================================")
        print("\nUsage: ccc [command] [options]")
        print("\nCommands:")
        print("  site      Manage NGINX sites")
        print("  stack     Manage server stacks")
        print("  clean     Clean caches")
        print("  secure    Security management")
        print("  sync      Sync configurations")
        print("\nFor more help: ccc [command] --help")

class CCCApp(CementApp):
    class Meta:
        label = 'ccc'
        base_controller = 'base'
        config_defaults = config_defaults
        log_handler = ColorLogHandler
        extensions = [
            'colorlog',
            'mustache',
        ]
        handlers = [
            CCCBaseController,
        ]
        exit_on_close = True

def main():
    with CCCApp() as app:
        # Import plugins after app initialization
        from ccc.cli.plugins.stack import CCCStackController
        from ccc.cli.plugins.site import CCCSiteController
        
        # Register handlers
        app.handler.register(CCCStackController)
        app.handler.register(CCCSiteController)
        
        try:
            app.run()
        except Exception as e:
            print(f"\nError: {e}")
            sys.exit(1)

if __name__ == '__main__':
    main()
