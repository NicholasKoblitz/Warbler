import os
from unittest import TestCase

from models import Follows, db, connect_db, Message, User, Likes

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

from app import app, CURR_USER_KEY

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False


class UserViewsTestCase(TestCase):

    def setUp(self):

        db.drop_all()
        db.create_all()
        self.client = app.test_client()


        self.testuser = User.signup(
            username="testuser",
            email="test@test.com",
            password="testuser",
            image_url=None
            )
        self.testuser_2 = User.signup("testuser_2", "test2@test.com", "testuser_2", None)

        db.session.commit()


        self.msg = Message(text="TestCase", user_id=self.testuser.id)
        db.session.add(self.msg)
        db.session.commit()

    def tearDown(self):
        db.session.rollback()


    def test_show_list_of_users(self):
        """Tests user search and page"""

        with self.client as c:
            resp = c.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("testuser", html)

            resp2 = c.get("/users?q=testuser")
            html2 = resp.get_data(as_text=True)


            self.assertEqual(resp2.status_code, 200)
            self.assertIn("testuser", html2)

    def test_user_profile(self):
        """Tests the user profile"""

        with self.client as c:
            resp = c.get(f"/users/{self.testuser.id}")
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn(self.msg.text, html)
            self.assertIn(self.testuser.username, html)

    def test_user_following_page(self):

        following = Follows(user_following_id=self.testuser.id, user_being_followed_id=self.testuser_2.id)
        db.session.add(following)
        db.session.commit()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            

            resp = c.get(f"/users/{self.testuser.id}/following")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("testuser_2", html)

    def test_user_followers_page(self):

        follower = Follows(user_following_id=self.testuser_2.id, user_being_followed_id=self.testuser.id)
        db.session.add(follower)
        db.session.commit()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.get(f"/users/{self.testuser.id}/followers")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("testuser_2", html)

    def test_user_following_unauthorized(self):

        following = Follows(user_following_id=self.testuser.id, user_being_followed_id=self.testuser_2.id)
        db.session.add(following)
        db.session.commit()

        with self.client as c:

            resp = c.get(f"/users/{self.testuser.id}/following", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Access unauthorized", html)


    def test_user_followers_unauthorized(self):

        follower = Follows(user_following_id=self.testuser_2.id, user_being_followed_id=self.testuser.id)
        db.session.add(follower)
        db.session.commit()

        with self.client as c:

            resp = c.get(f"/users/{self.testuser.id}/followers", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Access unauthorized", html)

    def test_user_likes_page(self):

        like = Likes(id=123, user_id=self.testuser.id, message_id=self.msg.id)

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.get(f"users/{self.testuser.id}/likes")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)

    def test_user_likes_page_unauthorized(self):
        """Tests if unauth user can view likes"""

        with self.client as c:
            resp = c.get(f"users/{self.testuser.id}/likes", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Access unauthorized", html)

    def test_show_user_profile_form(self):
        """Tests if profile update form shows"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.get("/users/profile", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)

    def test_user_profile_form_update(self):
        """Tests if profile update form updates the profile"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.post("/users/profile", data={"username": "TestUser"}, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("TestUser", html)

    def test_user_profile_unauthorized(self):
        """Tests that an unauthorized user can't update the profile"""

        with self.client as c:
            resp = c.get("/users/profile", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Access unauthorized", html)

            resp2 = c.post("/users/profile", data={"username": "TestUser"}, follow_redirects=True)
            html2 = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Access unauthorized", html)
            

