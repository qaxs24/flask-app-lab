import unittest
from run import app

class ProductsBlueprintTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()
    
    def test_products_page(self):
        """Тест сторінки зі списком товарів."""
        response = self.client.get("/products")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Products list", response.data)
        self.assertIn(b"Laptop", response.data)

if __name__ == "__main__":
    unittest.main()