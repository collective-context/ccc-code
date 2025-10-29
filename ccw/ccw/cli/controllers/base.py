"""CCC CODE base controller."""

from cement.core.controller import CementBaseController, expose

from ccw.core.variables import CCWVar

VERSION = CCWVar.ccw_version

BANNER = """
CCC CODE v%s
Copyright (c) 2024 CCC CODE.
""" % VERSION


class CCWBaseController(CementBaseController):
    class Meta:
        label = 'base'
        description = ("An essential toolset that eases CCC CODE "
                       "site and server administration with Nginx")
        arguments = [
            (['-v', '--version'], dict(action='version', version=BANNER)),
        ]

    @expose(hide=True)
    def default(self):
        self.app.args.print_help()

# Zuletzt bearbeitet: 2025-10-27
