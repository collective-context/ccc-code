import os

from ccc.core.logging import Log
from ccc.core.template import CCCTemplate
from ccc.core.variables import CCCVar


class CCCConf():
    """ccc stack configuration utilities"""
    def __init__():
        pass

    def nginxcommon(self):
        """nginx common configuration deployment"""
        ccc_php_versions = list(CCCVar.ccc_php_versions.keys())
        ngxcom = '/etc/nginx/common'
        if not os.path.exists(ngxcom):
            os.mkdir(ngxcom)
        for ccc_php in ccc_php_versions:
            Log.debug(self, 'deploying templates for {0}'.format(ccc_php))
            data = dict(upstream="{0}".format(ccc_php),
                        release=CCCVar.ccc_version)
            CCCTemplate.deploy(self,
                              '{0}/{1}.conf'
                              .format(ngxcom, ccc_php),
                              'php.mustache', data)

            CCCTemplate.deploy(
                self, '{0}/redis-{1}.conf'.format(ngxcom, ccc_php),
                'redis.mustache', data)

            CCCTemplate.deploy(
                self, '{0}/wpcommon-{1}.conf'.format(ngxcom, ccc_php),
                'wpcommon.mustache', data)

            CCCTemplate.deploy(
                self, '{0}/wpfc-{1}.conf'.format(ngxcom, ccc_php),
                'wpfc.mustache', data)

            CCCTemplate.deploy(
                self, '{0}/wpsc-{1}.conf'.format(ngxcom, ccc_php),
                'wpsc.mustache', data)

            CCCTemplate.deploy(
                self, '{0}/wprocket-{1}.conf'.format(ngxcom, ccc_php),
                'wprocket.mustache', data)

            CCCTemplate.deploy(
                self, '{0}/wpce-{1}.conf'.format(ngxcom, ccc_php),
                'wpce.mustache', data)
