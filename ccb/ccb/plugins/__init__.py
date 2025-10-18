"""CCB Plugins Package"""


def load_plugins(app):
    """Load all plugins"""
    from ccb.plugins.check import load as load_check
    from ccb.plugins.debug import load as load_debug
    
    load_check(app)
    load_debug(app)
