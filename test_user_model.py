"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

        self.u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        self.u2 = User(
            email="test2@test2.com",
            username="testuser2",
            password="HASHED_PASSWORD2"
        )

        db.session.add_all([self.u, self.u2])
        db.session.commit()


    def test_user_model(self):
        """Does basic model work?"""

        # User should have no messages & no followers
        self.assertEqual(len(self.u.messages), 0)
        self.assertEqual(len(self.u.followers), 0)

    def test_repr(self):
        """Tests the __repr__ method"""

        self.assertEqual(repr(self.u), f"<User #{self.u.id}: {self.u.username}, {self.u.email}>")

    def test_is_following(self):
        """Tests if u2 is followed by u"""
        
        self.u.following.append(self.u2)

        self.assertIn(self.u2, self.u.following)

    def test_is_not_following(self):
        """Tests if u2 is not following u"""

        self.assertNotIn(self.u2, self.u.following)

    def test_is_followed_by(self):
        """Tests if u2 is following u"""

        self.u.followers.append(self.u2)

        self.assertIn(self.u2, self.u.followers)

    def test_is_not_followed_by(self):

        self.assertNotIn(self.u2, self.u.followers)

    def test_user_authenticate(self):

        u3 = User(
            email="test2@test3.com",
            username="testuser3",
            password="HASHED_PASSWORD3"
        )
        db.session.commit()

        user = User.signup(u3.username, u3.email, u3.password, u3.image_url)
        auth_user_username = User.authenticate("mike", user.password)
        auth_user_password = User.authenticate(user.username, "WRONG_PASS")
        auth_user_complete = User.authenticate(u3.username, u3.password)

        self.assertNotEqual(user, auth_user_username)
        self.assertIsNot(user, auth_user_password)
        self.assertIs(user, auth_user_complete)

