import unittest

from auth import app

class TestHomePage(unittest.TestCase):
  def test_non_loggedin_home_page(self):
    tester = app.test_client(self)
    response = tester.get('/', content_type='text/html')
    self.assertEqual(response.status_code, 200);
    # TODO: Test that all the links in the returned page
    # also work

if __name__ == '__main__':
  unittest.main();
