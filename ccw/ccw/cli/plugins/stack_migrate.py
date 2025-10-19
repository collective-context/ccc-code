import os
import re
from cement.core.controller import CementBaseController, expose

from ccw.cli.plugins.stack_pref import post_pref, pre_pref
from ccw.core.aptget import CCWAptGet
from ccw.core.fileutils import CCWFileUtils
from ccw.core.logging import Log
from ccw.core.mysql import CCWMysql
from ccw.core.shellexec import CCWShellExec
from ccw.core.variables import CCWVar
from ccw.cli.plugins.sitedb import (getAllsites)
from ccw.core.template import CCWTemplate
from ccw.core.domainvalidate import CCWDomain


class CCWStackMigrateController(CementBaseController):
    class Meta:
        label = 'migrate'
        stacked_on = 'stack'
        stacked_type = 'nested'
        description = ('Migrate stack safely')
        arguments = [
            (['--mariadb'],
                dict(help="Migrate/Upgrade database to MariaDB",
                     action='store_true')),
            (['--nginx'],
                dict(help="Migrate Nginx TLS configuration to HTTP/3 QUIC",
                     action='store_true')),
            (['--force'],
                dict(help="Force Packages upgrade without any prompt",
                     action='store_true')),
            (['--ci'],
                dict(help="Argument used for testing, "
                     "do not use it on your server",
                     action='store_true')),
        ]

    @expose(hide=True)
    def migrate_mariadb(self, ci=False):

        # Backup all database
        CCWMysql.backupAll(self, fulldump=True)

        # Check current MariaDB version
        if (os.path.exists('/etc/apt/sources.list.d/ccw-repo.list') and
                CCWFileUtils.grepcheck(self, "/etc/apt/sources.list.d/ccw-repo.list", "mariadb")):
            ccw_mysql_current_repo = CCWFileUtils.grep(
                self, '/etc/apt/sources.list.d/ccw-repo.list', 'mariadb')
            repo_path = '/etc/apt/sources.list.d/ccw-repo.list'
        elif (os.path.exists('/etc/apt/sources.list.d/mariadb.list') and
              CCWFileUtils.grepcheck(self, '/etc/apt/sources.list.d/mariadb.list', "mariadb")):
            ccw_mysql_current_repo = CCWFileUtils.grep(
                self, '/etc/apt/sources.list.d/mariadb.list', 'mariadb')
            repo_path = '/etc/apt/sources.list.d/mariadb.list'

        if ccw_mysql_current_repo:
            Log.debug(self, "Looking for MariaDB version")
            pattern = r"/(\d+\.\d+)/"
            match = re.search(pattern, ccw_mysql_current_repo)
            current_mysql_version = match.group(1)
            Log.debug(self, f"Current MariaDB version is {current_mysql_version}")
        else:
            Log.error(self, "MariaDB is not installed from repository yet")

        if self.app.config.has_section('mariadb'):
            mariadb_release = self.app.config.get(
                'mariadb', 'release')
            if mariadb_release < CCWVar.mariadb_ver:
                mariadb_release = CCWVar.mariadb_ver
        else:
            mariadb_release = CCWVar.mariadb_ver
        if mariadb_release == current_mysql_version:
            Log.info(self, "You already have the latest "
                     "MariaDB version available")
            return 0

        CCWFileUtils.rm(self, repo_path)
        # Add MariaDB repo
        pre_pref(self, CCWVar.ccw_mysql)

        # Install MariaDB

        Log.wait(self, "Updating apt-cache          ")
        CCWAptGet.update(self)
        Log.valide(self, "Updating apt-cache          ")
        Log.wait(self, "Upgrading MariaDB          ")
        CCWAptGet.remove(self, ["mariadb-server"])
        CCWAptGet.auto_remove(self)
        CCWAptGet.install(self, CCWVar.ccw_mysql)
        if not ci:
            CCWAptGet.dist_upgrade(self)
        CCWAptGet.auto_remove(self)
        CCWAptGet.auto_clean(self)
        Log.valide(self, "Upgrading MariaDB          ")
        CCWFileUtils.mvfile(
            self, '/etc/mysql/my.cnf', '/etc/mysql/my.cnf.old')
        CCWFileUtils.create_symlink(
            self, ['/etc/mysql/mariadb.cnf', '/etc/mysql/my.cnf'])
        CCWShellExec.cmd_exec(self, 'systemctl daemon-reload')
        CCWShellExec.cmd_exec(self, 'systemctl enable mariadb')
        post_pref(self, CCWVar.ccw_mysql, [])

    @expose(hide=True)
    def migrate_nginx(self):

        # Add Nginx repo
        pre_pref(self, CCWVar.ccw_nginx)
        # Install Nginx
        Log.wait(self, "Updating apt-cache          ")
        CCWAptGet.update(self)
        Log.valide(self, "Updating apt-cache          ")
        Log.wait(self, "Upgrading Nginx          ")
        if CCWAptGet.install(self, CCWVar.ccw_nginx):
            Log.valide(self, "Upgrading Nginx          ")
        else:
            Log.failed(self, "Upgrading Nginx          ")
        allsites = getAllsites(self)
        for site in allsites:
            if not site:
                pass
            if os.path.exists(f'/var/www/{site.sitename}/conf/nginx/ssl.conf'):
                if not os.path.islink(f'/var/www/{site.sitename}/conf/nginx/ssl.conf'):
                    data = dict(ssl_live_path=CCWVar.ccw_ssl_live,
                                domain=site.sitename, quic=True)
                    CCWTemplate.deploy(
                        self, f'/var/www/{site.sitename}/conf/nginx/ssl.conf',
                        'ssl.mustache', data, overwrite=True)
                else:
                    (_, ccw_root_domain) = CCWDomain.getlevel(
                        self, site.sitename)
                    if (site.sitename != ccw_root_domain and
                            os.path.exists(f'/etc/letsencrypt/shared/{ccw_root_domain}.conf')):
                        data = dict(ssl_live_path=CCWVar.ccw_ssl_live,
                                    domain=ccw_root_domain, quic=True)
                        CCWTemplate.deploy(
                            self, f'/etc/letsencrypt/shared/{ccw_root_domain}.conf',
                            'ssl.mustache', data, overwrite=True)
        post_pref(self, CCWVar.ccw_nginx, [])

    @expose(hide=True)
    def default(self):
        pargs = self.app.pargs
        if not pargs.mariadb and not pargs.nginx:
            self.app.args.print_help()
        if pargs.mariadb:
            if CCWVar.ccw_distro == 'raspbian':
                Log.error(self, "MariaDB upgrade is not available on Raspbian")
            if CCWVar.ccw_mysql_host != "localhost":
                Log.error(
                    self, "Remote MySQL server in use, skipping local install")

            if CCWMysql.mariadb_ping(self):

                Log.info(self, "If your database size is big, "
                         "migration may take some time.")
                Log.info(self, "During migration non nginx-cached parts of "
                         "your site may remain down")
                if not pargs.force:
                    start_upgrade = input("Do you want to continue:[y/N]")
                    if start_upgrade != "Y" and start_upgrade != "y":
                        Log.error(self, "Not starting package update")
                if not pargs.ci:
                    self.migrate_mariadb()
                else:
                    self.migrate_mariadb(ci=True)
            else:
                Log.error(self, "Your current MySQL is not alive or "
                          "you allready installed MariaDB")
        if pargs.nginx:
            if os.path.exists('/usr/sbin/nginx'):
                self.migrate_nginx()
            else:
                Log.error(self, "Unable to connect to MariaDB")
