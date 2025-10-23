"""Testing utilities for CCC CODE"""
from cement.utils import test
from ccc.cli.main import CCCTestApp


class CCCTestCase(test.CementTestCase):
    app_class = CCCTestApp

    def setUp(self):
        """Override setup actions (for every test)."""
        super(CCCTestCase, self).setUp()

    def tearDown(self):
        """Override teardown actions (for every test)."""
        super(CCCTestCase, self).tearDown()
