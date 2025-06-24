from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import UserMixin

# Tworzymy instancje, które będą inicjalizowane w app.py
# (ale importowane wszędzie tam, gdzie są potrzebne)
db = SQLAlchemy()
bcrypt = Bcrypt()

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    label = db.Column(db.String(100))
    answers = db.relationship('Answer', backref='question', cascade="all, delete", lazy=True)

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)

class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    survey_id = db.Column(db.Integer)
    question_label = db.Column(db.String(100))
    answer_text = db.Column(db.String(200))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True,nullable=False)
    password = db.Column(db.String(150),nullable=False)

class SurveyResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.String(50))
    gender = db.Column(db.String(50))
    education = db.Column(db.String(100))
    residence = db.Column(db.String(100))
    candidate = db.Column(db.String(100))
    party = db.Column(db.String(100))
