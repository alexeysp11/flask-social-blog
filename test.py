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
        return user, post

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
                follow_redirects=True
            )
            assert response.status == '200 OK'
    
    # Ensure that login page redirects to the feed page if username is correct
    def test_login_redirect_if_username_is_correct(self):
        with self.app.test_client() as client:
            response = self.client.post(
                '/login',
                data=dict(username="admin", password="admin"),
                follow_redirects=True
            )
            # Feed page is the page for authenticated users, 
            # and its url is '/', '/home' and '/feed'
            assert request.path == '/'
    
    # Ensure that there's a user named admin in db 
    def test_login_correct_user_in_db(self):
        with self.app.test_client() as client:
            response = self.client.post(
                '/login',
                data=dict(username="admin", password="admin"),
                follow_redirects=True
            )
            user = User.query.filter_by(username="admin").first()
            assert "admin" == user.username
    
    # Ensure that there's no user named wrong in db 
    def test_login_incorrect_user_in_db(self):
        with self.app.test_client() as client:
            response = self.client.post(
                '/login',
                data=dict(username="wrong", password="wrong"),
                follow_redirects=True
            )
            user = User.query.filter_by(username="wrong").first()
            assert user is None
    
    # Ensure that the page for new post redirects to the feed
    def test_new_post_redirect_to_feed(self): 
        with self.app.test_client() as client:
            response = self.client.post(
                '/new',
                data=dict(title="test", text="test"),
                follow_redirects=True
            )
            assert request.path == '/'


if __name__ == '__main__':
    unittest.main()
