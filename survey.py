from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import db, Question, Answer, Response
import random

survey_bp = Blueprint('survey', __name__)

@survey_bp.route('/')
def index_page():
    return render_template("index.html")

@survey_bp.route('/main')
def main_page():
    return render_template("main.html")

@survey_bp.route('/form')
def form_page1():
    return redirect(url_for('survey.form_dynamic', question_number=0))

@survey_bp.route('/form/<int:question_number>', methods=['GET', 'POST'])
def form_dynamic(question_number):
    questions = Question.query.order_by(Question.id).all()
    if 0 <= question_number < len(questions):
        question = questions[question_number]
        next_number = question_number + 1 if question_number + 1 < len(questions) else None
        prev_number = question_number - 1 if question_number > 0 else None
    else:
        question = None
        next_number = None
        prev_number = None

    if 'survey_id' not in session:
        session['survey_id'] = random.randint(100000, 999999)
    survey_id = session['survey_id']

    if request.method == "POST":
        answer = request.form.get("answer")
        if answer:
            response = Response(
                survey_id=survey_id,
                question_label=question.label,
                answer_text=answer
            )
            db.session.add(response)
            db.session.commit()
        if next_number is not None:
            return redirect(url_for('survey.form_dynamic', question_number=next_number))
        else:
            session.pop('survey_id', None)
            return redirect(url_for('survey.thank_you'))

    return render_template(
        "form2.html",
        question=question,
        question_number=question_number,
        next_number=next_number,
        prev_number=prev_number
    )

@survey_bp.route('/thank_you')
def thank_you():
    return render_template("thankYou.html")
