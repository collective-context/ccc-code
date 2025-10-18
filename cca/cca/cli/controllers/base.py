"""CCA base controller."""

from cement.core.controller import CementBaseController, expose

try:
    from cca import VERSION
except ImportError:
    VERSION = 'undefined'

VERSION_BANNER = """
CCC Alpha (cca) v%s
Copyright (c) 2025 CCC CODE
CCA is the test lab for CCC CODE development using Cement v2
""" % VERSION


class CCABaseController(CementBaseController):
    """Base controller for CCA"""
    
    class Meta:
        label = 'base'
        description = 'CCC Alpha (CCA) - Test lab for CCC CODE'
        arguments = [
            (['-v', '--version'], dict(
                action='version',
                version=VERSION_BANNER
            )),
        ]

    @expose(hide=True)
    def default(self):
        """Default action if no sub-command is passed"""
        self.app.args.print_help()

    @expose(help='Show CCA information')
    def info(self):
        """Show information about CCA"""
        print(VERSION_BANNER)
        print("\nAvailable commands:")
        print("  cca info           - Show this information")
        print("  cca check actions  - Check GitHub Actions status")
        print("  cca debug run      - Run all tests and collect logs")
        print("  cca debug summary  - Show test summary from logs")
        print("\nUse 'cca <command> --help' for more information")
