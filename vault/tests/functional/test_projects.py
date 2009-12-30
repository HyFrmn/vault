from vault.tests import *

class TestProjectController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='project', action='index'))
        # Test response...
