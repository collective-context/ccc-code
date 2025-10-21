"""Maintenance Plugin for CCC CODE"""

from cement.core.controller import CementBaseController, expose

from ccc.core.aptget import CCCAptGet
from ccc.core.logging import Log


def ccc_maintenance_hook(app):
    pass


class CCCMaintenanceController(CementBaseController):
    class Meta:
        label = 'maintenance'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = ('update server packages to latest version')
        usage = "ccc maintenance"

    @expose(hide=True)
    def default(self):

        try:
            Log.info(self, "updating apt-cache, please wait...")
            CCCAptGet.update(self)
            Log.info(self, "updating packages, please wait...")
            CCCAptGet.dist_upgrade(self)
            Log.info(self, "cleaning-up packages, please wait...")
            CCCAptGet.auto_remove(self)
            CCCAptGet.auto_clean(self)
        except OSError as e:
            Log.debug(self, str(e))
            Log.error(self, "Package updates failed !")
        except Exception as e:
            Log.debug(self, str(e))
            Log.error(self, "Packages updates failed !")


def load(app):
    # register the plugin class.. this only happens if the plugin is enabled
    app.handler.register(CCCMaintenanceController)
    # register a hook (function) to run after arguments are parsed.
    app.hook.register('post_argument_parsing', ccc_maintenance_hook)
