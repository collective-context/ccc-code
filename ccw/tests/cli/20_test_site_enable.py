from ccw.utils import test
from ccw.cli.main import CCWTestApp


class CliTestCaseSiteEnable(test.CCWTestCase):

    def test_ccw_cli_site_enable(self):
        with CCWTestApp(argv=['site', 'enable', 'html.com']) as app:
            app.run()

# Zuletzt bearbeitet: 2025-10-27
