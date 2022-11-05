import os

from flask import Flask, render_template, request, flash, redirect, session, g, abort
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
import requests
import json
from forms import UserAddForm, LoginForm
from models import db, connect_db, User, Groceries, Favorites
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

    groc_count = (Groceries.query.filter(Groceries.user_id == g.user.id).count())
    fav_count = (Groceries.query.filter(Groceries.user_id == g.user.id).count())


    return render_template('users.html', user=user, groc_count = groc_count, fav_count = fav_count)


# TO DO: Finish favorites page and functionality
@app.route('/user/favorites')
def show_user_favorites():
    if g.user:

        favs = Favorites.query.filter(Favorites.user_id == g.user.id).all()
        # fav_ids = [fav.recipe_id for fav in favs]

        return render_template('favorites.html', favs = favs)


# TO DO: Finish grocery page and functionality
@app.route('/user/groceries')
def show_user_groceries():
    if g.user:
        user_groc = (Groceries.query.filter(Groceries.user_id == g.user.id).all())
        return render_template('groceries.html', user_groc = user_groc)






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

        baseURL = f'https://api.spoonacular.com/recipes/{rec_id}/information?includeNutrition=false'

        resp =  requests.get(baseURL, {'apiKey': API_KEY})

        recipe = resp.json()

        print(recipe)

        user_groc = (Groceries.query.filter(Groceries.user_id == g.user.id).all())
        groc_ids = [groc.ingredient_id for groc in user_groc]

        return render_template('recipe-details.html', recipe =recipe, groc_ids = groc_ids)
    
    else:
        form = LoginForm()
        return render_template('login.html', form = form)


@app.route("/recipes/search/<query>/")
@app.route("/recipes/search/<query>/<intol>")
def query_search_recipes(query, intol=None):
    """Query recipes with search term and return json response"""
    print(' QUERY: >>>>>>>>>>>>>>>>>>>>')
    print(query)

    headers = {
        'apiKey': API_KEY,
        'query': query,
        'number': '4',
        }

    if intol is not None:
        headers['intolerances'] = intol

    print(headers)

    baseURL = 'https://api.spoonacular.com/recipes/complexSearch'

    resp =  requests.get(baseURL, headers)

    recipes = resp.json()
    print(' RESP JSON: >>>>>>>>>>>>>>>>>>>>>')
    print(recipes)

    return recipes


@app.route('/groceries/add/<ings>', methods=["POST"])
def add_ingredients(ings):
    # make list
    ings = list(ings.split(','))
    print('ings:', ings)

    # get existing ingredients in groceries
    user_groc = (Groceries.query.filter(Groceries.user_id == g.user.id).all())
    groc_ids = [groc.ingredient_id for groc in user_groc]

    # Filter out existing ingredients
    new_ing = [ing for ing in ings if int(ing) not in groc_ids]

    # Add new ingredients to db
    for ing in new_ing:
        baseURL = f'https://api.spoonacular.com/food/ingredients/{ing}/information?amount=1'
        resp =  requests.get(baseURL, {'apiKey': API_KEY})
        ingredient = resp.json()
        print('ingredients check: ', ingredient)
        db.session.add(Groceries(user_id = g.user.id, ingredient_id = ing, name = ingredient["name"]))

    db.session.commit()

    return ings




@app.route('/groceries/remove/<int:ing_id>', methods = ['POST'])
def remove_ingredient(ing_id):
    del_ing = (Groceries.query.filter(Groceries.user_id == g.user.id, Groceries.ingredient_id == ing_id).one())

    db.session.delete(del_ing)
    db.session.commit()

    return redirect('/user/groceries')
    
@app.route('/groceries/remove/all', methods = ['POST'])
def remove_all_ingredients():
    Groceries.query.filter(Groceries.user_id == g.user.id).delete()
    db.session.commit()

    return "successfully deleted"

# Favorites

@app.route('/messages/<int:rec_id>/favorite', methods=['POST'])
def add_favorite(rec_id):
    """Toggle a favorite recipe for the currently-logged-in user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    favs = Favorites.query.filter(Favorites.user_id == g.user.id).all()
    fav_ids = [fav.recipe_id for fav in favs]

    if rec_id not in fav_ids:
        #Call to save for Fav card
        baseURL = f'https://api.spoonacular.com/recipes/{rec_id}/information?includeNutrition=false'
        resp =  requests.get(baseURL, {'apiKey': API_KEY})
        recipe = resp.json()
        # Save info to db
        new_fav = Favorites(user_id = g.user.id, recipe_id = rec_id, name = recipe['title'], img_url = recipe['image'])
        print(' new fav >>>>>>>>>>>>>>>>>>>>>', new_fav)
        db.session.add(new_fav)

    else:
        print('else statement >>>>>>>>>>>>>>>>>>>')
        del_fav = Favorites.query.filter(Favorites.user_id == g.user.id, Favorites.recipe_id == rec_id).one()
        db.session.delete(del_fav)

    db.session.commit()

    return 'sucess'






