import os

from cement.core.controller import CementBaseController, expose
from ccw.cli.plugins.site_functions import (
    detSitePar, check_domain_exists, site_package_check,
    pre_run_checks, setupdomain, SiteError,
    doCleanupAction, setupdatabase, setupwordpress, setwebrootpermissions,
    display_cache_settings, copyWildcardCert)
from ccw.cli.plugins.sitedb import (deleteSiteInfo, getAllsites,
                                   getSiteInfo, updateSiteInfo)
from ccw.core.acme import CCWAcme
from ccw.core.domainvalidate import CCWDomain
from ccw.core.git import CCWGit
from ccw.core.logging import Log
from ccw.core.nginxhashbucket import hashbucket
from ccw.core.services import CCWService
from ccw.core.sslutils import SSL
from ccw.core.variables import CCWVar


class CCWSiteBackupController(CementBaseController):
    class Meta:
        label = 'backup'
        stacked_on = 'site'
        stacked_type = 'nested'
        description = ('this commands allow you to backup your sites')
        arguments = [
            (['site_name'],
                dict(help='domain name for the site to be cloned.',
                     nargs='?')),
            (['--db'],
                dict(help="backup only site database", action='store_true')),
            (['--files'],
                dict(help="backup only site files", action='store_true')),
            (['--all'],
                dict(help="backup all sites", action='store_true')),
        ]

    @expose(hide=True)
    def default(self):
        pargs = self.app.pargs
        # self.app.render((data), 'default.mustache')
        # Check domain name validation
        data = dict()
        sites = getAllsites(self)

        if not pargs.site_name and not pargs.all:
            try:
                while not pargs.site_name:
                    # preprocessing before finalize site name
                    pargs.site_name = (input('Enter site name : ')
                                       .strip())
            except IOError as e:
                Log.debug(self, str(e))
                Log.error(self, "Unable to input site name, Please try again!")

        pargs.site_name = pargs.site_name.strip()
        ccw_domain = CCWDomain.validate(self, pargs.site_name)
        ccw_www_domain = "www.{0}".format(ccw_domain)
        (ccw_domain_type, ccw_root_domain) = CCWDomain.getlevel(
            self, ccw_domain)
        if not ccw_domain.strip():
            Log.error(self, "Invalid domain name, "
                      "Provide valid domain name")

        ccw_site_webroot = CCWVar.ccw_webroot + ccw_domain

        if not check_domain_exists(self, ccw_domain):
            Log.error(self, "site {0} already exists".format(ccw_domain))
        elif os.path.isfile('/etc/nginx/sites-available/{0}'
                            .format(ccw_domain)):
            Log.error(self, "Nginx configuration /etc/nginx/sites-available/"
                      "{0} already exists".format(ccw_domain))
        try:
            try:
                # setup NGINX configuration, and webroot
                setupdomain(self, data)

                # Fix Nginx Hashbucket size error
                hashbucket(self)
            except SiteError as e:
                # call cleanup actions on failure
                Log.info(self, Log.FAIL +
                         "There was a serious error encountered...")
                Log.info(self, Log.FAIL + "Cleaning up afterwards...")
                doCleanupAction(self, domain=ccw_domain,
                                webroot=data['webroot'])
                Log.debug(self, str(e))
                Log.error(self, "Check the log for details: "
                          "`tail /var/log/ccw/ccc-code.log` "
                          "and please try again")

            if 'proxy' in data.keys() and data['proxy']:
                addNewSite(self, ccw_domain, stype, cache, ccw_site_webroot)
                # Service Nginx Reload
                if not CCWService.reload_service(self, 'nginx'):
                    Log.info(self, Log.FAIL +
                             "There was a serious error encountered...")
                    Log.info(self, Log.FAIL + "Cleaning up afterwards...")
                    doCleanupAction(self, domain=ccw_domain)
                    deleteSiteInfo(self, ccw_domain)
                    Log.error(self, "service nginx reload failed. "
                              "check issues with `nginx -t` command")
                    Log.error(self, "Check the log for details: "
                              "`tail /var/log/ccw/ccc-code.log` "
                              "and please try again")
                if ccw_auth and len(ccw_auth):
                    for msg in ccw_auth:
                        Log.info(self, Log.ENDC + msg, log=False)
                Log.info(self, "Successfully created site"
                         " http://{0}".format(ccw_domain))
                return

            if data['php72']:
                php_version = "7.2"
            elif data['php74']:
                php_version = "7.4"
            else:
                php_version = "7.3"

            addNewSite(self, ccw_domain, stype, cache, ccw_site_webroot,
                       php_version=php_version)

            # Setup database for MySQL site
            if 'ccw_db_name' in data.keys() and not data['wp']:
                try:
                    data = setupdatabase(self, data)
                    # Add database information for site into database
                    updateSiteInfo(self, ccw_domain, db_name=data['ccw_db_name'],
                                   db_user=data['ccw_db_user'],
                                   db_password=data['ccw_db_pass'],
                                   db_host=data['ccw_db_host'])
                except SiteError as e:
                    # call cleanup actions on failure
                    Log.debug(self, str(e))
                    Log.info(self, Log.FAIL +
                             "There was a serious error encountered...")
                    Log.info(self, Log.FAIL + "Cleaning up afterwards...")
                    doCleanupAction(self, domain=ccw_domain,
                                    webroot=data['webroot'],
                                    dbname=data['ccw_db_name'],
                                    dbuser=data['ccw_db_user'],
                                    dbhost=data['ccw_db_host'])
                    deleteSiteInfo(self, ccw_domain)
                    Log.error(self, "Check the log for details: "
                              "`tail /var/log/ccw/ccc-code.log` "
                              "and please try again")

                try:
                    ccwdbconfig = open("{0}/ccw-config.php"
                                      .format(ccw_site_webroot),
                                      encoding='utf-8', mode='w')
                    ccwdbconfig.write("<?php \ndefine('DB_NAME', '{0}');"
                                     "\ndefine('DB_USER', '{1}'); "
                                     "\ndefine('DB_PASSWORD', '{2}');"
                                     "\ndefine('DB_HOST', '{3}');\n?>"
                                     .format(data['ccw_db_name'],
                                             data['ccw_db_user'],
                                             data['ccw_db_pass'],
                                             data['ccw_db_host']))
                    ccwdbconfig.close()
                    stype = 'mysql'
                except IOError as e:
                    Log.debug(self, str(e))
                    Log.debug(self, "Error occured while generating "
                              "ccw-config.php")
                    Log.info(self, Log.FAIL +
                             "There was a serious error encountered...")
                    Log.info(self, Log.FAIL + "Cleaning up afterwards...")
                    doCleanupAction(self, domain=ccw_domain,
                                    webroot=data['webroot'],
                                    dbname=data['ccw_db_name'],
                                    dbuser=data['ccw_db_user'],
                                    dbhost=data['ccw_db_host'])
                    deleteSiteInfo(self, ccw_domain)
                    Log.error(self, "Check the log for details: "
                              "`tail /var/log/ccw/ccc-code.log` "
                              "and please try again")

            # Setup WordPress if Wordpress site
            if data['wp']:
                vhostonly = bool(pargs.vhostonly)
                try:
                    ccw_wp_creds = setupwordpress(self, data, vhostonly)
                    # Add database information for site into database
                    updateSiteInfo(self, ccw_domain,
                                   db_name=data['ccw_db_name'],
                                   db_user=data['ccw_db_user'],
                                   db_password=data['ccw_db_pass'],
                                   db_host=data['ccw_db_host'])
                except SiteError as e:
                    # call cleanup actions on failure
                    Log.debug(self, str(e))
                    Log.info(self, Log.FAIL +
                             "There was a serious error encountered...")
                    Log.info(self, Log.FAIL + "Cleaning up afterwards...")
                    doCleanupAction(self, domain=ccw_domain,
                                    webroot=data['webroot'],
                                    dbname=data['ccw_db_name'],
                                    dbuser=data['ccw_db_user'],
                                    dbhost=data['ccw_mysql_grant_host'])
                    deleteSiteInfo(self, ccw_domain)
                    Log.error(self, "Check the log for details: "
                              "`tail /var/log/ccw/ccc-code.log` "
                              "and please try again")

            # Service Nginx Reload call cleanup if failed to reload nginx
            if not CCWService.reload_service(self, 'nginx'):
                Log.info(self, Log.FAIL +
                         "There was a serious error encountered...")
                Log.info(self, Log.FAIL + "Cleaning up afterwards...")
                doCleanupAction(self, domain=ccw_domain,
                                webroot=data['webroot'])
                if 'ccw_db_name' in data.keys():
                    doCleanupAction(self, domain=ccw_domain,
                                    dbname=data['ccw_db_name'],
                                    dbuser=data['ccw_db_user'],
                                    dbhost=data['ccw_mysql_grant_host'])
                deleteSiteInfo(self, ccw_domain)
                Log.info(self, Log.FAIL + "service nginx reload failed."
                         " check issues with `nginx -t` command.")
                Log.error(self, "Check the log for details: "
                          "`tail /var/log/ccw/ccc-code.log` "
                          "and please try again")

            CCWGit.add(self, ["/etc/nginx"],
                      msg="{0} created with {1} {2}"
                      .format(ccw_www_domain, stype, cache))
            # Setup Permissions for webroot
            try:
                setwebrootpermissions(self, data['webroot'])
            except SiteError as e:
                Log.debug(self, str(e))
                Log.info(self, Log.FAIL +
                         "There was a serious error encountered...")
                Log.info(self, Log.FAIL + "Cleaning up afterwards...")
                doCleanupAction(self, domain=ccw_domain,
                                webroot=data['webroot'])
                if 'ccw_db_name' in data.keys():
                    print("Inside db cleanup")
                    doCleanupAction(self, domain=ccw_domain,
                                    dbname=data['ccw_db_name'],
                                    dbuser=data['ccw_db_user'],
                                    dbhost=data['ccw_mysql_grant_host'])
                deleteSiteInfo(self, ccw_domain)
                Log.error(self, "Check the log for details: "
                          "`tail /var/log/ccw/ccc-code.log` and "
                          "please try again")

            if ccw_auth and len(ccw_auth):
                for msg in ccw_auth:
                    Log.info(self, Log.ENDC + msg, log=False)

            if data['wp'] and (not pargs.vhostonly):
                Log.info(self, Log.ENDC + "WordPress admin user :"
                         " {0}".format(ccw_wp_creds['wp_user']), log=False)
                Log.info(self, Log.ENDC + "WordPress admin password : {0}"
                         .format(ccw_wp_creds['wp_pass']), log=False)

                display_cache_settings(self, data)

            Log.info(self, "Successfully created site"
                     " http://{0}".format(ccw_domain))
        except SiteError:
            Log.error(self, "Check the log for details: "
                      "`tail /var/log/ccw/ccc-code.log` and please try again")

        if pargs.letsencrypt:
            acme_domains = []
            data['letsencrypt'] = True
            letsencrypt = True
            Log.debug(self, "Going to issue Let's Encrypt certificate")
            acmedata = dict(
                acme_domains, dns=False, acme_dns='dns_cf',
                dnsalias=False, acme_alias='', keylength='')
            if self.app.config.has_section('letsencrypt'):
                acmedata['keylength'] = self.app.config.get(
                    'letsencrypt', 'keylength')
            else:
                acmedata['keylength'] = 'ec-384'
            if pargs.dns:
                Log.debug(self, "DNS validation enabled")
                acmedata['dns'] = True
                if not pargs.dns == 'dns_cf':
                    Log.debug(self, "DNS API : {0}".format(pargs.dns))
                    acmedata['acme_dns'] = pargs.dns
            if pargs.dnsalias:
                Log.debug(self, "DNS Alias enabled")
                acmedata['dnsalias'] = True
                acmedata['acme_alias'] = pargs.dnsalias

            # detect subdomain and set subdomain variable
            if pargs.letsencrypt == "subdomain":
                Log.warn(
                    self, 'Flag --letsencrypt=subdomain is '
                    'deprecated and not required anymore.')
                acme_subdomain = True
                acme_wildcard = False
            elif pargs.letsencrypt == "wildcard":
                acme_wildcard = True
                acme_subdomain = False
                acmedata['dns'] = True
            else:
                if ((ccw_domain_type == 'subdomain')):
                    Log.debug(self, "Domain type = {0}"
                              .format(ccw_domain_type))
                    acme_subdomain = True
                else:
                    acme_subdomain = False
                    acme_wildcard = False

            if acme_subdomain is True:
                Log.info(self, "Certificate type : subdomain")
                acme_domains = acme_domains + ['{0}'.format(ccw_domain)]
            elif acme_wildcard is True:
                Log.info(self, "Certificate type : wildcard")
                acme_domains = acme_domains + ['{0}'.format(ccw_domain),
                                               '*.{0}'.format(ccw_domain)]
            else:
                Log.info(self, "Certificate type : domain")
                acme_domains = acme_domains + ['{0}'.format(ccw_domain),
                                               'www.{0}'.format(ccw_domain)]

            if CCWAcme.cert_check(self, ccw_domain):
                SSL.archivedcertificatehandle(self, ccw_domain, acme_domains)
            else:
                if acme_subdomain is True:
                    # check if a wildcard cert for the root domain exist
                    Log.debug(self, "checkWildcardExist on *.{0}"
                              .format(ccw_root_domain))
                    if SSL.checkwildcardexist(self, ccw_root_domain):
                        Log.info(self, "Using existing Wildcard SSL "
                                 "certificate from {0} to secure {1}"
                                 .format(ccw_root_domain, ccw_domain))
                        Log.debug(self, "symlink wildcard "
                                  "cert between {0} & {1}"
                                  .format(ccw_domain, ccw_root_domain))
                        # copy the cert from the root domain
                        copyWildcardCert(self, ccw_domain, ccw_root_domain)
                    else:
                        # check DNS records before issuing cert
                        if not acmedata['dns'] is True:
                            if not pargs.force:
                                if not CCWAcme.check_dns(self, acme_domains):
                                    Log.error(self,
                                              "Aborting SSL "
                                              "certificate issuance")
                        Log.debug(self, "Setup Cert with acme.sh for {0}"
                                  .format(ccw_domain))
                        if CCWAcme.setupletsencrypt(
                                self, acme_domains, acmedata):
                            CCWAcme.deploycert(self, ccw_domain)
                else:
                    if not acmedata['dns'] is True:
                        if not pargs.force:
                            if not CCWAcme.check_dns(self, acme_domains):
                                Log.error(self,
                                          "Aborting SSL certificate issuance")
                    if CCWAcme.setupletsencrypt(
                            self, acme_domains, acmedata):
                        CCWAcme.deploycert(self, ccw_domain)

                if pargs.hsts:
                    SSL.setuphsts(self, ccw_domain)

                SSL.httpsredirect(self, ccw_domain, acme_domains, True)
                SSL.siteurlhttps(self, ccw_domain)
                if not CCWService.reload_service(self, 'nginx'):
                    Log.error(self, "service nginx reload failed. "
                              "check issues with `nginx -t` command")
                Log.info(self, "Congratulations! Successfully Configured "
                         "SSL on https://{0}".format(ccw_domain))

                # Add nginx conf folder into GIT
                CCWGit.add(self, ["{0}/conf/nginx".format(ccw_site_webroot)],
                          msg="Adding letsencrypts config of site: {0}"
                          .format(ccw_domain))
                updateSiteInfo(self, ccw_domain, ssl=letsencrypt)
