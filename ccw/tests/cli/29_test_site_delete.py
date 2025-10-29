from ccw.utils import test
from ccw.cli.main import CCWTestApp


class CliTestCaseSiteDelete(test.CCWTestCase):

    def test_ccw_cli_site_detele(self):
        with CCWTestApp(argv=['site', 'delete', 'html.com',
                             '--force']) as app:
            app.run()

    def test_ccw_cli_site_detele_all(self):
        with CCWTestApp(argv=['site', 'delete', 'wp.com',
                             '--all', '--force']) as app:
            app.run()

    def test_ccw_cli_site_detele_db(self):
        with CCWTestApp(argv=['site', 'delete', 'mysql.com',
                             '--db', '--force']) as app:
            app.run()

    def test_ccw_cli_site_detele_files(self):
        with CCWTestApp(argv=['site', 'delete', 'php.com',
                             '--files', '--force']) as app:
            app.run()

# Zuletzt bearbeitet: 2025-10-27
