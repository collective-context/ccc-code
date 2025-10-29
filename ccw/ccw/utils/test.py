"""Testing utilities for CCC CODE"""
from cement.utils import test
from ccw.cli.main import CCWTestApp


class CCWTestCase(test.CementTestCase):
    app_class = CCWTestApp

    def setUp(self):
        """Override setup actions (for every test)."""
        super(CCWTestCase, self).setUp()

    def tearDown(self):
        """Override teardown actions (for every test)."""
        super(CCWTestCase, self).tearDown()

# Zuletzt bearbeitet: 2025-10-27
