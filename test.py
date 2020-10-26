import unittest
from flask import url_for, request
from flask_testing import TestCase
from flask_login import current_user
from app import app, db
from app.models import User, Post

class BaseTestCase(TestCase):
    """A base test case."""

    def create_app(self):
        app.config['TESTING'] = True

        db.init_app(app)
        from app.models import User, Post
        with app.app_context():
            db.create_all()
        
        return app

    def setUp(self):
        db.create_all()
        
        post = Post(title="Test post", 
                    text="This is a test. Only a test.")
        
        user = User(firstname="admin", 
                    lastname="admin",
                    username="admin",
                    email="admin@example.com", 
                    password="admin")
        
        db.session.add(user)
        user.posts.append(post)
        db.session.commit()

    def tearDown(self):
        user = User.query.filter_by(username='admin').first()
        posts = Post.query.filter_by(author=user).all()

        db.session.delete(user)
        for post in posts: 
            db.session.delete(post)
        db.session.commit()
        

class FlaskTestCase(BaseTestCase):

    # Ensure that login page has status code 200
    def test_login_status200(self):
        with self.app.test_client() as client:
            response = self.client.post(
                '/login',
                data=dict(username="admin", password="admin"),
                follow_redirects=False
            )
            assert response.status == '200 OK'


if __name__ == '__main__':
    unittest.main()
