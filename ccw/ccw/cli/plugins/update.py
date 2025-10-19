import os
import time


from cement.core.controller import CementBaseController, expose
from ccw.core.download import CCWDownload
from ccw.core.logging import Log
from ccw.core.variables import CCWVar


def ccw_update_hook(app):
    pass


class CCWUpdateController(CementBaseController):
    class Meta:
        label = 'ccw_update'
        stacked_on = 'base'
        aliases = ['update']
        aliases_only = True
        stacked_type = 'nested'
        description = ('update CCC CODE to latest version')
        arguments = [
            (['--force'],
             dict(help='Force CCC CODE update', action='store_true')),
            (['--beta'],
             dict(help='Update CCC CODE to latest mainline release '
                  '(same than --mainline)',
                  action='store_true')),
            (['--mainline'],
             dict(help='Update CCC CODE to latest mainline release',
                  action='store_true')),
            (['--branch'],
                dict(help="Update CCC CODE from a specific repository branch ",
                     action='store' or 'store_const',
                     const='develop', nargs='?')),
            (['--travis'],
             dict(help='Argument used only for CCC CODE development',
                  action='store_true')),
        ]
        usage = "ccw update [options]"

    @expose(hide=True)
    def default(self):
        pargs = self.app.pargs
        filename = "ccwupdate" + time.strftime("%Y%m%d-%H%M%S")

        install_args = ""
        ccw_branch = "master"
        if pargs.mainline or pargs.beta:
            ccw_branch = "mainline"
            install_args = install_args + "--mainline "
        elif pargs.branch:
            ccw_branch = pargs.branch
            install_args = install_args + "-b {0} ".format(ccw_branch)
        if pargs.force:
            install_args = install_args + "--force "
        if pargs.travis:
            install_args = install_args + "--travis "
            ccw_branch = "updating-configuration"

        # check if CCC CODE already up-to-date
        if ((not pargs.force) and (not pargs.travis) and
            (not pargs.mainline) and (not pargs.beta) and
                (not pargs.branch)):
            ccw_current = ("v{0}".format(CCWVar.ccw_version))
            ccw_latest = CCWDownload.latest_release(self, "collective-context/ccc-code")
            if ccw_current == ccw_latest:
                Log.info(
                    self, "CCC CODE {0} is already installed"
                    .format(ccw_latest))
                self.app.close(0)

        # prompt user before starting upgrade
        if not pargs.force:
            Log.info(
                self, "CCC CODE changelog available on "
                "https://github.com/collective-context/ccc-code/releases/tag/{0}"
                .format(ccw_latest))
            start_upgrade = input("Do you want to continue:[y/N]")
            if start_upgrade not in ("Y", "y"):
                Log.error(self, "Not starting CCC CODE update")

        # download the install/update script
        if not os.path.isdir('/var/lib/ccw/tmp'):
            os.makedirs('/var/lib/ccw/tmp')
        CCWDownload.download(self, [["https://raw.githubusercontent.com/"
                                    "collective-context/ccc-code/{0}/install"
                                    .format(ccw_branch),
                                    "/var/lib/ccw/tmp/{0}".format(filename),
                                    "update script"]])

        # launch install script
        if os.path.isfile('install'):
            Log.info(self, "updating CCC CODE from local install\n")
            try:
                Log.info(self, "updating CCC CODE, please wait...")
                os.system("/bin/bash install --travis")
            except OSError as e:
                Log.debug(self, str(e))
                Log.error(self, "CCC CODE update failed !")
        else:
            try:
                Log.info(self, "updating CCC CODE, please wait...")
                os.system("/bin/bash /var/lib/ccw/tmp/{0} "
                          "{1}".format(filename, install_args))
            except OSError as e:
                Log.debug(self, str(e))
                Log.error(self, "CCC CODE update failed !")

        os.remove("/var/lib/ccw/tmp/{0}".format(filename))


def load(app):
    # register the plugin class.. this only happens if the plugin is enabled
    app.handler.register(CCWUpdateController)
    # register a hook (function) to run after arguments are parsed.
    app.hook.register('post_argument_parsing', ccw_update_hook)
