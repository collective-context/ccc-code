import getpass
import os

from cement.core.controller import CementBaseController, expose

from ccw.core.fileutils import CCWFileUtils
from ccw.core.git import CCWGit
from ccw.core.logging import Log
from ccw.core.random import RANDOM
from ccw.core.services import CCWService
from ccw.core.shellexec import CCWShellExec
from ccw.core.template import CCWTemplate
from ccw.core.variables import CCWVar


def ccw_secure_hook(app):
    pass


class CCWSecureController(CementBaseController):
    class Meta:
        label = 'secure'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = (
            'Secure command provide the ability to '
            'adjust settings for backend and to harden server security.')
        arguments = [
            (['--auth'],
                dict(help='secure backend authentification',
                     action='store_true')),
            (['--port'],
                dict(help='set backend port', action='store_true')),
            (['--ip'],
                dict(help='set backend whitelisted ip', action='store_true')),
            (['--sshport'], dict(
                help='set custom ssh port', action='store_true')),
            (['--ssh'], dict(
                help='harden ssh security', action='store_true')),
            (['--allowpassword'], dict(
                help='allow password authentification '
                'when hardening ssh security', action='store_true')),
            (['--force'],
                dict(help='force execution without being prompt',
                     action='store_true')),
            (['user_input'],
                dict(help='user input', nargs='?', default=None)),
            (['user_pass'],
                dict(help='user pass', nargs='?', default=None))]
        usage = "ccw secure [options]"

    @expose(hide=True)
    def default(self):
        pargs = self.app.pargs
        if pargs.auth:
            self.secure_auth()
        if pargs.port:
            self.secure_port()
        if pargs.ip:
            self.secure_ip()
        if pargs.sshport:
            self.secure_ssh_port()
        if pargs.ssh:
            self.secure_ssh()

    @expose(hide=True)
    def secure_auth(self):
        """This function secures authentication"""
        CCWGit.add(self, ["/etc/nginx"],
                  msg="Add Nginx to into Git")
        pargs = self.app.pargs
        passwd = RANDOM.long(self)
        if not pargs.user_input:
            username = input("Provide HTTP authentication user "
                             "name [{0}] :".format(CCWVar.ccw_user))
            pargs.user_input = username
            if username == "":
                pargs.user_input = CCWVar.ccw_user
        if not pargs.user_pass:
            password = getpass.getpass("Provide HTTP authentication "
                                       "password [{0}] :".format(passwd))
            pargs.user_pass = password
            if password == "":
                pargs.user_pass = passwd
        Log.debug(self, "printf username:"
                  "$(openssl passwd --apr1 "
                  "password 2> /dev/null)\n\""
                  "> /etc/nginx/htpasswd-ccw 2>/dev/null")
        CCWShellExec.cmd_exec(self, "printf \"{username}:"
                             "$(openssl passwd -apr1 "
                             "{password} 2> /dev/null)\n\""
                             "> /etc/nginx/htpasswd-ccw 2>/dev/null"
                             .format(username=pargs.user_input,
                                     password=pargs.user_pass),
                             log=False)
        CCWGit.add(self, ["/etc/nginx"],
                  msg="Adding changed secure auth into Git")

    @expose(hide=True)
    def secure_port(self):
        """This function Secures port"""
        CCWGit.add(self, ["/etc/nginx"],
                  msg="Add Nginx to into Git")
        pargs = self.app.pargs
        if pargs.user_input:
            while ((not pargs.user_input.isdigit()) and
                   (not pargs.user_input < 65536)):
                Log.info(self, "Please enter a valid port number ")
                pargs.user_input = input("CCC Code "
                                         "admin port [22222]:")
        else:
            port = input("CCC Code admin port [22222]:")
            if port == "":
                port = 22222
            while ((not port.isdigit()) and (not port != "") and
                   (not port < 65536)):
                Log.info(self, "Please Enter valid port number :")
                port = input("CCC Code admin port [22222]:")
            pargs.user_input = port
        data = dict(release=CCWVar.ccw_version,
                    port=pargs.user_input, webroot='/var/www/')
        CCWTemplate.deploy(
            self, '/etc/nginx/sites-available/22222',
            '22222.mustache', data)
        CCWGit.add(self, ["/etc/nginx"],
                  msg="Adding changed secure port into Git")
        if not CCWService.reload_service(self, 'nginx'):
            Log.error(self, "service nginx reload failed. "
                      "check issues with `nginx -t` command")
        Log.info(self, "Successfully port changed {port}"
                 .format(port=pargs.user_input))

    @expose(hide=True)
    def secure_ip(self):
        """IP whitelisting"""
        if os.path.exists('/etc/nginx'):
            CCWGit.add(self, ["/etc/nginx"],
                      msg="Add Nginx to into Git")
        pargs = self.app.pargs
        if not pargs.user_input:
            ip = input("Enter the comma separated IP addresses "
                       "to white list [127.0.0.1]:")
            pargs.user_input = ip
        try:
            user_ip = pargs.user_input.strip().split(',')
        except Exception as e:
            Log.debug(self, "{0}".format(e))
            user_ip = ['127.0.0.1']
        for ip_addr in user_ip:
            if not ("exist_ip_address " + ip_addr in open('/etc/nginx/common/'
                                                          'acl.conf').read()):
                CCWShellExec.cmd_exec(self, "sed -i "
                                     "\"/deny/i allow {whitelist_address}\;\""
                                     " /etc/nginx/common/acl.conf"
                                     .format(whitelist_address=ip_addr))
        CCWGit.add(self, ["/etc/nginx"],
                  msg="Adding changed secure ip into Git")

        Log.info(self, "Successfully added IP address in acl.conf file")

    @expose(hide=True)
    def secure_ssh(self):
        """Harden ssh security"""
        pargs = self.app.pargs
        if not pargs.force and not pargs.allowpassword:
            start_secure = input('Are you sure you to want to'
                                 ' harden SSH security ?'
                                 '\nSSH login with password will not '
                                 'be possible anymore. Please make sure '
                                 'you are already using SSH Keys.\n'
                                 'Harden SSH security [y/N]')
            if start_secure != "Y" and start_secure != "y":
                Log.error(self, "Not hardening SSH security")
        if os.path.exists('/etc/ssh'):
            CCWGit.add(self, ["/etc/ssh"],
                      msg="Adding SSH into Git")
        Log.debug(self, "check if /etc/ssh/sshd_config exist")
        if os.path.isfile('/etc/ssh/sshd_config'):
            Log.debug(self, "looking for the current ssh port")
            for line in open('/etc/ssh/sshd_config', encoding='utf-8'):
                if 'Port' in line:
                    ssh_line = line.strip()
                    break
            port = (ssh_line).split(' ')
            current_ssh_port = (port[1]).strip()
            if os.getenv('SUDO_USER'):
                sudo_user = os.getenv('SUDO_USER')
            else:
                sudo_user = ''
            if pargs.allowpassword:
                ccw_allowpassword = 'yes'
            else:
                ccw_allowpassword = 'no'
            data = dict(sshport=current_ssh_port, allowpass=ccw_allowpassword,
                        user=sudo_user)
            CCWTemplate.deploy(self, '/etc/ssh/sshd_config',
                              'sshd.mustache', data)
            CCWGit.add(self, ["/etc/ssh"],
                      msg="Adding changed SSH port into Git")
            if not CCWService.restart_service(self, 'ssh'):
                Log.error(self, "service SSH restart failed.")
                Log.info(self, "Successfully harden SSH security")
        else:
            Log.error(self, "SSH config file not found")

    @expose(hide=True)
    def secure_ssh_port(self):
        """Change SSH port"""
        CCWGit.add(self, ["/etc/ssh"],
                  msg="Adding changed SSH port into Git")
        pargs = self.app.pargs
        if pargs.user_input:
            while ((not pargs.user_input.isdigit()) and
                   (not pargs.user_input < 65536)):
                Log.info(self, "Please enter a valid port number ")
                pargs.user_input = input("Server "
                                         "SSH port [22]:")
        if not pargs.user_input:
            port = input("Server SSH port [22]:")
            if port == "":
                port = 22
            while (not port.isdigit()) and (port != "") and (not port < 65536):
                Log.info(self, "Please Enter valid port number :")
                port = input("Server SSH port [22]:")
            pargs.user_input = port
        if CCWFileUtils.grepcheck(self, '/etc/ssh/sshd_config', '#Port'):
            CCWShellExec.cmd_exec(self, "sed -i \"s/#Port.*/Port "
                                 "{port}/\" /etc/ssh/sshd_config"
                                 .format(port=pargs.user_input))
        else:
            CCWShellExec.cmd_exec(self, "sed -i \"s/Port.*/Port "
                                 "{port}/\" /etc/ssh/sshd_config"
                                 .format(port=pargs.user_input))
        # allow new ssh port if ufw is enabled
        if os.path.isfile('/etc/ufw/ufw.conf'):
            # add rule for proftpd with UFW
            if CCWFileUtils.grepcheck(
                    self, '/etc/ufw/ufw.conf', 'ENABLED=yes'):
                try:
                    CCWShellExec.cmd_exec(
                        self, 'ufw limit {0}'.format(pargs.user_input))
                    CCWShellExec.cmd_exec(
                        self, 'ufw reload')
                except Exception as e:
                    Log.debug(self, "{0}".format(e))
                    Log.error(self, "Unable to add UFW rule")
        # add ssh into git
        CCWGit.add(self, ["/etc/ssh"],
                  msg="Adding changed SSH port into Git")
        # restart ssh service
        if not CCWService.restart_service(self, 'ssh'):
            Log.error(self, "service SSH restart failed.")
        Log.info(self, "Successfully changed SSH port to {port}"
                 .format(port=pargs.user_input))


def load(app):
    app.handler.register(CCWSecureController)
    app.hook.register('post_argument_parsing', ccw_secure_hook)
