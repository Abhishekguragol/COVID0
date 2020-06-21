from app import app
from app.models import User
from app import db
from flask import request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import jwt
import datetime
from functools import wraps

# Home page
@app.route('/')
@app.route('/index')
def index():
    return "HCL Hackathon!"

#@app.route('/login')
#deflogin():
    #form = LoginForm()
    #return render_template('login.html', title='Sign In', form=form)

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
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = User(public_id=str(uuid.uuid4()), name=data['name'], email=data['email'], username=data['username'], password=hashed_password)

    try:
        db.session.add(new_user)
        db.session.commit()
    except:
        return jsonify({'message': 'Unsuccessful registration'})

    return jsonify({'message': 'registered successfully'})


# Login route for frontend request, response in json
@app.route('/login', methods=['GET', 'POST'])
def login_user():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

    user = User.query.filter_by(username=auth.username).first()

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id': user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token' : token.decode('UTF-8')})

    return make_response('could not verify',  401, {'WWW.Authentication': 'Basic realm: "login required"'})


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
