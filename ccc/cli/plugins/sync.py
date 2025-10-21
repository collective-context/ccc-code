import glob
import os

from cement.core.controller import CementBaseController, expose

from ccc.cli.plugins.sitedb import getAllsites, updateSiteInfo
from ccc.core.fileutils import CCCFileUtils
from ccc.core.logging import Log
from ccc.core.mysql import StatementExcecutionError, CCCMysql


def ccc_sync_hook(app):
    pass


class CCCSyncController(CementBaseController):
    class Meta:
        label = 'sync'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = 'synchronize the CCC CODE database'

    @expose(hide=True)
    def default(self):
        self.sync()

    @expose(hide=True)
    def sync(self):
        """
        1. reads database information from wp/ccc-config.php
        2. updates records into ccc database accordingly.
        """
        Log.info(self, "Synchronizing ccc database, please wait...")
        sites = getAllsites(self)
        if not sites:
            pass
        for site in sites:
            if site.site_type in ['mysql', 'wp', 'wpsubdir', 'wpsubdomain']:
                ccc_site_webroot = site.site_path
                # Read config files
                configfiles = glob.glob(ccc_site_webroot + '/*-config.php')

                if (os.path.exists(
                    '{0}/ee-config.php'.format(ccc_site_webroot)) and
                    os.path.exists(
                        '{0}/ccc-config.php'.format(ccc_site_webroot))):
                    configfiles = glob.glob(
                        ccc_site_webroot + 'ccc-config.php')

                # search for wp-config.php inside htdocs/
                if not configfiles:
                    Log.debug(self, "Config files not found in {0}/ "
                                    .format(ccc_site_webroot))
                    if site.site_type != 'mysql':
                        Log.debug(self,
                                  "Searching wp-config.php in {0}/htdocs/"
                                  .format(ccc_site_webroot))
                        configfiles = glob.glob(
                            ccc_site_webroot + '/htdocs/wp-config.php')

                if configfiles:
                    if CCCFileUtils.isexist(self, configfiles[0]):
                        ccc_db_name = (
                            CCCFileUtils.grep(self, configfiles[0],
                                             'DB_NAME').split(',')[1]
                            .split(')')[0].strip().replace('\'', ''))
                        ccc_db_user = (
                            CCCFileUtils.grep(self, configfiles[0],
                                             'DB_USER').split(',')[1]
                            .split(')')[0].strip().replace('\'', ''))
                        ccc_db_pass = (
                            CCCFileUtils.grep(self, configfiles[0],
                                             'DB_PASSWORD').split(',')[1]
                            .split(')')[0].strip().replace('\'', ''))
                        ccc_db_host = (
                            CCCFileUtils.grep(self, configfiles[0],
                                             'DB_HOST').split(',')[1]
                            .split(')')[0].strip().replace('\'', ''))

                        # Check if database really exist
                        try:
                            if not CCCMysql.check_db_exists(self, ccc_db_name):
                                # Mark it as deleted if not exist
                                ccc_db_name = 'deleted'
                                ccc_db_user = 'deleted'
                                ccc_db_pass = 'deleted'
                        except StatementExcecutionError as e:
                            Log.debug(self, str(e))
                        except Exception as e:
                            Log.debug(self, str(e))

                        if site.db_name != ccc_db_name:
                            # update records if any mismatch found
                            Log.debug(self, "Updating ccc db record for {0}"
                                      .format(site.sitename))
                            updateSiteInfo(self, site.sitename,
                                           db_name=ccc_db_name,
                                           db_user=ccc_db_user,
                                           db_password=ccc_db_pass,
                                           db_host=ccc_db_host)
                else:
                    Log.debug(self, "Config files not found for {0} "
                              .format(site.sitename))


def load(app):
    # register the plugin class.. this only happens if the plugin is enabled
    app.handler.register(CCCSyncController)
    # register a hook (function) to run after arguments are parsed.
    app.hook.register('post_argument_parsing', ccc_sync_hook)
