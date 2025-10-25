"""
Tests for main CCC application
"""

import pytest
from ccc.main import CCCApp
from ccc import __version__


def test_app_creation():
    """Test that app can be created"""
    with CCCApp() as app:
        assert app is not None


def test_app_version():
    """Test app version"""
    with CCCApp() as app:
        assert app.config.get("ccc", "version") == __version__


def test_version_import():
    """Test version can be imported"""
    from ccc import __version__
    assert __version__ == "1.0.0"


def test_app_import():
    """Test CCCApp can be imported"""
    from ccc import CCCApp
    assert CCCApp is not None
