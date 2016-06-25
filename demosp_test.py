import demosp
import unittest

class AppTest(unittest.TestCase):
    def setUp(self):
        self.app = demosp.app.test_client()

    def test_root(self):
        rv = self.app.get('/')
        assert 'Please log in to continue' in rv.data

if __name__ == '__main__':
    unittest.main()
