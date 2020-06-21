from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.Integer)
    email = db.Column(db.String(120), index=True, unique=True)
    username = db.Column(db.String(64), index=True, unique=True)
    name = db.Column(db.String(150))
    password = db.Column(db.String(50))
    #admin = db.Column(db.Boolean)

    def __repr__(self):
        return '<User {}>'.format(self.username)
