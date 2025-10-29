from ccw.utils import test
from ccw.cli.main import CCWTestApp


class CliTestCaseStackStatus(test.CCWTestCase):

    def test_ccw_cli_stack_services_status_nginx(self):
        with CCWTestApp(argv=['stack', 'status', '--nginx']) as app:
            app.run()

    def test_ccw_cli_stack_services_status_php_fpm(self):
        with CCWTestApp(argv=['stack', 'status', '--php']) as app:
            app.run()

    def test_ccw_cli_stack_services_status_mysql(self):
        with CCWTestApp(argv=['stack', 'status', '--mysql']) as app:
            app.run()

    def test_ccw_cli_stack_services_status_all(self):
        with CCWTestApp(argv=['stack', 'status']) as app:
            app.run()

# Zuletzt bearbeitet: 2025-10-27
