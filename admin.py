from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, Response as FlaskResponse
from flask_login import login_required, current_user
from models import db, Question, Answer, Response
import csv
from io import StringIO

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
@login_required
def admin_page():
    return render_template("admin.html", username=current_user.username)

@admin_bp.route('/editing')
@login_required
def editing_page():
    questions = Question.query.all()
    return render_template("editing.html", questions=questions)

@admin_bp.route('/charts')
@login_required
def charts_page():
    return render_template("charts.html")

@admin_bp.route('/export-responses')
@login_required
def export_responses():
    survey_ids = [row[0] for row in db.session.query(Response.survey_id).distinct().all()]
    questions = Question.query.order_by(Question.id).all()
    labels = [q.label for q in questions if q.label]
    label_to_text = {q.label: q.text for q in questions if q.label}
    data = {sid: {label: '' for label in labels} for sid in survey_ids}
    for r in Response.query.all():
        if r.survey_id in data and r.question_label in labels:
            data[r.survey_id][r.question_label] = r.answer_text
    si = StringIO()
    si.write('\ufeff')
    header = ['survey_id'] + [label_to_text[l] for l in labels]
    cw = csv.writer(si)
    cw.writerow(header)
    for sid in survey_ids:
        row = [sid] + [data[sid][l] for l in labels]
        cw.writerow(row)
    output = si.getvalue()
    si.close()
    return FlaskResponse(
        output,
        mimetype='text/csv; charset=utf-8',
        headers={"Content-Disposition": "attachment;filename=odpowiedzi.csv"}
    )
