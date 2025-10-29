from ccw.utils import test
from ccw.cli.main import CCWTestApp


class CliTestCaseSiteList(test.CCWTestCase):

    def test_ccw_cli_site_list_enable(self):
        with CCWTestApp(argv=['site', 'list', '--enabled']) as app:
            app.run()

    def test_ccw_cli_site_list_disable(self):
        with CCWTestApp(argv=['site', 'list', '--disabled']) as app:
            app.run()

# Zuletzt bearbeitet: 2025-10-27
