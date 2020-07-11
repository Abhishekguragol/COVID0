from app import db, login
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.Integer)
    email = db.Column(db.String(120), index=True, unique=True)
    username = db.Column(db.String(64), index=True, unique=True)
    name = db.Column(db.String(150))
    password = db.Column(db.String(50))
    #admin = db.Column(db.Boolean)

    def __repr__(self):
        return '<User {}>'.format(self.username)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Business(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.Integer, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    username = db.Column(db.String(64), index=True, unique=True)
    name = db.Column(db.String(150))
    location = db.Column(db.String(150))
    password = db.Column(db.String(50))
    #verifier = db.Column(db.Boolean)
    #admin = db.Column(db.Boolean)

    def __repr__(self):
        return '<Business Name {}>'.format(self.name)


class BusinessDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.Integer)   ## this public_id must be same as Business class
    verifier = db.Column(db.Boolean)
    rule1 = db.Column(db.Boolean)
    rule2 = db.Column(db.Boolean)
    rule3 = db.Column(db.Boolean)
    adnl_rule = db.Column(db.String()) #pass a dictionary
    #admin = db.Column(db.Boolean)

    def __repr__(self):
        return '<Business details ID {}>'.format(self.public_id)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_public_id = db.Column(db.Integer)   ## this public_id must be same as Business class
    business_public_id = db.Column(db.Integer)
    text = db.Column(db.String(160))
    rating = db.Column(db.Integer)    


    def __repr__(self):
        return '<Business details ID {}>'.format(self.public_id)