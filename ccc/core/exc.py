"""CCC CODE exception classes."""


class CCCError(Exception):
    """Generic errors."""

    def __init__(self, msg):
        Exception.__init__(self)
        self.msg = msg

    def __str__(self):
        return self.msg


class CCCConfigError(CCCError):
    """Config related errors."""
    pass


class CCCRuntimeError(CCCError):
    """Generic runtime errors."""
    pass


class CCCArgumentError(CCCError):
    """Argument related errors."""
    pass
