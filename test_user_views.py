"""User View tests"""

#  FLASK_ENV=production python -m unittest test_user_views.py

import os
from unittest import TestCase

from models import db, connect_db, User, Groceries, Favorites
# from bs4 import BeautifulSoup

os.environ['DATABASE_URL'] = "postgresql:///mygrub_test"

# import app
from app import app, CURR_USER_KEY

db.create_all()

# so forms ignore CSRF

app.config['WTF_CSRF_ENABLED'] = False


class MessageViewTestCase(TestCase):
    """TEst views for messages"""

    def setUp(self):
        """Create test client, and sample data"""

        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",
                                    email="test@test.com",
                                    password="testuser")
        self.testuser_id = 8989
        self.testuser.id = self.testuser_id

        
        db.session.commit()


    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp 



    def test_add_groceries(self):

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id

            resp = c.post("/groceries/add/1001", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            groc = Groceries.query.filter(Groceries.user_id == self.testuser_id).all()
            self.assertEqual(len(groc), 1)
            self.assertEqual(groc[0].user_id, self.testuser_id)
            self.assertEqual(groc[0].name, 'butter')

    def test_add_favorites(self):

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id

            resp = c.post("/recipes/654812/favorite", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            favs = Favorites.query.filter(Favorites.user_id == self.testuser_id).all()
            self.assertEqual(len(favs), 1)
            self.assertEqual(favs[0].user_id, self.testuser_id)
            self.assertEqual(favs[0].recipe_id, 654812)
            self.assertEqual(favs[0].name, 'Pasta and Seafood')
            self.assertIsNotNone(favs[0].img_url)

    def test_unauthorized_user_page_access(self):
        # self.setup_followers()
        with self.client as c:

            resp = c.get(f"/user/{self.testuser_id}", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("testuser", str(resp.data))
            self.assertIn("Access unauthorized", str(resp.data))

      ########################
     # Setup for future test#
    ########################

    def setup_groceries(self):
        g1 = Groceries(user_id = self.testuser_id, ingredient_id = 5062, name = 'chicken breasts')
        g2 = Groceries(user_id = self.testuser_id, ingredient_id = 2009, name = 'chilli powder')
        g3 = Groceries(user_id = self.testuser_id, ingredient_id = 2047, name = 'table salt')
         
        db.session.add_all([g1, g2, g3])
        db.session.commit()
     
    def setup_favorites(self):
        f1 = Favorites(user_id = self.testuser_id, recipe_id = 654812, name = 'Pasta and Seafood', img_url = 'https://spoonacular.com/recipeImages/654812-556x370.jpg')
        f2 = Favorites(user_id = self.testuser_id, recipe_id = 662151, name = 'Sugar Cookies', img_url = 'https://spoonacular.com/recipeImages/662151-556x370.jpg')
        f3 = Favorites(user_id = self.testuser_id, recipe_id = 637876, name = 'Chicken 65', img_url = 'https://spoonacular.com/recipeImages/637876-556x370.jpg')
        f4 = Favorites(user_id = self.testuser_id, recipe_id = 555555, name = 'Tester', img_url = 'https://spoonacular.com/recipeImages/637876-556x370.jpg')


        db.session.add_all([f1, f2, f3])
        db.session.commit()

    #########################

    def test_users_show(self):
        self.setup_groceries()
        self.setup_favorites()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id

            resp = c.get(f"/user/{self.testuser_id}")
            self.assertEqual(resp.status_code, 200)

            self.assertIn("testuser", str(resp.data))
            # for amount of favorites
            self.assertIn("4", str(resp.data))
            # for amount of groceries
            self.assertIn("3", str(resp.data))


    def test_show_groceries(self):
        self.setup_groceries()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id

            resp = c.get('/user/groceries')

            self.assertEqual(resp.status_code, 200)
            self.assertIn('testuser', str(resp.data))

            self.assertIn('chicken breasts', str(resp.data))
            self.assertIn('table salt', str(resp.data))
            self.assertNotIn('pepper', str(resp.data))

    def test_remove_grocery(self):
        self.setup_groceries()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id

            resp1 = c.post('/groceries/remove/5062')
            self.assertEqual(resp1.status_code, 302)

            resp2 = c.get('/user/groceries')
            self.assertEqual(resp2.status_code, 200)

            self.assertNotIn('chicken breasts', str(resp2.data))
            self.assertIn('table salt', str(resp2.data))
            self.assertIn('chilli powder', str(resp2.data))

    def test_remove_all_groceries(self):
        self.setup_groceries()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id

            resp1 = c.post('/groceries/remove/all')
            self.assertEqual(resp1.status_code, 200)

            resp2 = c.get('/user/groceries')
            self.assertEqual(resp2.status_code, 200)

            self.assertNotIn('chicken breasts', str(resp2.data))
            self.assertNotIn('table salt', str(resp2.data))
            self.assertNotIn('chilli powder', str(resp2.data))


    def test_show_favorites(self):
        self.setup_favorites()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id

            resp = c.get('/user/favorites')

            self.assertEqual(resp.status_code, 200)
            self.assertIn('favorites', str(resp.data))

            self.assertIn('Pasta and Seafood', str(resp.data))
            self.assertIn('Chicken 65', str(resp.data))
            self.assertIn('https://spoonacular.com/recipeImages/662151-556x370.jpg', str(resp.data))

    