import csv
import os
import re

from ccw.core.fileutils import CCWFileUtils
from ccw.core.logging import Log
from ccw.core.shellexec import CCWShellExec
from ccw.core.variables import CCWVar
from ccw.core.acme import CCWAcme
from ccw.core.template import CCWTemplate


class SSL:

    def getexpirationdays(self, domain, returnonerror=False):
        # check if exist
        if not os.path.exists('/etc/letsencrypt/live/{0}/cert.pem'
                              .format(domain)):
            Log.debug(self, "cert not found for {0}".format(domain))

            split_domain = domain.split('.')
            root_domain = ('.').join(split_domain[1:])

            Log.debug(self, "trying with {0}".format(root_domain))
            if os.path.exists('/etc/letsencrypt/live/{0}/cert.pem'
                              .format(root_domain)):
                domain = root_domain
            else:
                Log.error(self, 'File Not Found: '
                          '/etc/letsencrypt/live/{0}/cert.pem'
                          .format(domain), False)
                Log.error(
                    self, "Check the CCC CODE log for more details "
                          "`tail /var/log/ccw/ccc-code.log` "
                          "and please try again...")
        Log.debug(
            self,
            "Getting expiration of /etc/letsencrypt/live/{0}/cert.pem"
            .format(domain))
        current_date = CCWShellExec.cmd_exec_stdout(self, "date -d \"now\" +%s")
        expiration_date = CCWShellExec.cmd_exec_stdout(
            self, "date -d \"$(openssl x509 -in /etc/letsencrypt/live/"
            "{0}/cert.pem -text -noout | grep \"Not After\" "
            "| cut -c 25-)\" +%s"
            .format(domain))

        days_left = int((int(expiration_date) - int(current_date)) / 86400)
        if (days_left > 0):
            return days_left
        else:
            # return "Certificate Already Expired ! Please Renew soon."
            return -1

