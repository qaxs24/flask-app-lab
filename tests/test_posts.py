import unittest
from app import create_app, db
from app.posts.models import Post, CategoryEnum
from app.models import User
from config import TestingConfig
from werkzeug.security import generate_password_hash

class TestPosts(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        # Create a test user
        self.user = User(username='testuser', email='test@example.com', password=generate_password_hash('password'))
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def login(self):
        return self.client.post('/login', data=dict(
            username='testuser',
            password='password'
        ), follow_redirects=True)

    def test_create_post(self):
        self.login()
        response = self.client.post('/post/create', data=dict(
            title='Test Post',
            content='This is a test post content',
            category='news',
            enabled='y',
            publish_date='2023-01-01T12:00'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        # Check if post exists in DB
        post = Post.query.first()
        self.assertIsNotNone(post)
        self.assertEqual(post.title, 'Test Post')
        self.assertEqual(post.author, 'testuser')

    def test_read_post(self):
        post = Post(title='Read Test', content='Content', category=CategoryEnum.news)
        db.session.add(post)
        db.session.commit()
        
        response = self.client.get(f'/post/{post.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Read Test', response.data)

    def test_update_post(self):
        self.login()
        post = Post(title='Update Test', content='Content', category=CategoryEnum.news)
        db.session.add(post)
        db.session.commit()
        
        response = self.client.post(f'/post/{post.id}/update', data=dict(
            title='Updated Title',
            content='Updated Content',
            category='tech',
            enabled='y',
            publish_date='2023-01-01T12:00'
        ), follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        updated_post = db.session.get(Post, post.id)
        self.assertEqual(updated_post.title, 'Updated Title')
        self.assertEqual(updated_post.category, CategoryEnum.tech)

    def test_delete_post(self):
        self.login()
        post = Post(title='Delete Test', content='Content', category=CategoryEnum.news)
        db.session.add(post)
        db.session.commit()
        
        response = self.client.post(f'/post/{post.id}/delete', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(db.session.get(Post, post.id))

    def test_create_post_without_login(self):
        response = self.client.post('/post/create', data=dict(
            title='Test Post',
            content='Content',
            category='news'
        ), follow_redirects=True)
        # Should redirect to login page
        self.assertIn(b'Please log in', response.data)

if __name__ == '__main__':
    unittest.main()
