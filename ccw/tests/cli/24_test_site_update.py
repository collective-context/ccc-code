from ccw.utils import test
from ccw.cli.main import CCWTestApp


class CliTestCaseSiteUpdate(test.CCWTestCase):

    def test_ccw_cli_site_update_html(self):
        with CCWTestApp(argv=['site', 'update', 'php.com',
                             '--html']) as app:
            app.run()

    def test_ccw_cli_site_update_php(self):
        with CCWTestApp(argv=['site', 'update', 'html.com',
                             '--php']) as app:
            app.run()

    def test_ccw_cli_site_update_mysql(self):
        with CCWTestApp(argv=['site', 'update', 'mysql.com',
                             '--html']) as app:
            app.run()

    def test_ccw_cli_site_update_wp(self):
        with CCWTestApp(argv=['site', 'update', 'mysql.com',
                             '--wp']) as app:
            app.run()

    def test_ccw_cli_site_update_wpsubdir(self):
        with CCWTestApp(argv=['site', 'update', 'wp.com',
                             '--wpsubdir']) as app:
            app.run()

    def test_ccw_cli_site_update_wpsubdomain(self):
        with CCWTestApp(argv=['site', 'update', 'wpsubdir.com',
                             '--wpsubdomain']) as app:
            app.run()

    def test_ccw_cli_site_update_wpfc(self):
        with CCWTestApp(argv=['site', 'update', 'wpsc.com',
                             '--wpfc']) as app:
            app.run()

    def test_ccw_cli_site_update_wpsc(self):
        with CCWTestApp(argv=['site', 'update', 'wpfc.com',
                             '--wpsc']) as app:
            app.run()

# Zuletzt bearbeitet: 2025-10-27
