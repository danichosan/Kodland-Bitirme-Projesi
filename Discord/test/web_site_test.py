import unittest
from main import app

class WebSiteTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Drive My Career', response.data)

    def test_form_page(self):
        response = self.app.get('/form')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Form', response.data)

    def test_contact_page(self):
        response = self.app.get('/contact')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Iletisim', response.data)

if __name__ == '__main__':
    unittest.main()
