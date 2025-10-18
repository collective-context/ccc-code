import os
import time


from cement.core.controller import CementBaseController, expose
from ccw.core.download import WODownload
from ccw.core.logging import Log
from ccw.core.variables import WOVar


def ccw_update_hook(app):
    pass


class CCWUpdateController(CementBaseController):
    class Meta:
        label = 'ccw_update'
        stacked_on = 'base'
        aliases = ['update']
        aliases_only = True
        stacked_type =  'nested'
        description = ('update WordOps to latest version')
        arguments = [
            (['--force'],
             dict(help='Force WordOps update', action='store_true')),
            (['--beta'],
             dict(help='Update WordOps to latest mainline release '
                  '(same than --mainline)',
                  action='store_true')),
            (['--mainline'],
             dict(help='Update WordOps to latest mainline release',
                  action='store_true')),
            (['--branch'],
                dict(help="Update WordOps from a specific repository branch ",
                     action='store' or 'store_const',
                     const='develop', nargs='?')),
            (['--travis'],
             dict(help='Argument used only for WordOps development',
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

        # check if WordOps already up-to-date
        if ((not pargs.force) and (not pargs.travis) and
            (not pargs.mainline) and (not pargs.beta) and
                (not pargs.branch)):
            ccw_current = ("v{0}".format(WOVar.wo_version))
            ccw_latest = WODownload.latest_release(self, "WordOps/WordOps")
            if ccw_current == ccw_latest:
                Log.info(
                    self, "WordOps {0} is already installed"
                    .format(ccw_latest))
                self.app.close(0)

        # prompt user before starting upgrade
        if not pargs.force:
            Log.info(
                self, "WordOps changelog available on "
                "https://github.com/WordOps/WordOps/releases/tag/{0}"
                .format(ccw_latest))
            start_upgrade = input("Do you want to continue:[y/N]")
            if start_upgrade not in ("Y", "y"):
                Log.error(self, "Not starting WordOps update")

        # download the install/update script
        if not os.path.isdir('/var/lib/ccw/tmp'):
            os.makedirs('/var/lib/ccw/tmp')
        WODownload.download(self, [["https://raw.githubusercontent.com/"
                                    "WordOps/WordOps/{0}/install"
                                    .format(ccw_branch),
                                    "/var/lib/ccw/tmp/{0}".format(filename),
                                    "update script"]])

        # launch install script
        if os.path.isfile('install'):
            Log.info(self, "updating WordOps from local install\n")
            try:
                Log.info(self, "updating WordOps, please wait...")
                os.system("/bin/bash install --travis")
            except OSError as e:
                Log.debug(self, str(e))
                Log.error(self, "WordOps update failed !")
        else:
            try:
                Log.info(self, "updating WordOps, please wait...")
                os.system("/bin/bash /var/lib/ccw/tmp/{0} "
                          "{1}".format(filename, install_args))
            except OSError as e:
                Log.debug(self, str(e))
                Log.error(self, "WordOps update failed !")

        os.remove("/var/lib/ccw/tmp/{0}".format(filename))


def load(app):
    # register the plugin class.. this only happens if the plugin is enabled
    app.handler.register(CCWUpdateController)
    # register a hook (function) to run after arguments are parsed.
    app.hook.register('post_argument_parsing', ccw_update_hook)
