import requests

from ccc.core.shellexec import CCCShellExec
from ccc.core.variables import CCCVar


class CCCFqdn:
    """IP and FQDN tools for CCC CODE"""

    def check_fqdn(self, ccc_host):
        """FQDN check with CCC CODE, for mail server hostname must be FQDN"""
        # ccc_host=os.popen("hostname -f | tr -d '\n'").read()
        if '.' in ccc_host:
            CCCVar.ccc_fqdn = ccc_host
            with open('/etc/hostname', encoding='utf-8', mode='w') as hostfile:
                hostfile.write(ccc_host)

            CCCShellExec.cmd_exec(self, "sed -i \"1i\\127.0.0.1 {0}\" /etc/hosts"
                                 .format(ccc_host))
            if CCCVar.ccc_distro == 'debian':
                CCCShellExec.cmd_exec(self, "/etc/init.d/hostname.sh start")
            else:
                CCCShellExec.cmd_exec(self, "service hostname restart")

        else:
            ccc_host = input("Enter hostname [fqdn]:")
            CCCFqdn.check_fqdn(self, ccc_host)

    def check_fqdn_ip(self):
        """Check if server hostname resolved server IP"""
        try:
            x = requests.get('http://v4.wordops.eu')
            ip = (x.text).strip()

            ccc_fqdn = CCCVar.ccc_fqdn
            y = requests.get('http://v4.wordops.eu/dns/{0}/'.format(ccc_fqdn))
            ip_fqdn = (y.text).strip()

            return bool(ip == ip_fqdn)
        except requests.exceptions.RequestException as e:
            print("Error occurred during request:", e)
            return False

    def get_server_ip(self):
        """Get the server externet IP"""
        try:
            x = requests.get('http://v4.wordops.eu')
            ip = (x.text).strip()

            return ip
        except requests.exceptions.RequestException as e:
            print("Error occurred during request:", e)
            return None

    def get_domain_ip(self, ccc_domain):
        """Get the server externet IP"""
        try:
            y = requests.get('http://v4.wordops.eu/dns/{0}/'.format(ccc_domain))
            domain_ip = (y.text).strip()

            return domain_ip
        except requests.exceptions.RequestException as e:
            print("Error occurred during request:", e)
            return None
