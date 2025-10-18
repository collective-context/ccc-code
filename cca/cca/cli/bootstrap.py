"""CCA bootstrapping."""

# All built-in application controllers should be imported, and registered
# in this file in the same way as CCABaseController.

from cca.cli.controllers.base import CCABaseController


def load(app):
    app.handler.register(CCABaseController)
