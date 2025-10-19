"""
CCC CODE plugins module
"""

def load(app):
    """Load all plugins"""
    from ccw.cli.plugins import (
        clean, debug, import_slow_log, info, log, maintenance,
        secure, site, site_backup, site_clone, site_create,
        site_update, stack, stack_migrate, stack_pref,
        stack_services, stack_upgrade, update
    )
    
    # Register all plugin controllers
    clean.load(app)
    debug.load(app)
    import_slow_log.load(app)
    info.load(app)
    log.load(app)
    maintenance.load(app)
    secure.load(app)
    site.load(app)
    stack.load(app)
    update.load(app)
