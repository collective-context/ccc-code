"""WordPress utilities for CCC CODE"""
from ccw.core.logging import Log
from ccw.core.shellexec import CCWShellExec
from ccw.core.variables import CCWVar


class CCWWp:
    """WordPress utilities for CCC CODE"""

    def wpcli(self, command):
        """WP-CLI wrapper"""
        try:
            CCWShellExec.cmd_exec(
                self, '{0} --allow-root '.format(CCWVar.ccw_wpcli_path) +
                '{0}'.format(command))
        except Exception:
            Log.error(self, "WP-CLI command failed")

# Zuletzt bearbeitet: 2025-10-27
