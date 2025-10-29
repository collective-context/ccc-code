from ccw.utils import test
from ccw.cli.main import CCWTestApp


class CliTestCaseStackRemove(test.CCWTestCase):

    def test_ccw_cli_stack_remove_admin(self):
        with CCWTestApp(argv=['stack', 'remove', '--admin', '--force']) as app:
            app.run()

    def test_ccw_cli_stack_remove_nginx(self):
        with CCWTestApp(argv=['stack', 'remove', '--nginx', '--force']) as app:
            app.run()

    def test_ccw_cli_stack_remove_php(self):
        with CCWTestApp(argv=['stack', 'remove', '--php', '--force']) as app:
            app.run()

    def test_ccw_cli_stack_remove_mysql(self):
        with CCWTestApp(argv=['stack', 'remove', '--mysql', '--force']) as app:
            app.run()

    def test_ccw_cli_stack_remove_wpcli(self):
        with CCWTestApp(argv=['stack', 'remove', '--wpcli', '--force']) as app:
            app.run()

    def test_ccw_cli_stack_remove_phpmyadmin(self):
        with CCWTestApp(argv=['stack', 'remove',
                                      '--phpmyadmin', '--force']) as app:
            app.run()

    def test_ccw_cli_stack_remove_adminer(self):
        with CCWTestApp(
                argv=['stack', 'remove', '--adminer', '--force']) as app:
            app.run()

    def test_ccw_cli_stack_remove_utils(self):
        with CCWTestApp(argv=['stack', 'remove', '--utils', '--force']) as app:
            app.run()

# Zuletzt bearbeitet: 2025-10-27
