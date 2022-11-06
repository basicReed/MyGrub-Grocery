"""User model tests """

# python -m unittest test_user_model.py

import os

from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Favorites, Groceries

# connect to db
os.environ['DATABASE_URL'] = "postgresql:///mygrub_test"


from app import app


db.create_all()

class UserModelTestCase(TestCase):
    """Test views for messages"""

    def setUp(self):
        "Create test client, and add sample data"
        db.drop_all()
        db.create_all()

        # Make test users and commit to db
        u1 = User.signup("test1", "email1@email.com", "password")
        uid1 = 1111
        u1.id = uid1

        u2 = User.signup("test2", "email2@email.com", "password")
        uid2 = 2222
        u2.id = uid2

        db.session.commit()

        # Query users
        u1 = User.query.get(uid1)
        u2 = User.query.get(uid2)

        # Set values
        self.u1 = u1
        self.uid1 = uid1

        self.u2 = u2
        self.uid2 = uid2

        self.client = app.test_client()

    def tearDown(self):
        """Tear down all settup variables"""
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        #New user should have no favorites or groceries
        self.assertEqual(len(u.favorites), 0)
        self.assertEqual(len(u.groceries), 0)
    

    #################
    # New User Tests
    #################


    def test_valid_signup(self):
        """Does signup and password hash work?"""
        # submit signup
        u_test = User.signup("testtesttest", "testtest@test.com", "password")
        uid = 9999
        u_test.id = uid
        db.session.commit()
        # call user/check inputs
        u_test = User.query.get(uid)
        self.assertIsNotNone(u_test)
        self.assertEqual(u_test.username, "testtesttest")
        self.assertEqual(u_test.email, "testtest@test.com")
        #Bcrypt string starts with $2b$
        self.assertTrue(u_test.password.startswith('$2b$'))

    # USERNAME TEST 
    # TO DO: Repeat username
    def test_invalid_username_signup(self):
        """Sign up with no username"""
        invalid = User.signup(None, "test@test.com", "password")
        uid = 8888
        invalid.id = uid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

        # with self.assertRaises(ValidationError) as context:
        #     User.signup("test1", "email123@email.com", "password")
        #     db.session.commit()


    # EMAIL TEST
    # TO DO: Repeat email
    def test_invalid_email_signup(self):
        """Sign up with no email"""
        invalid = User.signup("testtest", None, "password")
        uid = 7777
        invalid.id = uid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    #PASSWORDS TEST
    def test_invalid_password_signup(self):
        """Sign up with no password"""
        with self.assertRaises(ValueError) as context:
            User.signup("testtest", "email@email.com", "")
        
        with self.assertRaises(ValueError) as context:
            User.signup("testtest", "email@email.com", None)


    ######################
    # Authentication Tests
    ######################

    def test_valid_authentication(self):
        """Using correct login work?"""
        u = User.authenticate(self.u1.username, "password")
        self.assertIsNotNone(u)
        self.assertEqual(u.id, self.uid1)
    
    def test_invalid_username(self):
        """Login with wrong username work?"""
        self.assertFalse(User.authenticate("badusername", "password"))

    def test_wrong_password(self):
        """Login with wrong password work?"""  
        self.assertFalse(User.authenticate(self.u1.username, "badpassword"))

