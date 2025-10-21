"""WordPress utilities for CCC CODE"""
from ccc.core.logging import Log
from ccc.core.shellexec import CCCShellExec
from ccc.core.variables import CCCVar


class CCCWp:
    """WordPress utilities for CCC CODE"""

    def wpcli(self, command):
        """WP-CLI wrapper"""
        try:
            CCCShellExec.cmd_exec(
                self, '{0} --allow-root '.format(CCCVar.ccc_wpcli_path) +
                '{0}'.format(command))
        except Exception:
            Log.error(self, "WP-CLI command failed")
