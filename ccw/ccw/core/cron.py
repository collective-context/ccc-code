from ccw.core.logging import Log
from ccw.core.shellexec import CCWShellExec
"""
Set CRON on LINUX system.
"""


class CCWCron():
    def setcron_weekly(self, cmd, comment='Cron set by CCC CODE', user='root',
                       min=0, hour=12):
        if not CCWShellExec.cmd_exec(self, "crontab -l "
                                    "| grep -q \'{0}\'".format(cmd)):

            CCWShellExec.cmd_exec(self, "/bin/bash -c \"crontab -l 2> /dev/null | {{ cat; echo -e \\\"\\n0 0 * * 0 {0} # {1}\\\"; }} | crontab -\"".format(cmd, comment))
            Log.debug(self, "Cron set")

    def setcron_daily(self, cmd, comment='Cron set by CCC CODE', user='root',
                      min=0, hour=12):
        if not CCWShellExec.cmd_exec(self, "crontab -l "
                                    "| grep -q \'{0}\'".format(cmd)):

            CCWShellExec.cmd_exec(self, "/bin/bash -c \"crontab -l 2> /dev/null | {{ cat; echo -e \\\"\\n@daily {0} # {1}\\\"; }} | crontab -\"".format(cmd, comment))
            Log.debug(self, "Cron set")

    def remove_cron(self, cmd):
        if CCWShellExec.cmd_exec(self, "crontab -l "
                                "| grep -q \'{0}\'".format(cmd)):
            if not CCWShellExec.cmd_exec(self, "/bin/bash -c "
                                        "\"crontab "
                                        "-l | sed '/{0}/d'"
                                        "| crontab -\""
                                        .format(cmd)):
                Log.error(self, "Failed to remove crontab entry", False)
        else:
            Log.debug(self, "Cron not found")

# Zuletzt bearbeitet: 2025-10-27
