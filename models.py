from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:Htown2022.@cargodb.cluster-ckpufaeekpgg.us-east-1.rds.amazonaws.com/CargoDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Cargo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Float)
    cargotype = db.Column(db.String(50))
    departure = db.Column(db.Date)
    arrival = db.Column(db.Date)
    shipid = db.Column(db.Integer, db.ForeignKey('spaceship.id'))
    ship = db.relationship('Spaceship', backref=db.backref('cargos', lazy=True))

class Spaceship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    maxweight = db.Column(db.Float)
    captainid = db.Column(db.Integer, db.ForeignKey('captain.id'))
    captain = db.relationship('Captain', backref=db.backref('spaceships', lazy=True))

class Captain(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    rank = db.Column(db.String(50))
    homeplanet = db.Column(db.String(50))
