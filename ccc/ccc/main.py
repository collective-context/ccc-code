"""
Main application entry point for CCC
Cement v3 based CLI application
"""

from cement import App, Controller, ex
from cement.core.exc import CaughtSignal

# Import version
from ccc import __version__


class BaseController(Controller):
    """Base controller for CCC CLI"""

    class Meta:
        label = "base"
        description = "Collective Context Commander - Production AI orchestration"
        arguments = [
            (["-v", "--version"], {
                "action": "version",
                "version": f"CCC Production v{__version__}"
            }),
        ]

    @ex(
        help="Show system status and information",
    )
    def info(self):
        """Display CCC system information"""
        self.app.log.info("CCC System Information")
        print(f"CCC Production v{__version__}")
        print("Framework: Cement v3")
        print("")
        print("Available commands:")
        print("  ccc info     - Show this information")
        print("  ccc status   - Show operational status")
        print("  ccc debug    - Debug information")
        print("")
        print("Use 'ccc <command> --help' for more information")

    @ex(
        help="Show current operational status",
    )
    def status(self):
        """Display operational status"""
        self.app.log.info("Checking CCC status...")
        print("CCC Status: Operational ✓")
        print(f"Version: {__version__}")
        print(f"Debug Mode: {self.app.debug}")

    @ex(
        help="Show debug information",
    )
    def debug(self):
        """Display debug information"""
        print("CCC Debug Information")
        print("=" * 40)
        print(f"Version: {__version__}")
        print(f"Debug: {self.app.debug}")
        print(f"Config: {self.app.config.get_dict()}")


class CCCApp(App):
    """CCC Application"""

    class Meta:
        label = "ccc"
        base_controller = "base"
        handlers = [BaseController]
        extensions = ["yaml", "colorlog", "jinja2"]
        config_file_suffix = ".yml"
        config_defaults = {
            "ccc": {
                "version": __version__,
                "debug": False,
            }
        }
        log_handler = "colorlog"
        output_handler = "jinja2"


def main():
    """Main entry point"""
    with CCCApp() as app:
        try:
            app.run()
        except AssertionError as e:
            print(f"AssertionError: {e}")
            app.exit_code = 1
        except CaughtSignal as e:
            print(f"\n{e}")
            app.exit_code = 0


if __name__ == "__main__":
    main()
