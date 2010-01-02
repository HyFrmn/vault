from vault.tests import *

class TestApplicationController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='application', action='index'))
        # Test response...
