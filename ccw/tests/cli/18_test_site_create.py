from ccw.utils import test
from ccw.cli.main import CCWTestApp


class CliTestCaseSiteCreate(test.CCWTestCase):

    def test_ccw_cli_site_create_html(self):
        with CCWTestApp(argv=['site', 'create', 'html.com',
                             '--html']) as app:
            app.config.set('ccw', '', True)
            app.run()

    def test_ccw_cli_site_create_php(self):
        with CCWTestApp(argv=['site', 'create', 'php.com',
                             '--php']) as app:
            app.run()

    def test_ccw_cli_site_create_mysql(self):
        with CCWTestApp(argv=['site', 'create', 'mysql.com',
                             '--mysql']) as app:
            app.run()

    def test_ccw_cli_site_create_wp(self):
        with CCWTestApp(argv=['site', 'create', 'wp.com',
                             '--wp']) as app:
            app.run()

    def test_ccw_cli_site_create_wpsubdir(self):
        with CCWTestApp(argv=['site', 'create', 'wpsubdir.com',
                             '--wpsubdir']) as app:
            app.run()

    def test_ccw_cli_site_create_wpsubdomain(self):
        with CCWTestApp(argv=['site', 'create', 'wpsubdomain.com',
                             '--wpsubdomain']) as app:
            app.run()

    def test_ccw_cli_site_create_wpfc(self):
        with CCWTestApp(argv=['site', 'create', 'wpfc.com',
                             '--wpfc']) as app:
            app.run()

    def test_ccw_cli_site_create_wpsc(self):
        with CCWTestApp(argv=['site', 'create', 'wpsc.com',
                             '--wpsc']) as app:
            app.run()

    def test_ccw_cli_site_create_wpce(self):
        with CCWTestApp(argv=['site', 'create', 'wpce.com',
                             '--wpce']) as app:
            app.run()

    def test_ccw_cli_site_create_wprocket(self):
        with CCWTestApp(argv=['site', 'create', 'wprocket.com',
                             '--wprocket']) as app:
            app.run()

# Zuletzt bearbeitet: 2025-10-27
