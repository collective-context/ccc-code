from ccw.utils import test
from ccw.cli.main import CCWTestApp


class CliTestCaseStackRestart(test.CCWTestCase):

    def test_ccw_cli_stack_services_restart_nginx(self):
        with CCWTestApp(argv=['stack', 'restart', '--nginx']) as app:
            app.run()

    def test_ccw_cli_stack_services_restart_php_fpm(self):
        with CCWTestApp(argv=['stack', 'restart', '--php']) as app:
            app.run()

    def test_ccw_cli_stack_services_restart_mysql(self):
        with CCWTestApp(argv=['stack', 'restart', '--mysql']) as app:
            app.run()

    def test_ccw_cli_stack_services_restart_all(self):
        with CCWTestApp(argv=['stack', 'restart']) as app:
            app.run()

# Zuletzt bearbeitet: 2025-10-27
