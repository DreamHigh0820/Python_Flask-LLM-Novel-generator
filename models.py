from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    tier = db.Column(db.String(32),nullable=False,default="None")
    tokens =  db.Column(db.Integer, nullable=True,default=0)
    customer_id = db.Column(db.String(100),nullable=False)
    had_free_trial = db.Column(db.Boolean, default=False, nullable=False)
    end_sub = db.Column(db.DateTime,nullable=True) 
    def add(self):
        db.session.add(self)
        db.session.commit()
    def update(self):
        db.session.commit()
    def check_end_sub(self):
        if not self.end_sub:
          return
        if datetime.now() >= self.end_sub:
          self.tier = "Free"
          self.update()
          
class Fingerprints(db.Model):
    fingerprint = db.Column(db.String(100), unique=True, nullable=False,primary_key=True)
    used_for_free_trial = db.Column(db.Boolean, default=False, nullable=False)
    def add(self):
        db.session.add(self)
        db.session.commit()
    def update(self):
        db.session.commit()