from ccw.utils import test
from ccw.cli.main import CCWTestApp


class CliTestCaseStackPurge(test.CCWTestCase):

    def test_ccw_cli_stack_purge_web(self):
        with CCWTestApp(
                argv=['stack', 'purge', '--web', '--force']) as app:
            app.run()

    def test_ccw_cli_stack_purge_admin(self):
        with CCWTestApp(
                argv=['stack', 'purge', '--admin', '--force']) as app:
            app.run()

    def test_ccw_cli_stack_purge_nginx(self):
        with CCWTestApp(
                argv=['stack', 'purge', '--nginx', '--force']) as app:
            app.run()

    def test_ccw_cli_stack_purge_php(self):
        with CCWTestApp(argv=['stack', 'purge',
                                      '--php', '--force']) as app:
            app.run()

    def test_ccw_cli_stack_purge_mysql(self):
        with CCWTestApp(argv=['stack', 'purge',
                                      '--mysql', '--force']) as app:
            app.run()

    def test_ccw_cli_stack_purge_wpcli(self):
        with CCWTestApp(argv=['stack', 'purge',
                                      '--wpcli', '--force']) as app:
            app.run()

    def test_ccw_cli_stack_purge_phpmyadmin(self):
        with CCWTestApp(
                argv=['stack', 'purge', '--phpmyadmin', '--force']) as app:
            app.run()

    def test_ccw_cli_stack_purge_adminer(self):
        with CCWTestApp(
                argv=['stack', 'purge', '--adminer', '--force']) as app:
            app.run()

    def test_ccw_cli_stack_purge_utils(self):
        with CCWTestApp(argv=['stack', 'purge',
                                      '--utils', '--force']) as app:
            app.run()

# Zuletzt bearbeitet: 2025-10-27
