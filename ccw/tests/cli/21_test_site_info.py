from ccw.utils import test
from ccw.cli.main import CCWTestApp


class CliTestCaseSiteInfo(test.CCWTestCase):

    def test_ccw_cli_site_info(self):
        with CCWTestApp(argv=['site', 'info', 'html.com']) as app:
            app.run()

# Zuletzt bearbeitet: 2025-10-27
