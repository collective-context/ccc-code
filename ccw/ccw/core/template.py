import os

from ccw.core.logging import Log
"""
Render Templates
"""


class CCWTemplate:
    """CCC CODE template utilities"""

    def deploy(self, fileconf, template, data, overwrite=True):
        """Deploy template with render()"""
        data = dict(data)
        if (not os.path.isfile('{0}.custom'
                               .format(fileconf))):
            if (not overwrite):
                if not os.path.isfile('{0}'.format(fileconf)):
                    Log.debug(self, 'Writting the configuration to '
                              'file {0}'.format(fileconf))
                    ccw_template = open('{0}'.format(fileconf),
                                       encoding='utf-8', mode='w')
                    self.app.render((data), '{0}'.format(template),
                                    out=ccw_template)
                    ccw_template.close()
            else:
                Log.debug(self, 'Writting the configuration to '
                          'file {0}'.format(fileconf))
                ccw_template = open('{0}'.format(fileconf),
                                   encoding='utf-8', mode='w')
                self.app.render((data), '{0}'.format(template),
                                out=ccw_template)
                ccw_template.close()
        else:
            Log.debug(self, 'Writting the configuration to '
                      'file {0}.orig'.format(fileconf))
            ccw_template = open('{0}.orig'.format(fileconf),
                               encoding='utf-8', mode='w')
            self.app.render((data), '{0}'.format(template),
                            out=ccw_template)
            ccw_template.close()

# Zuletzt bearbeitet: 2025-10-27
