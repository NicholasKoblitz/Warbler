import os
from unittest import TestCase

from models import db, User, Message, Follows

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

from app import app

db.create_all()


class MessageModelTestCase(TestCase):

    def setUp(self):

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(self.u)
        db.session.commit()

        self.msg = Message(
            text="Test",
            user_id=self.u.id
        )

        db.session.add(self.msg)
        db.session.commit()

    def test_message_object(self):
        """Tests the Message Model"""

        self.assertEqual(len(Message.query.all()), 1)

    def test_message_to_user(self):
        """Tests the message to user relationship"""

        self.assertEqual(self.msg.user, User.query.filter(self.msg.user.id == self.u.id).first())

    def test_user_to_msg(self):
        """Tests the user to messages relationship"""

        self.assertEqual(self.u.messages[0], Message.query.filter(self.msg.user.id == self.u.id).first())