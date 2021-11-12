from re import template
from flask import Flask, render_template, redirect, session, flash, jsonify, g, request
import requests
from flask_debugtoolbar import DebugToolbarExtension
from models import Drink, connect_db, db, User, Drink
from forms import UserAddForm, DrinkAddForm, DrinkEditForm, LoginForm
from sqlalchemy.exc import IntegrityError
# from secrets import API_SECRET_KEY

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///drinks"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

CURR_USER_KEY = "curr_user"

API_BASE_URL = "http://www.thecocktaildb.com/api/json/v2/1/"

connect_db(app)
db.drop_all()
db.create_all()
db.session.commit()

toolbar = DebugToolbarExtension(app)

### API STUFF
# BASE URL FOR SEARCH  http://www.thecocktaildb.com/api/json/v1/1/search.php?s=

    # data = res.json()
    # drink = data["results"][0]
    
    # return drink

@app.route('/')
def index_page():
    drinks = Drink.query.all()
    return render_template('index.html', drinks=drinks)

# QUERIES API AND RETURNS SPECIFIED INFO
@app.route('/drink_name', methods=["GET", "POST"])
def get_drink():
    """Return drink for specified drink"""
    key = '9973533'
    strDrink = request.form["strDrink"]
    res = requests.get(f"{API_BASE_URL}/search.php?s={strDrink}",
                       params={'key': key, 'strDrink': strDrink})
    data = res.json()
    name = data["drinks"][0]["strDrink"]
    tags = data["drinks"][0]["strTags"]
    category = data["drinks"][0]["strCategory"]
    alcoholic = data["drinks"][0]["strAlcoholic"]
    glass = data["drinks"][0]["strGlass"]
    instructions = data["drinks"][0]["strInstructions"]
    ingredient1 = data["drinks"][0]["strIngredient1"]
    ingredient2 = data["drinks"][0]["strIngredient2"]
    ingredient3 = data["drinks"][0]["strIngredient3"]
    ingredient4 = data["drinks"][0]["strIngredient4"]
    ingredient5 = data["drinks"][0]["strIngredient5"]
    measure1 = data["drinks"][0]["strMeasure1"]
    measure2 = data["drinks"][0]["strMeasure2"]
    measure3 = data["drinks"][0]["strMeasure3"]
    measure4 = data["drinks"][0]["strMeasure4"]
    measure5 = data["drinks"][0]["strMeasure5"]
    image = data["drinks"][0]["strDrinkThumb"]
    drink = {'name': name, 'tags':tags, 'category': category,'alcoholic': alcoholic, 'glass': glass, 'instructions': instructions, 'ingredient1': ingredient1, 'ingredient2': ingredient2, 'ingredient3': ingredient3, 'ingredient4': ingredient4, 'ingredient5': ingredient5, 'measure1': measure1, 'measure2': measure2, 'measure3': measure3, 'measure4': measure4, 'measure5': measure5, 'image': image}
    return render_template('show_drinks.html', drink=drink)

# ****** THESE WERE CREATED WITH ADDING YOUR OWN DRINKS IN MIND, RETURN TO THIS LATER ******
# @app.route('/api/drinks')
# def list_all_drinks():
#     """Return JSON w/ all drinks"""

#     all_drinks = [drink.serialize() for drink in Drink.query.all()]
#     return jsonify(drinks=all_drinks)

# @app.route('/api/drinks/<int:id>')
# def get_drink(id):
#     """Returns JSON for one drink in particular"""
#     drink = Drink.query.get_or_404(id)
#     return jsonify(drink=drink.serialize())

# #THIS CREATE_DRINK ONLY RETURNS JSON
# @app.route('/drink', methods=["GET", "POST"])
# def create_drink():
#     """Creates a new drink from form data and returns JSON of that created drink"""
    
#     name = request.json["name"]
#     ingredients = request.json["ingredients"]
#     image_url = request.json["image_url"]
    
#     new_drink = Drink(name=name, ingredients=ingredients, image_url=image_url)
    
#     db.session.add(new_drink)
#     db.session.commit()

#     response_json = jsonify(drink=new_drink.serialize())
#     return (response_json, 201)

#     # return render_template("add_drink.html")

# @app.route('/api/drinks/<int:id>', methods=["PATCH"])
# def update_drink(id):
#     """Updates a particular drink and responds w/ JSON of that updated drink"""
#     drink = Drink.query.get_or_404(id)
#     # MAY NEED FORM TO EDIT DRINK, HAVE TO CHANGE THIS CODE
#     # form = DrinkEditForm(obj=drink)
#     drink.name = request.json.get('name', drink.name)
#     drink.ingredients = request.json.get('ingredients', drink.ingredients)
#     drink.image = request.json.get('image', drink.image)
#     db.session.commit()
#     return jsonify(drink=drink.serialize())

# @app.route('/api/drinks/<int:id>', methods=["DELETE"])
# def delete_drink(id):
#     """Deletes a particular drink"""
#     drink = Drink.query.get_or_404(id)
#     db.session.delete(drink)
#     db.session.commit()
#     return jsonify(message="deleted")

# # THIS CREATE_DRINK WAS CREATED TO ADD YOUR OWN DRINK TO DB, NEED TO ADJUST
# @app.route('/add_drink', methods=["GET", "POST"])
# def add_drinks():
#     # drink = Drink.query.get_or_404(id)
#     form = DrinkAddForm()
#     name = db.session.query(Drink.name)
#     ingredients = db.session.query(Drink.ingredients)
#     image_url = db.session.query(Drink.image_url)

#     new_drink = Drink(name=name, ingredients=ingredients, image_url=image_url)
    
#     if form.validate_on_submit():
#         Drink.name = form.name.data
#         Drink.ingredients = form.ingredients.data
#         Drink.image_url = form.image_url.data
#         db.session.add(new_drink)
#         db.session.commit()
#         return redirect('/add_drink')
#     else:
#         return render_template("show_drinks.html", form=form, name=name, ingredients=ingredients, image_url=image_url)
    
# THIS IS A MESS, IDEK WHAT TO DO WITH THIS    

# @app.route('/show_drinks', methods=['GET'])
# def show_drinks():
#     """Shows all Drinks"""
#     if "user_id" not in session:
#         flash("Please login first!", "danger")
#         return redirect('/')
#     form = DrinkEditForm()
#     all_drinks = Drink.query.all()
#     if form.validate_on_submit():
#         drink = form.drink.data
#         new_drink = Drink(drink=drink, user_id=session['user_id'])
#         db.session.add(new_drink)
#         db.session.commit()
#         flash('Drink Created!', 'success')
#         return redirect('/show_drinks')

#     return render_template("show_drinks.html", form=form, drinks=all_drinks)

###############
# USER REGISTER, LOGIN, LOGOUT

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

    
@app.route('/register', methods=['GET', 'POST'])
def register_user():
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
    form = UserAddForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        new_user = User.register(username, password, first_name, last_name, email)

        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username taken.  Please pick another')
            return render_template('register.html', form=form)
        session['user_id'] = new_user.id
        flash('Welcome! Successfully Created Your Account!', "success")
        return redirect('/')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            flash(f"Welcome Back, {user.username}!", "primary")
            session['user_id'] = user.id
            return redirect('/drinks')
        else:
            form.username.errors = ['Invalid username/password.']
            return redirect('/')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()

    flash("You have successfully logged out.", 'success')
    return redirect("/login")
