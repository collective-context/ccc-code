#!/usr/bin/env python3
"""Main application entry point for CCA"""

import sys
from cement.core.foundation import CementApp
from cement.core.exc import CaughtSignal, FrameworkError
from cement.utils.misc import init_defaults

try:
    from cca import VERSION
except ImportError:
    VERSION = 'undefined'

# Defaults wie WordOps
defaults = init_defaults('cca')
defaults['cca']['plugin_config_dir'] = '/etc/cca/plugins.d'


class CCAApp(CementApp):
    """CCA application class"""
    
    class Meta:
        label = 'cca'
        
        # Config defaults
        config_defaults = defaults
        
        # WICHTIG: Cement v2 Bootstrap-Pattern wie WordOps
        bootstrap = 'cca.cli.bootstrap'           # Lädt Base Controller
        plugin_bootstrap = 'cca.cli.plugins'      # Lädt Plugins


def main():
    """Main entry point"""
    with CCAApp() as app:
        try:
            app.setup()
            app.run()
        except AssertionError as e:
            print('AssertionError > %s' % e.args[0])
            sys.exit(1)
        except CaughtSignal as e:
            sys.exit(e.code)
        except FrameworkError as e:
            print('FrameworkError > %s' % e.args[0])
            sys.exit(1)


if __name__ == '__main__':
    main()
