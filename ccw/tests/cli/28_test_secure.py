from ccw.utils import test
from ccw.cli.main import CCWTestApp


class CliTestCaseSecure(test.CCWTestCase):

    def test_ccw_cli_secure_auth(self):
        with CCWTestApp(argv=['secure', '--auth', 'abc', 'superpass']) as app:
            app.run()

    def test_ccw_cli_secure_port(self):
        with CCWTestApp(argv=['secure', '--port', '22222']) as app:
            app.run()

    def test_ccw_cli_secure_ip(self):
        with CCWTestApp(argv=['secure', '--ip', '172.16.0.1']) as app:
            app.run()

# Zuletzt bearbeitet: 2025-10-27
