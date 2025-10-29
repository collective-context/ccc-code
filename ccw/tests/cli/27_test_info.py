from ccw.utils import test
from ccw.cli.main import CCWTestApp


class CliTestCaseInfo(test.CCWTestCase):

    def test_ccw_cli_info_mysql(self):
        with CCWTestApp(argv=['info', '--mysql']) as app:
            app.run()

    def test_ccw_cli_info_php(self):
        with CCWTestApp(argv=['info', '--php']) as app:
            app.run()

    def test_ccw_cli_info_nginx(self):
        with CCWTestApp(argv=['info', '--nginx']) as app:
            app.run()

# Zuletzt bearbeitet: 2025-10-27
