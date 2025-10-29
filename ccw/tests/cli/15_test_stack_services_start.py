from ccw.utils import test
from ccw.cli.main import CCWTestApp


class CliTestCaseStackStart(test.CCWTestCase):

    def test_ccw_cli_stack_services_start_nginx(self):
        with CCWTestApp(argv=['stack', 'start', '--nginx']) as app:
            app.run()

    def test_ccw_cli_stack_services_start_php_fpm(self):
        with CCWTestApp(argv=['stack', 'start', '--php']) as app:
            app.run()

    def test_ccw_cli_stack_services_start_mysql(self):
        with CCWTestApp(argv=['stack', 'start', '--mysql']) as app:
            app.run()

    def test_ccw_cli_stack_services_start_all(self):
        with CCWTestApp(argv=['stack', 'start']) as app:
            app.run()

# Zuletzt bearbeitet: 2025-10-27
