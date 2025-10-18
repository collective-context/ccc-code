import glob
import os

from cement.core.controller import CementBaseController, expose

from ccw.cli.plugins.sitedb import getAllsites, updateSiteInfo
from ccw.core.fileutils import WOFileUtils
from ccw.core.logging import Log
from ccw.core.mysql import StatementExcecutionError, WOMysql


def ccw_sync_hook(app):
    pass


class CCWSyncController(CementBaseController):
    class Meta:
        label = 'sync'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = 'synchronize the WordOps database'

    @expose(hide=True)
    def default(self):
        self.sync()

    @expose(hide=True)
    def sync(self):
        """
        1. reads database information from wp/ccw-config.php
        2. updates records into ccw database accordingly.
        """
        Log.info(self, "Synchronizing ccw database, please wait...")
        sites = getAllsites(self)
        if not sites:
            pass
        for site in sites:
            if site.site_type in ['mysql', 'wp', 'wpsubdir', 'wpsubdomain']:
                ccw_site_webroot = site.site_path
                # Read config files
                configfiles = glob.glob(ccw_site_webroot + '/*-config.php')

                if (os.path.exists(
                    '{0}/ee-config.php'.format(ccw_site_webroot)) and
                    os.path.exists(
                        '{0}/ccw-config.php'.format(ccw_site_webroot))):
                    configfiles = glob.glob(
                        ccw_site_webroot + 'ccw-config.php')

                # search for wp-config.php inside htdocs/
                if not configfiles:
                    Log.debug(self, "Config files not found in {0}/ "
                                    .format(ccw_site_webroot))
                    if site.site_type != 'mysql':
                        Log.debug(self,
                                  "Searching wp-config.php in {0}/htdocs/"
                                  .format(ccw_site_webroot))
                        configfiles = glob.glob(
                            ccw_site_webroot + '/htdocs/wp-config.php')

                if configfiles:
                    if WOFileUtils.isexist(self, configfiles[0]):
                        ccw_db_name = (
                            WOFileUtils.grep(self, configfiles[0],
                                             'DB_NAME').split(',')[1]
                            .split(')')[0].strip().replace('\'', ''))
                        ccw_db_user = (
                            WOFileUtils.grep(self, configfiles[0],
                                             'DB_USER').split(',')[1]
                            .split(')')[0].strip().replace('\'', ''))
                        ccw_db_pass = (
                            WOFileUtils.grep(self, configfiles[0],
                                             'DB_PASSWORD').split(',')[1]
                            .split(')')[0].strip().replace('\'', ''))
                        ccw_db_host = (
                            WOFileUtils.grep(self, configfiles[0],
                                             'DB_HOST').split(',')[1]
                            .split(')')[0].strip().replace('\'', ''))

                        # Check if database really exist
                        try:
                            if not WOMysql.check_db_exists(self, ccw_db_name):
                                # Mark it as deleted if not exist
                                ccw_db_name = 'deleted'
                                ccw_db_user = 'deleted'
                                ccw_db_pass = 'deleted'
                        except StatementExcecutionError as e:
                            Log.debug(self, str(e))
                        except Exception as e:
                            Log.debug(self, str(e))

                        if site.db_name != ccw_db_name:
                            # update records if any mismatch found
                            Log.debug(self, "Updating ccw db record for {0}"
                                      .format(site.sitename))
                            updateSiteInfo(self, site.sitename,
                                           db_name=ccw_db_name,
                                           db_user=ccw_db_user,
                                           db_password=ccw_db_pass,
                                           db_host=ccw_db_host)
                else:
                    Log.debug(self, "Config files not found for {0} "
                              .format(site.sitename))


def load(app):
    # register the plugin class.. this only happens if the plugin is enabled
    app.handler.register(CCWSyncController)
    # register a hook (function) to run after arguments are parsed.
    app.hook.register('post_argument_parsing', ccw_sync_hook)
