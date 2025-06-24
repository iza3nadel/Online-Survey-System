from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
from flask_bcrypt import Bcrypt
import random
import csv
from io import StringIO
from flask import Response as FlaskResponse
from auth import auth_bp
from admin import admin_bp
from survey import survey_bp
from api import api_bp
from models import db, bcrypt, User, Question, Answer, Response, SurveyResponse

app = Flask(__name__)
app.secret_key = "tajny klucz" 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db.init_app(app)
bcrypt.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(survey_bp)
app.register_blueprint(api_bp)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/save_questions', methods=['POST'])
@login_required
def save_questions():
    data = request.get_json()
    if not data or 'questions' not in data:
        return jsonify({'error': 'Brak danych'}), 400


    Answer.query.delete()
    Question.query.delete()
    db.session.commit()


    for q in data['questions']:
        question = Question(text=q['question'], label=q['label'])
        db.session.add(question)
        db.session.flush()  
        for a in q['answers']:
            db.session.add(Answer(text=a, question_id=question.id))
    db.session.commit()
    return jsonify({'success': True})

@app.route('/add_question', methods=['POST'])
@login_required
def add_question():
    question_text = request.form.get('question_text', '').strip()
    question_label = request.form.get('question_label', '').strip()
    answers = request.form.getlist('answers')

    if not question_text or not question_label or len(answers) < 2:
        flash('Uzupełnij pytanie, etykietę i przynajmniej dwie odpowiedzi!', 'danger')
        return redirect(url_for('editing_page'))

    new_q = Question(text=question_text, label=question_label)
    db.session.add(new_q)
    db.session.flush()  

    for a in answers:
        if a.strip():
            db.session.add(Answer(text=a.strip(), question_id=new_q.id))
    db.session.commit()
    flash('Dodano nowe pytanie!', 'success')
    return redirect(url_for('editing_page'))


if __name__ == "__main__":
    app.run(debug=True)
