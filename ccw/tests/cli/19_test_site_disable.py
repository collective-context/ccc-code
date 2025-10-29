from ccw.utils import test
from ccw.cli.main import CCWTestApp


class CliTestCaseSiteDisable(test.CCWTestCase):

    def test_ccw_cli_site_disable(self):
        with CCWTestApp(argv=['site', 'disable', 'html.com']) as app:
            app.run()

# Zuletzt bearbeitet: 2025-10-27
