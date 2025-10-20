import unittest
from run import app 

class PortfolioBlueprintTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        self.client = app.test_client()

    def test_resume_page(self):
        """Тест доступності сторінки резюме."""
        response = self.client.get("/resume")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Full-stack", response.data)   
    
    def test_contacts_page(self):
        """Тест доступності сторінки контактів."""
        response = self.client.get("/contacts")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Email", response.data)

if __name__ == "__main__":
    unittest.main()