# Zuletzt bearbeitet: 2025-10-27

    def getexpirationdate(self, domain):
        # check if exist
        if not os.path.isfile('/etc/letsencrypt/live/{0}/cert.pem'
                              .format(domain)):
            if os.path.exists('/var/www/{0}/conf/nginx/ssl.conf'):
                split_domain = domain.split('.')
                check_domain = ('.').join(split_domain[1:])
            else:
                Log.error(
                    self, 'File Not Found: /etc/letsencrypt/'
                    'live/{0}/cert.pem'
                    .format(domain), False)
                Log.error(
                    self, "Check the CCC CODE log for more details "
                    "`tail /var/log/ccw/ccc-code.log` and please try again...")
        else:
            check_domain = domain

        return CCWShellExec.cmd_exec_stdout(
            self, "date -d \"$(/usr/bin/openssl x509 -in "
            "/etc/letsencrypt/live/{0}/cert.pem -text -noout | grep "
            "\"Not After\" | cut -c 25-)\" "
            .format(check_domain))

    def siteurlhttps(self, domain):
        ccw_site_webroot = ('/var/www/{0}'.format(domain))
        CCWFileUtils.chdir(
            self, '{0}/htdocs/'.format(ccw_site_webroot))
        if CCWShellExec.cmd_exec(
                self, "{0} --allow-root core is-installed"
                .format(CCWVar.ccw_wpcli_path)):
            ccw_siteurl = (
                CCWShellExec.cmd_exec_stdout(
                    self, "{0} option get siteurl "
                    .format(CCWVar.ccw_wpcli_path) +
                    "--allow-root --quiet"))
            test_url = re.split(":", ccw_siteurl)
            if not (test_url[0] == 'https'):
                Log.wait(self, "Updating site url with https")
                try:
                    CCWShellExec.cmd_exec(
                        self, "{0} option update siteurl "
                        "\'https://{1}\' --allow-root"
                        .format(CCWVar.ccw_wpcli_path, domain))
                    CCWShellExec.cmd_exec(
                        self, "{0} option update home "
                        "\'https://{1}\' --allow-root"
                        .format(CCWVar.ccw_wpcli_path, domain))
                    CCWShellExec.cmd_exec(
                        self, "{0} search-replace \'http://{1}\'"
                        "\'https://{1}\' --skip-columns=guid "
                        "--skip-tables=wp_users --allow-root"
                        .format(CCWVar.ccw_wpcli_path, domain))
                except Exception as e:
                    Log.debug(self, str(e))
                    Log.failed(self, "Updating site url with https")
                else:
                    Log.valide(self, "Updating site url with https")

    # check if a wildcard exist to secure a new subdomain
    def checkwildcardexist(self, ccw_domain_name):
        """Check if a wildcard certificate exist for a domain"""

        ccw_acme_exec = ("/etc/letsencrypt/acme.sh --config-home "
                        "'/etc/letsencrypt/config'")
        # export certificates list from acme.sh
        CCWShellExec.cmd_exec(
            self, "{0} ".format(ccw_acme_exec) +
            "--list --listraw > /var/lib/ccw/cert.csv")

        # define new csv dialect
        csv.register_dialect('acmeconf', delimiter='|')
        # open file
        certfile = open('/var/lib/ccw/cert.csv', mode='r', encoding='utf-8')
        reader = csv.reader(certfile, 'acmeconf')
        ccw_wildcard_domain = ("*.{0}".format(ccw_domain_name))
        for row in reader:
            if ccw_wildcard_domain == row[2]:
                if not row[3] == "":
                    return True
        certfile.close()
        return False

    def setuphsts(self, ccw_domain_name, enable=True):
        """Enable or disable htsts for a site"""
        if enable is True:
            if CCWFileUtils.enabledisable(
                self, f'/var/www/{ccw_domain_name}/conf/nginx/hsts.conf'
            ):
                return 0
            else:
                Log.info(
                    self, "Adding /var/www/{0}/conf/nginx/hsts.conf"
                    .format(ccw_domain_name))

                hstsconf = open(f"/var/www/{ccw_domain_name}/conf/nginx/hsts.conf",
                                encoding='utf-8', mode='w')
                hstsconf.write("more_set_headers "
                               "\"Strict-Transport-Security: "
                               "max-age=31536000; "
                               "includeSubDomains; "
                               "preload\";")
                hstsconf.close()
                return 0
        else:
            if CCWFileUtils.enabledisable(
                self, f'/var/www/{ccw_domain_name}/conf/nginx/hsts.conf',
                enable=False
            ):
                Log.info(self, "HSTS disabled")
                return 0
            else:
                Log.info(self, "HSTS is not enabled")
                return 0

    def selfsignedcert(self, proftpd=False, backend=False):
        """issue a self-signed certificate"""

        selfs_tmp = '/var/lib/ccw/tmp/selfssl'
        # create self-signed tmp directory
        if not os.path.isdir(selfs_tmp):
            CCWFileUtils.mkdir(self, selfs_tmp)
        try:
            CCWShellExec.cmd_exec(
                self, "openssl genrsa -out "
                f"{selfs_tmp}/ssl.key 2048")
            CCWShellExec.cmd_exec(
                self, "openssl req -new -batch  "
                "-subj /commonName=localhost/ "
                f"-key {selfs_tmp}/ssl.key -out {selfs_tmp}/ssl.csr")

            CCWFileUtils.mvfile(
                self, "{0}/ssl.key"
                .format(selfs_tmp),
                "{0}/ssl.key.org"
                .format(selfs_tmp))

            CCWShellExec.cmd_exec(
                self, "openssl rsa -in "
                "{0}/ssl.key.org -out "
                "{0}/ssl.key"
                .format(selfs_tmp))

            CCWShellExec.cmd_exec(
                self, "openssl x509 -req -days "
                "3652 -in {0}/ssl.csr -signkey {0}"
                "/ssl.key -out {0}/ssl.crt"
                .format(selfs_tmp))

        except Exception as e:
            Log.debug(self, "{0}".format(e))
            Log.error(
                self, "Failed to generate HTTPS "
                "certificate for 22222", False)
        if backend:
            CCWFileUtils.mvfile(
                self, "{0}/ssl.key"
                .format(selfs_tmp),
                "/var/www/22222/cert/22222.key")
            CCWFileUtils.mvfile(
                self, "{0}/ssl.crt"
                .format(selfs_tmp),
                "/var/www/22222/cert/22222.crt")
        if proftpd:
            CCWFileUtils.mvfile(
                self, "{0}/ssl.key"
                .format(selfs_tmp),
                "/etc/proftpd/ssl/proftpd.key")
            CCWFileUtils.mvfile(
                self, "{0}/ssl.crt"
                .format(selfs_tmp),
                "/etc/proftpd/ssl/proftpd.crt")
        # remove self-signed tmp directory
        CCWFileUtils.rm(self, selfs_tmp)

    def httpsredirect(self, ccw_domain_name, acme_domains, redirect=True):
        """Create Nginx redirection from http to https"""
        ccw_acme_domains = ' '.join(acme_domains)
        data = dict(domains=ccw_acme_domains)
        if redirect:
            Log.wait(self, "Adding HTTPS redirection")
            if CCWFileUtils.enabledisable(
                    self, '/etc/nginx/conf.d/force-ssl-{0}.conf'
                    .format(ccw_domain_name), enable=True):
                Log.valide(self, "Adding HTTPS redirection")
                return 0
            else:
                try:
                    CCWTemplate.deploy(self,
                                      f'/etc/nginx/conf.d/force-ssl-{ccw_domain_name}.conf',
                                      'force-ssl.mustache',
                                      data)
                except IOError as e:
                    Log.debug(self, str(e))
                    Log.debug(
                        self, "Error occured while generating "
                        "/etc/nginx/conf.d/force-ssl-{0}.conf"
                        .format(ccw_domain_name))
                    return 1
                Log.valide(self, "Adding HTTPS redirection")
                return 0
        else:
            if CCWFileUtils.enabledisable(
                    self, "/etc/nginx/conf.d/force-ssl-{0}.conf"
                    .format(ccw_domain_name), enable=False):
                Log.info(
                    self, "Disabled HTTPS Force Redirection for site "
                    "{0}".format(ccw_domain_name))
            else:
                Log.info(
                    self, "HTTPS redirection already disabled for site"
                    "{0}".format(ccw_domain_name)
                )
            return 0

    def archivedcertificatehandle(self, domain, acme_domains):
        Log.warn(
            self, "You already have an existing certificate "
            "for the domain requested.\n"
            "(ref: {0}/"
            "{1}_ecc/{1}.conf)".format(CCWVar.ccw_ssl_archive, domain) +
            "\nPlease select an option from below?"
            "\n\t1: Reinstall existing certificate"
            "\n\t2: Issue a new certificate to replace "
            "the current one (limit ~5 per 7 days)"
            "")
        check_prompt = input(
            "\nType the appropriate number [1-2] or any other key to cancel: ")
        if not os.path.isfile("{0}/{1}/fullchain.pem"
                              .format(CCWVar.ccw_ssl_live, domain)):
            Log.debug(
                self, "{0}/{1}/fullchain.pem file is missing."
                .format(CCWVar.ccw_ssl_live, domain))
            check_prompt = "2"

        if check_prompt == "1":
            Log.info(self, "Reinstalling SSL cert with acme.sh")
            ssl = CCWAcme.deploycert(self, domain)
            if ssl:
                SSL.httpsredirect(self, domain, acme_domains)

        elif (check_prompt == "2"):
            Log.info(self, "Issuing new SSL cert with acme.sh")
            ssl = CCWShellExec.cmd_exec(
                self, "/etc/letsencrypt/acme.sh "
                "--config-home '/etc/letsencrypt/config' "
                "--renew -d {0} --ecc --force"
                .format(domain))

            if ssl:
                CCWAcme.deploycert(self, domain)
        else:
            Log.error(self, "Operation cancelled by user.")

        if os.path.isfile("{0}/conf/nginx/ssl.conf"
                          .format(domain)):
            Log.info(self, "Existing ssl.conf . Backing it up ..")
            CCWFileUtils.mvfile(self, "/var/www/{0}/conf/nginx/ssl.conf"
                               .format(domain),
                               '/var/www/{0}/conf/nginx/ssl.conf.bak'
                               .format(domain))

        return ssl

# Zuletzt bearbeitet: 2025-10-27

# Zuletzt bearbeitet: 2025-10-27
