"""
Tests for main CCC application
"""

import pytest
from ccc.main import CCCApp


def test_app_creation():
    """Test that app can be created"""
    with CCCApp() as app:
        assert app is not None


def test_app_version():
    """Test app version"""
    with CCCApp() as app:
        assert app.config.get("ccc", "version") == "1.0.0"
