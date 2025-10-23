"""CCC CODE main application entry point."""
import sys
from os import geteuid

from cement.core.exc import CaughtSignal, FrameworkError
from cement.core.foundation import CementApp
from cement.ext.ext_argparse import ArgParseArgumentHandler
from cement.utils.misc import init_defaults

from ccc.core import exc

# Application default.  Should update config/ccc.conf to reflect any
# changes, or additions here.
defaults = init_defaults('ccc')

# All internal/external plugin configurations are loaded from here
defaults['ccc']['plugin_config_dir'] = '/etc/ccc/plugins.d'

# External plugins (generally, do not ship with application code)
defaults['ccc']['plugin_dir'] = '/var/lib/ccc/plugins'

# External templates (generally, do not ship with application code)
defaults['ccc']['template_dir'] = '/var/lib/ccc/templates'


def encode_output(app, text):
    """ Encode the output to be suitable for the terminal

    :param app: The Cement App (unused)
    :param text: The rendered text
    :return: The encoded text
    """

    return text.encode("utf-8")


class CCCArgHandler(ArgParseArgumentHandler):
    class Meta:
        label = 'ccc_args_handler'

    def error(self, message):
        super(CCCArgHandler, self).error("unknown args")


class CCCApp(CementApp):
    class Meta:
        label = 'ccc'

        config_defaults = defaults

        # All built-in application bootstrapping (always run)
        bootstrap = 'ccc.cli.bootstrap'

        # Internal plugins (ship with application code)
        plugin_bootstrap = 'ccc.cli.plugins'

        # Internal templates (ship with application code)
        template_module = 'ccc.cli.templates'

        extensions = ['mustache', 'argcomplete', 'colorlog']

        hooks = [
            ("post_render", encode_output)
        ]

        output_handler = 'mustache'

        log_handler = 'colorlog'

        arg_handler = CCCArgHandler
        exit_on_close = True


class CCCTestApp(CCCApp):
    """A test app that is better suited for testing."""
    class Meta:
        # default argv to empty (don't use sys.argv)
        argv = []

        # don't look for config files (could break tests)
        config_files = []

        # don't call sys.exit() when app.close() is called in tests
        exit_on_close = False


# Define the applicaiton object outside of main, as some libraries might wish
# to import it as a global (rather than passing it into another class/func)
app = CCCApp()


def main():
    with app:
        try:
            global sys

            # if not root...kick out
            if not geteuid() == 0:
                print("\nNon-privileged users cant use CCC CODE. "
                      "Switch to root or invoke sudo.\n")
                app.close(1)
            app.run()
        except AssertionError as e:
            print("AssertionError => %s" % e.args[0])
            app.exit_code = 1
        except exc.CCCError as e:
            # Catch our application errors and exit 1 (error)
            print('CCCError > %s' % e)
            app.exit_code = 1
        except CaughtSignal as e:
            # Default Cement signals are SIGINT and SIGTERM, exit 0 (non-error)
            print('CaughtSignal > %s' % e)
            app.exit_code = 0
        except FrameworkError as e:
            # Catch framework errors and exit 1 (error)
            print('FrameworkError > %s' % e)
            app.exit_code = 1
        finally:
            # Maybe we want to see a full-stack trace for the above
            # exceptions, but only if --debug was passed?
            if app.debug:
                import traceback
                traceback.print_exc()


if __name__ == '__main__':
    main()
