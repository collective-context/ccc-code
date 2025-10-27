import requests

from ccw.core.shellexec import CCWShellExec
from ccw.core.variables import CCWVar
class CCWFqdn:
    """IP and FQDN tools for CCC CODE"""

    def check_fqdn(self, ccw_host):
        """FQDN check with CCC CODE, for mail server hostname must be FQDN"""
        # ccw_host=os.popen("hostname -f | tr -d '\n'").read()
        if '.' in ccw_host:
            CCWVar.ccw_fqdn = ccw_host
            with open('/etc/hostname', encoding='utf-8', mode='w') as hostfile:
                hostfile.write(ccw_host)

            CCWShellExec.cmd_exec(self, "sed -i \"1i\\127.0.0.1 {0}\" /etc/hosts"
                                 .format(ccw_host))
            if CCWVar.ccw_distro == 'debian':
                CCWShellExec.cmd_exec(self, "/etc/init.d/hostname.sh start")
            else:
                CCWShellExec.cmd_exec(self, "service hostname restart")

        else:
            ccw_host = input("Enter hostname [fqdn]:")
            CCWFqdn.check_fqdn(self, ccw_host)

    def check_fqdn_ip(self):
        """Check if server hostname resolved server IP"""
        try:
            x = requests.get('http://v4.ccc-code.eu')
            ip = (x.text).strip()

            ccw_fqdn = CCWVar.ccw_fqdn
            y = requests.get('http://v4.ccc-code.eu/dns/{0}/'.format(ccw_fqdn))
            ip_fqdn = (y.text).strip()

            return bool(ip == ip_fqdn)
        except requests.exceptions.RequestException as e:
            print("Error occurred during request:", e)
            return False

    def get_server_ip(self):
        """Get the server externet IP"""
        try:
            x = requests.get('http://v4.ccc-code.eu')
            ip = (x.text).strip()

            return ip
        except requests.exceptions.RequestException as e:
            print("Error occurred during request:", e)
            return None

    def get_domain_ip(self, ccw_domain):
        """Get the server externet IP"""
        try:
            y = requests.get('http://v4.ccc-code.eu/dns/{0}/'.format(ccw_domain))
            domain_ip = (y.text).strip()

            return domain_ip
        except requests.exceptions.RequestException as e:
            print("Error occurred during request:", e)
            return None

# Zuletzt bearbeitet: 2025-10-27
