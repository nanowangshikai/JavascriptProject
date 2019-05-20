from app import db,login
from datetime import datetime
from app import login
from sqlalchemy import ForeignKey, Column, Integer, String
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    admin = db.Column(db.Boolean, default=False, nullable=False)
    preference = db.Column(db.String(320))
    password_hash = db.Column(db.String(128))
    record_id = relationship("Record", backref="user", lazy="dynamic")
    choice_id = relationship("Choice", backref="user", lazy="dynamic")


    def is_admin(self):
        return self.admin

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):

        return '{}'.format(self.username)

class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    carSeries = db.Column(db.String(140), index=True)
    # version = db.Column(db.String(140), index=True, unique = True)
    chooseid = relationship("Choice", backref="brand", lazy='dynamic')
    # record_id = relationship("Record", backref='brand', lazy='dynamic')

    def __repr__(self):
        return "<Brand(carSeries='%s')>" % (self.carSeries)

class Choice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chooseSeries = db.Column(db.String, db.ForeignKey('brand.carSeries'))
    vote = db.Column(db.Integer, default=False, nullable=False)
    UserId = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    def __repre(self):
        return "Choice(carSelected='%s')" % (self.chooseSeries)

class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    UserId = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    # ChoiceId = db.Column(db.Integer, db.ForeignKey('brand.version'))

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
