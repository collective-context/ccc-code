"""Custom exceptions for ccb"""

class CCBError(Exception):
    """Base exception for ccb"""
    pass


class CCBConfigError(CCBError):
    """Configuration related errors"""
    pass


class CCBRuntimeError(CCBError):
    """Runtime errors"""
    pass
