import os

from flask import Flask, render_template, request, flash, redirect, session, g, abort
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
import requests
import json
from forms import UserAddForm, LoginForm
from models import db, connect_db, User
from secret_key import SECRET_KEY, API_KEY


CURR_USER_KEY = "curr_user"

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///mygrub'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', SECRET_KEY)
app.config['SESSION_COOKIE_SAMESITE'] = None


toolbar = DebugToolbarExtension(app)

connect_db(app)

# db.drop_all()
db.create_all()

##############################################################################
# User signup/login/logout

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
       

        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:           
            do_login(user)
    
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    """Handle logout of user."""
    do_logout()
    flash('Logout Successful', 'success')
    return redirect('/login')


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('signup.html', form=form)

##############################################################################
# User Pages


#ERROR 404 for js file???

@app.route('/user/<int:user_id>')
def show_user_profile(user_id):

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = User.query.get_or_404(user_id)

    return render_template('users.html', user=user)


# TO DO: Finish favorites page and functionality
@app.route('/user/favorites')
def show_user_favorites():
    if g.user:
        return render_template('favorites.html')


# TO DO: Finish grocery page and functionality
@app.route('/user/groceries')
def show_user_groceries():
    if g.user:
        return render_template('groceries.html')






##############################################################################
# Homepage and error pages
# TO DO: Add errors page

@app.route("/")
def homepage():
    """Show homepage:
    """
    if g.user:
        
        return render_template('recipes.html')

    else:
        form = LoginForm()
        return render_template('login.html', form = form)


##############################################################################
# Recipes Handling

@app.route("/recipes/<int:rec_id>/details")
def get_recipe_details(rec_id):
    """Show details of recipe"""
    if g.user:
        headers = {
            'apiKey': API_KEY,
            }
        info = f"/recipes/{rec_id}/information"
    
        baseURL = 'https://api.spoonacular.com'

        resp =  requests.get(baseURL + info, headers = headers)

        recipe = resp.json()

        return render_template('recipe-details.html', recipe =recipe)
    
    else:
        form = LoginForm()
        return render_template('login.html', form = form)



@app.route("/recipes/search/<query>")
def query_search_recipes(query):
    """Query recipes with search term and return json response"""
    print(' QUERY: >>>>>>>>>>>>>>>>>>>>')
    print(query)

    headers = {
        'apiKey': API_KEY,
        'query': query,
        'number': '4'
        }

    baseURL = 'https://api.spoonacular.com/recipes/complexSearch'

    resp =  requests.get(baseURL, headers)

    recipes = resp.json()
    print(' RESP JSON: >>>>>>>>>>>>>>>>>>>>>')
    print(recipes)

    return recipes