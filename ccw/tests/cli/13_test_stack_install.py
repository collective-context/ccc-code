from ccw.utils import test
from ccw.cli.main import CCWTestApp


class CliTestCaseStackInstall(test.CCWTestCase):

    def test_ccw_cli_stack_install_nginx(self):
        with CCWTestApp(argv=['stack', 'install', '--nginx']) as app:
            app.run()

    def test_ccw_cli_stack_install_php(self):
        with CCWTestApp(argv=['stack', 'install', '--php']) as app:
            app.run()

    def test_ccw_cli_stack_install_php73(self):
        with CCWTestApp(argv=['stack', 'install', '--php73']) as app:
            app.run()

    def test_ccw_cli_stack_install_mysql(self):
        with CCWTestApp(argv=['stack', 'install', '--mysql']) as app:
            app.run()

    def test_ccw_cli_stack_install_wpcli(self):
        with CCWTestApp(argv=['stack', 'install', '--wpcli']) as app:
            app.run()

    def test_ccw_cli_stack_install_phpmyadmin(self):
        with CCWTestApp(argv=['stack', 'install', '--phpmyadmin']) as app:
            app.run()

    def test_ccw_cli_stack_install_adminer(self):
        with CCWTestApp(argv=['stack', 'install', '--adminer']) as app:
            app.run()

    def test_ccw_cli_stack_install_utils(self):
        with CCWTestApp(argv=['stack', 'install', '--utils']) as app:
            app.run()

# Zuletzt bearbeitet: 2025-10-27
