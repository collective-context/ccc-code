"""CCC CODE exception classes."""


class CCWError(Exception):
    """Generic errors."""

    def __init__(self, msg):
        Exception.__init__(self)
        self.msg = msg

    def __str__(self):
        return self.msg


class CCWConfigError(CCWError):
    """Config related errors."""
    pass


class CCRuntimeError(CCWError):
    """Generic runtime errors."""
    pass


class CCWArgumentError(CCWError):
    """Argument related errors."""
    pass

# Zuletzt bearbeitet: 2025-10-27
