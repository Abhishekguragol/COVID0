from app import app
from app.models import User
from app import db
from flask import request, jsonify, make_response, render_template, redirect,url_for
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import jwt
import datetime
from functools import wraps

# Home page
@app.route('/')
@app.route('/index')
def index():
    return "<h1> Welcome </h1>"



def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        token = None

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})

        try:
            data = jwt.decode(token, app.config[SECRET_KEY])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'token is invalid'})

        return f(current_user, *args, **kwargs)

    return decorator


# Sing Up route for frontend request, response in json
@app.route('/register', methods=['GET', 'POST'])
def signup_user():
    print("In register")
    if request.method == 'POST':
        print("Register Sub")
        data = request.get_json()
        print(request.form)

        hashed_password = generate_password_hash(request.form['password'], method='sha256')

        new_user = User(public_id=str(uuid.uuid4()), name=request.form['name'], email=request.form['email'], username=request.form['username'], password=hashed_password)

        try:
            
            db.session.add(new_user)
            
            db.session.commit()
            
            return redirect(url_for('index'))

        except:
            return jsonify({'message': 'Unsuccessful registration'})

    return render_template('signup.html', title='Sign Up')


# Login route for frontend request, response in json
@app.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        #auth = request.authorization

        if not request.form["username"] or not request.form["password"]:
            return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

        user = User.query.filter_by(username=request.form["username"]).first()

        if check_password_hash(user.password, request.form["password"]):
            token = jwt.encode({'public_id': user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
            return render_template('home.html', title='Sign Up')
        else:
            return make_response('could not verify',  401, {'WWW.Authentication': 'Basic realm: "login required"'})
    return render_template('login.html', title='Sign Up')

# To list all users (use for testing)
@app.route('/all_users', methods=['GET'])
def get_all_users():

    users = User.query.all()
    #user1 = User.query.filter_by(username="sidd").first()
    result = []

    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['password'] = user.password
        user_data['email'] = user.email
        user_data['username'] = user.username

    result.append(user_data)

    return jsonify({'users': result})
