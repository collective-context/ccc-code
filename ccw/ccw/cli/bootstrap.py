"""CCC CODE bootstrapping."""

# All built-in application controllers should be imported, and registered
# in this file in the same way as CCWBaseController.


from ccw.cli.controllers.base import CCWBaseController


def load(app):
    app.handler.register(CCWBaseController)
