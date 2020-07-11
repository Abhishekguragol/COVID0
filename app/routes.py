from app import app
from app.models import User, Business, BusinessDetails, Comment
from app import db
from flask import request, jsonify, make_response, render_template, redirect,url_for
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import jwt
import datetime
from functools import wraps
from flask_login import current_user, login_user, login_required

## USER_VIEW
## Test username: tester
## Test password: tester123

## BUSINESS_VIEW
## Test username: biztester
## Test password: biztester123

# Landing page
@app.route('/')
@app.route('/index')
def index():
    return redirect(url_for('login_for_user'))


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
def signup_for_user():
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
            return redirect(url_for('login_for_user'))
            #return render_template('home.html', title='Sign Up')

        except:
            return jsonify({'message': 'Unsuccessful registration'})

    return render_template('signup.html', title='Sign Up')


# Login route for frontend request, response in json
@app.route('/login', methods=['GET', 'POST'])
def login_for_user():
    if current_user.is_authenticated:
        return redirect(url_for('home_user'))

    if request.method == 'POST':
        #auth = request.authorization

        if not request.form["username"] or not request.form["password"]:
            return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

        user = User.query.filter_by(username=request.form["username"]).first()

        if user:
            if check_password_hash(user.password, request.form["password"]) and user.username == request.form["username"]:
                token = jwt.encode({'public_id': user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
                login_user(user)
                return redirect(url_for('home_user'))

            else:
                return make_response('could not verify',  401, {'WWW.Authentication': 'Basic realm: "login required"'})

        else:
            return make_response('could not verify',  401, {'WWW.Authentication': 'Basic realm: "login required"'})

    return render_template('login.html', title='Sign Up')

# Home page upon login for user view -> still static, design the db and pull businesses data to display
@app.route('/home', methods=['GET', 'POST'])
@login_required
def home_user():
    # rendered from template, revert to API is there's time
    d = {}
    business = Business.query.all()
    business_details = BusinessDetails.query.all()
    
    for i in business:
        #print(i.public_id)
        for j in business_details:
            #print(j.public_id)
            if i.public_id == j.public_id:
                d[i.public_id] = {} 
                d[i.public_id]['rule1'] = j.rule1
                d[i.public_id]['rule2'] = j.rule2
                d[i.public_id]['rule3'] = j.rule3 
                d[i.public_id]['name'] = i.name    
    
    print(d)
    
    return render_template('cardindex_temp.html', title='You logged in woo', d=d)


# Business sign up page
@app.route('/business_signup', methods=['GET', 'POST'])
def business_signup():
    print("In Business register")
    if request.method == 'POST':
        print("Register Sub")
        data = request.get_json()
        print("REQUEST data:")
        print(request.form)

        hashed_password = generate_password_hash(request.form['password'], method='sha256')

        num = str(uuid.uuid4())

        new_user = Business(public_id=num, name=request.form['name'], email=request.form['email'], username=request.form['username'], password=hashed_password, location=request.form['location'])
        new_user_1 = BusinessDetails(public_id=num, verifier = False, rule1 = False, rule2 = False, rule3 = False, adnl_rule = "adnl rule")

        try:
            db.session.add(new_user)
            db.session.commit()
            print(new_user)

            db.session.add(new_user_1)
            db.session.commit()
            print(new_user_1)

            return redirect(url_for('business_login'))

            #return render_template('home.html', title='Sign Up')

        except:
            return jsonify({'message': 'Unsuccessful registration'})

#   return render_template('signup.html', title='Sign Up')
    return render_template('business_register.html', title='Business sign up page')


# Business sign up page
@app.route('/business_login', methods=['GET', 'POST'])
def business_login():
    print("In Business Login")
    if request.method == 'POST':
        #auth = request.authorization

        if not request.form["username"] or not request.form["password"]:
            return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

        user = Business.query.filter_by(username=request.form["username"]).first()

        if user:
            if check_password_hash(user.password, request.form["password"]) and user.username == request.form["username"]:
                token = jwt.encode({'public_id': user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
                #login_user(user)
                return redirect(url_for('home_business'))

            else:
                return make_response('could not verify',  401, {'WWW.Authentication': 'Basic realm: "login required"'})

        else:
            return make_response('could not verify',  401, {'WWW.Authentication': 'Basic realm: "login required"'})

    return render_template('business_login.html', title='Business Log in')


# Home page upon login for business view -> still static, design the db and pull businesses data to display
@app.route('/home_business/<public_id>', methods=['GET', 'POST'])
def home_business(public_id):
    biz = Business.query.filter_by(public_id=public_id).first()
    bizdetails = BusinessDetails.query.filter_by(public_id=public_id).first()
    comment = Comment.query.filter_by(business_public_id=public_id)

    ### passed queried data from db about business, its details and comments    
    return render_template('business_home_temp.html', title='You logged in woo', biz=biz, bizdetails=bizdetails, comment=comment)



# COVID Guidelines indexing based on search string
@app.route('/guidelines', methods=['GET', 'POST'])
def guidelines():
    print("In guidelines")
    if request.method == 'POST':
        #auth = request.authorization
        query = request.form["query"]

        if not query:
            return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})


        from covid_guidelines import covid_guidelines
        response = covid_guidelines.find_docs(query)
        print(response)
        return jsonify({'json': response})

             
    return render_template('guidelines.html', title='GUIDELINES')




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
