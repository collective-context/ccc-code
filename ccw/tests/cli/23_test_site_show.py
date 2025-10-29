from ccw.utils import test
from ccw.cli.main import CCWTestApp


class CliTestCaseSiteShow(test.CCWTestCase):

    def test_ccw_cli_show_edit(self):
        with CCWTestApp(argv=['site', 'show', 'html.com']) as app:
            app.run()

# Zuletzt bearbeitet: 2025-10-27
