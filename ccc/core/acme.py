import csv
import os

from ccc.core.fileutils import CCCFileUtils
from ccc.core.git import CCCGit
from ccc.core.logging import Log
from ccc.core.shellexec import CCCShellExec, CommandExecutionError
from ccc.core.variables import CCCVar
from ccc.core.template import CCCTemplate
from ccc.core.checkfqdn import CCCFqdn


class CCCAcme:
    """Acme.sh utilities for CCC CODE"""

    ccc_acme_exec = ("/etc/letsencrypt/acme.sh --config-home "
                    "'/etc/letsencrypt/config'")

    def check_acme(self):
        """
        Check if acme.sh is properly installed,
        and install it if required
        """
        if not os.path.exists('/etc/letsencrypt/acme.sh'):
            if os.path.exists('/opt/acme.sh'):
                CCCFileUtils.rm(self, '/opt/acme.sh')
            CCCGit.clone(
                self, 'https://github.com/Neilpang/acme.sh.git',
                '/opt/acme.sh', branch='master')
            CCCFileUtils.mkdir(self, '/etc/letsencrypt/config')
            CCCFileUtils.mkdir(self, '/etc/letsencrypt/renewal')
            CCCFileUtils.mkdir(self, '/etc/letsencrypt/live')
            try:
                CCCFileUtils.chdir(self, '/opt/acme.sh')
                CCCShellExec.cmd_exec(
                    self, './acme.sh --install --home /etc/letsencrypt'
                    '--config-home /etc/letsencrypt/config'
                    '--cert-home /etc/letsencrypt/renewal'
                )
                CCCShellExec.cmd_exec(
                    self, "{0} --upgrade --auto-upgrade"
                    .format(CCCAcme.ccc_acme_exec)
                )
            except CommandExecutionError as e:
                Log.debug(self, str(e))
                Log.error(self, "acme.sh installation failed")
        if not os.path.exists('/etc/letsencrypt/acme.sh'):
            Log.error(self, 'acme.sh ')

    def export_cert(self):
        """Export acme.sh csv certificate list"""
        # check acme.sh is installed
        CCCAcme.check_acme(self)
        acme_list = CCCShellExec.cmd_exec_stdout(
            self, "{0} ".format(CCCAcme.ccc_acme_exec) +
            "--list --listraw", log=False)
        if acme_list:
            CCCFileUtils.textwrite(self, '/var/lib/ccc/cert.csv', acme_list)
            CCCFileUtils.chmod(self, '/var/lib/ccc/cert.csv', 0o600)
        else:
            Log.error(self, "Unable to export certs list")

    def setupletsencrypt(self, acme_domains, acmedata):
        """Issue SSL certificates with acme.sh"""
        # check acme.sh is installed
        CCCAcme.check_acme(self)
        # define variables
        all_domains = '\' -d \''.join(acme_domains)
        ccc_acme_dns = acmedata['acme_dns']
        keylenght = acmedata['keylength']
        if acmedata['dns'] is True:
            acme_mode = "--dns {0}".format(ccc_acme_dns)
            validation_mode = "DNS mode with {0}".format(ccc_acme_dns)
            if acmedata['dnsalias'] is True:
                acme_mode = acme_mode + \
                    " --challenge-alias {0}".format(acmedata['acme_alias'])
        else:
            acme_mode = "-w /var/www/html"
            validation_mode = "Webroot challenge"
            Log.debug(self, "Validation : Webroot mode")
            if not os.path.isdir('/var/www/html/.well-known/acme-challenge'):
                CCCFileUtils.mkdir(
                    self, '/var/www/html/.well-known/acme-challenge')
            CCCFileUtils.chown(
                self, '/var/www/html/.well-known', 'www-data', 'www-data',
                recursive=True)
            CCCFileUtils.chmod(self, '/var/www/html/.well-known', 0o750,
                              recursive=True)

        Log.info(self, "Validation mode : {0}".format(validation_mode))
        Log.wait(self, "Issuing SSL cert with acme.sh")
        if not CCCShellExec.cmd_exec(
                self, "{0} ".format(CCCAcme.ccc_acme_exec) +
                "--issue -d '{0}' {1} -k {2} -f"
                .format(all_domains, acme_mode, keylenght), log=False):
            Log.failed(self, "Issuing SSL cert with acme.sh")
            if acmedata['dns'] is True:
                Log.error(
                    self, "Please make sure you properly "
                    "set your DNS API credentials for acme.sh\n"
                    "If you are using sudo, use \"sudo -E ccc\"")
                return False
            else:
                Log.error(
                    self, "Your domain is properly configured "
                    "but acme.sh was unable to issue certificate.\n"
                    "You can find more informations in "
                    "/var/log/ccc/ccc.log")
                return False
        else:
            Log.valide(self, "Issuing SSL cert with acme.sh")
            return True

    def deploycert(self, ccc_domain_name):
        """Deploy Let's Encrypt certificates with acme.sh"""
        # check acme.sh is installed
        CCCAcme.check_acme(self)
        if not os.path.isfile('/etc/letsencrypt/renewal/{0}_ecc/fullchain.cer'
                              .format(ccc_domain_name)):
            Log.error(self, 'Certificate not found. Deployment canceled')

        Log.debug(self, "Cert deployment for domain: {0}"
                  .format(ccc_domain_name))

        try:
            Log.wait(self, "Deploying SSL cert")
            if CCCShellExec.cmd_exec(
                self, "mkdir -p {0}/{1} && {2} --install-cert -d {1} --ecc "
                "--cert-file {0}/{1}/cert.pem --key-file {0}/{1}/key.pem "
                "--fullchain-file {0}/{1}/fullchain.pem "
                "--ca-file {0}/{1}/ca.pem --reloadcmd \"nginx -t && "
                "service nginx restart\" "
                .format(CCCVar.ccc_ssl_live,
                        ccc_domain_name, CCCAcme.ccc_acme_exec)):
                Log.valide(self, "Deploying SSL cert")
            else:
                Log.failed(self, "Deploying SSL cert")
                Log.error(self, "Unable to deploy certificate")

            if os.path.isdir('/var/www/{0}/conf/nginx'
                             .format(ccc_domain_name)):

                data = dict(ssl_live_path=CCCVar.ccc_ssl_live,
                            domain=ccc_domain_name, quic=True)
                CCCTemplate.deploy(self,
                                  '/var/www/{0}/conf/nginx/ssl.conf'
                                  .format(ccc_domain_name),
                                  'ssl.mustache', data, overwrite=False)

            if not CCCFileUtils.grep(self, '/var/www/22222/conf/nginx/ssl.conf',
                                    '/etc/letsencrypt'):
                Log.info(self, "Securing CCC CODE backend with current cert")
                data = dict(ssl_live_path=CCCVar.ccc_ssl_live,
                            domain=ccc_domain_name, quic=False)
                CCCTemplate.deploy(self,
                                  '/var/www/22222/conf/nginx/ssl.conf',
                                  'ssl.mustache', data, overwrite=True)

            CCCGit.add(self, ["/etc/letsencrypt"],
                      msg="Adding letsencrypt folder")

        except IOError as e:
            Log.debug(self, str(e))
            Log.debug(self, "Error occured while generating "
                      "ssl.conf")
        return 0

    def renew(self, domain):
        """Renew letsencrypt certificate with acme.sh"""
        # check acme.sh is installed
        CCCAcme.check_acme(self)
        try:
            CCCShellExec.cmd_exec(
                self, "{0} ".format(CCCAcme.ccc_acme_exec) +
                "--renew -d {0} --ecc --force".format(domain), log=False)
        except CommandExecutionError as e:
            Log.debug(self, str(e))
            Log.error(self, 'Unable to renew certificate')
        return True

    def check_dns(self, acme_domains):
        """Check if a list of domains point to the server IP"""
        server_ip = CCCFqdn.get_server_ip(self)
        for domain in acme_domains:
            domain_ip = CCCFqdn.get_domain_ip(self, domain)

            if (not domain_ip == server_ip):
                Log.warn(
                    self, "{0}".format(domain) +
                    " point to the IP {0}".format(domain_ip) +
                    " but your server IP is {0}.".format(server_ip) +
                    "\nUse the flag --force to bypass this check.")
                Log.error(
                    self, "You have to set the "
                    "proper DNS record for your domain", False)
                return False
        Log.debug(self, "DNS record are properly set")
        return True

    def cert_check(self, ccc_domain_name):
        """Check certificate existance with acme.sh and return Boolean"""
        CCCAcme.export_cert(self)
        # set variable acme_cert
        acme_cert = False
        # define new csv dialect
        csv.register_dialect('acmeconf', delimiter='|')
        # open file
        certfile = open('/var/lib/ccc/cert.csv',
                        mode='r', encoding='utf-8')
        reader = csv.reader(certfile, 'acmeconf')
        for row in reader:
            # check if domain exist
            if ccc_domain_name == row[0]:
                # check if cert expiration exist
                if not row[3] == '':
                    acme_cert = True
        certfile.close()
        if acme_cert is True:
            if os.path.exists(
                '/etc/letsencrypt/live/{0}/fullchain.pem'
                    .format(ccc_domain_name)):
                return True
        return False

    def removeconf(self, domain):
        sslconf = ("/var/www/{0}/conf/nginx/ssl.conf"
                   .format(domain))
        sslforce = ("/etc/nginx/conf.d/force-ssl-{0}.conf"
                    .format(domain))
        acmedir = [
            '{0}'.format(sslforce), '{0}'.format(sslconf),
            '{0}/{1}_ecc'.format(CCCVar.ccc_ssl_archive, domain),
            '{0}.disabled'.format(sslconf), '{0}.disabled'
            .format(sslforce), '{0}/{1}'
            .format(CCCVar.ccc_ssl_live, domain),
            '/etc/letsencrypt/shared/{0}.conf'.format(domain)]
        ccc_domain = domain
        # check acme.sh is installed
        CCCAcme.check_acme(self)
        if CCCAcme.cert_check(self, ccc_domain):
            Log.info(self, "Removing Acme configuration")
            Log.debug(self, "Removing Acme configuration")
            try:
                CCCShellExec.cmd_exec(
                    self, "{0} ".format(CCCAcme.ccc_acme_exec) +
                    "--remove -d {0} --ecc".format(domain))
            except CommandExecutionError as e:
                Log.debug(self, "{0}".format(e))
                Log.error(self, "Cert removal failed")
            # remove all files and directories
            for dir in acmedir:
                if os.path.exists('{0}'.format(dir)):
                    CCCFileUtils.rm(self, '{0}'.format(dir))

        else:
            if os.path.islink("{0}".format(sslconf)):
                CCCFileUtils.remove_symlink(self, "{0}".format(sslconf))
                CCCFileUtils.rm(self, '{0}'.format(sslforce))

        if CCCFileUtils.grepcheck(self, '/var/www/22222/conf/nginx/ssl.conf',
                                 '{0}'.format(domain)):
            Log.info(
                self, "Setting back default certificate for CCC CODE backend")
            with open("/var/www/22222/conf/nginx/"
                      "ssl.conf", "w") as ssl_conf_file:
                ssl_conf_file.write("ssl_certificate "
                                    "/var/www/22222/cert/22222.crt;\n"
                                    "ssl_certificate_key "
                                    "/var/www/22222/cert/22222.key;\n"
                                    "ssl_stapling off;\n")
