"""
Pytest configuration and fixtures
"""

import pytest
from ccc.main import CCCApp


@pytest.fixture
def app():
    """App fixture"""
    with CCCApp() as app:
        yield app
