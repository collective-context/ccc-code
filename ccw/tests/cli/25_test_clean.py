from ccw.utils import test
from ccw.cli.main import CCWTestApp


class CliTestCaseClean(test.CCWTestCase):

    def test_ccw_cli_clean(self):
        with CCWTestApp(argv=['clean']) as app:
            app.run()

    def test_ccw_cli_clean_fastcgi(self):
        with CCWTestApp(argv=['clean', '--fastcgi']) as app:
            app.run()

    def test_ccw_cli_clean_all(self):
        with CCWTestApp(argv=['clean', '--all']) as app:
            app.run()

    def test_ccw_cli_clean_opcache(self):
        with CCWTestApp(argv=['clean', '--opcache']) as app:
            app.run()

    def test_ccw_cli_clean_redis(self):
        with CCWTestApp(argv=['clean', '--redis']) as app:
            app.run()

# Zuletzt bearbeitet: 2025-10-27
