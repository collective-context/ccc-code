"""CCC CODE base controller."""

from cement.core.controller import CementBaseController, expose

from ccc.core.variables import CCCVar

VERSION = CCCVar.ccc_version

BANNER = """
CCC CODE v%s
Copyright (c) 2024 Collective Context Commander.
""" % VERSION


class CCCBaseController(CementBaseController):
    class Meta:
        label = 'base'
        description = ("An essential toolset that eases WordPress "
                       "site and server administration with Nginx")
        arguments = [
            (['-v', '--version'], dict(action='version', version=BANNER)),
        ]

    @expose(hide=True)
    def default(self):
        self.app.args.print_help()
