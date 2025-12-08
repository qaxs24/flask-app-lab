import unittest
from app import create_app, db
from app.models import User

class UsersBlueprintTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register_page_loads(self):
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'\xd0\xa0\xd0\xb5\xd1\x94\xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd1\x86\xd1\x96\xd1\x8f', response.data) # 'Реєстрація' encoded

    def test_login_page_loads(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'\xd0\x92\xd1\x85\xd1\x96\xd0\xb4', response.data) # 'Вхід' encoded

    def test_user_registration(self):
        response = self.client.post('/register', data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password',
            'confirm_password': 'password'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        user = User.query.filter_by(username='testuser').first()
        self.assertIsNotNone(user)
        self.assertTrue(user.check_password('password'))

    def test_login_logout(self):
        # Create user first
        user = User(username='testuser', email='test@example.com')
        user.set_password('password')
        db.session.add(user)
        db.session.commit()

        # Login
        response = self.client.post('/login', data={
            'username': 'testuser',
            'password': 'password'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        # Check if redirected to account page (check for 'Профіль' text)
        self.assertIn(b'\xd0\x9f\xd1\x80\xd0\xbe\xd1\x84\xd1\x96\xd0\xbb\xd1\x8c', response.data)

        # Logout
        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        # Check if redirected to login page
        self.assertIn(b'\xd0\x92\xd1\x85\xd1\x96\xd0\xb4', response.data)

if __name__ == "__main__":
    unittest.main()
