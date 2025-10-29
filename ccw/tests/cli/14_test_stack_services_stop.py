from ccw.utils import test
from ccw.cli.main import CCWTestApp


class CliTestCaseStackStop(test.CCWTestCase):

    def test_ccw_cli_stack_services_stop_nginx(self):
        with CCWTestApp(argv=['stack', 'stop', '--nginx']) as app:
            app.run()

    def test_ccw_cli_stack_services_stop_php_fpm(self):
        with CCWTestApp(argv=['stack', 'stop', '--php']) as app:
            app.run()

    def test_ccw_cli_stack_services_stop_mysql(self):
        with CCWTestApp(argv=['stack', 'stop', '--mysql']) as app:
            app.run()

    def test_ccw_cli_stack_services_stop_all(self):
        with CCWTestApp(argv=['stack', 'stop']) as app:
            app.run()

# Zuletzt bearbeitet: 2025-10-27
