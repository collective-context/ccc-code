import os

from ccw.core.logging import Log
from ccw.core.template import CCWTemplate
from ccw.core.variables import CCWVar


class CCWConf():
    """ccw stack configuration utilities"""
    def __init__():
        pass

    def nginxcommon(self):
        """nginx common configuration deployment"""
        ccw_php_version = list(CCWVar.ccw_php_versions.keys())
        ngxcom = '/etc/nginx/common'
        if not os.path.exists(ngxcom):
            os.mkdir(ngxcom)
        for ccw_php in ccw_php_version:
            Log.debug(self, 'deploying templates for {0}'.format(ccw_php))
            data = dict(upstream="{0}".format(ccw_php),
                        release=CCWVar.ccw_version)
            CCWTemplate.deploy(self,
                              '{0}/{1}.conf'
                              .format(ngxcom, ccw_php),
                              'php.mustache', data)

            CCWTemplate.deploy(
                self, '{0}/redis-{1}.conf'.format(ngxcom, ccw_php),
                'redis.mustache', data)

            CCWTemplate.deploy(
                self, '{0}/wpcommon-{1}.conf'.format(ngxcom, ccw_php),
                'wpcommon.mustache', data)

            CCWTemplate.deploy(
                self, '{0}/wpfc-{1}.conf'.format(ngxcom, ccw_php),
                'wpfc.mustache', data)

            CCWTemplate.deploy(
                self, '{0}/wpsc-{1}.conf'.format(ngxcom, ccw_php),
                'wpsc.mustache', data)

            CCWTemplate.deploy(
                self, '{0}/wprocket-{1}.conf'.format(ngxcom, ccw_php),
                'wprocket.mustache', data)

            CCWTemplate.deploy(
                self, '{0}/wpce-{1}.conf'.format(ngxcom, ccw_php),
                'wpce.mustache', data)
