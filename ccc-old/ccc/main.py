"""
Main application entry point for CCC
Cement v3 based CLI application
"""

from cement import App, Controller, ex
from cement.core.exc import CaughtSignal


class BaseController(Controller):
    """Base controller for CCC CLI"""

    class Meta:
        label = "base"
        description = "Collective Context Commander - AI orchestration tool"
        arguments = [
            (["-v", "--version"], {"action": "version", "version": "CCC 1.0.0"}),
        ]

    @ex(
        help="Show current status",
    )
    def status(self):
        """Display system status"""
        self.app.log.info("Checking CCC status...")
        print("CCC Status: Operational ✓")
        print(f"Version: {self.app.config.get('ccc', 'version')}")


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
                "version": "1.0.0",
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
