"""CCC CODE bootstrapping."""

# All built-in application controllers should be imported, and registered
# in this file in the same way as CCCBaseController.


from ccc.cli.controllers.base import CCCBaseController


def load(app):
    app.handler.register(CCCBaseController)
