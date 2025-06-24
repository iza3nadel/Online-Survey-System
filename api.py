from flask import Blueprint, jsonify, request
from flask_login import login_required
from models import db, Question, Response

api_bp = Blueprint('api', __name__)

@api_bp.route('/api/question-labels')
@login_required
def question_labels():
    labels = [q.label for q in Question.query.order_by(Question.id).all() if q.label]
    return jsonify(labels)

@api_bp.route('/api/question-labels-texts')
@login_required
def question_labels_texts():
    questions = Question.query.order_by(Question.id).all()
    return jsonify({q.label: q.text for q in questions if q.label})

@api_bp.route('/api/chart-data')
@login_required
def chart_data():
    label = request.args.get('label')
    responses = Response.query.all()
    data = {}
    for r in responses:
        if label and r.question_label != label:
            continue
        if r.question_label not in data:
            data[r.question_label] = {}
        if r.answer_text not in data[r.question_label]:
            data[r.question_label][r.answer_text] = 0
        data[r.question_label][r.answer_text] += 1
    chart_data = []
    for label_key, answers in data.items():
        chart_data.append({
            'question_label': label_key,
            'answers': [{'text': k, 'count': v} for k, v in answers.items()]
        })
    return jsonify(chart_data)

@api_bp.route('/api/chart-data-xy')
@login_required
def chart_data_xy():
    x_label = request.args.get('x_label')
    y_label = request.args.get('y_label')
    if not x_label or not y_label or x_label == y_label:
        return jsonify({'labels': [], 'datasets': []})
    responses = Response.query.filter(Response.question_label.in_([x_label, y_label])).all()
    from collections import defaultdict
    survey_map = defaultdict(dict)
    for r in responses:
        survey_map[r.survey_id][r.question_label] = r.answer_text
    x_values = set()
    y_values = set()
    for answers in survey_map.values():
        if x_label in answers and y_label in answers:
            x_values.add(answers[x_label])
            y_values.add(answers[y_label])
    x_values = sorted(x_values)
    y_values = sorted(y_values)
    counts = {y: [0 for _ in x_values] for y in y_values}
    for answers in survey_map.values():
        if x_label in answers and y_label in answers:
            x = answers[x_label]
            y = answers[y_label]
            xi = x_values.index(x)
            counts[y][xi] += 1
    datasets = []
    colors = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe']
    for i, y in enumerate(y_values):
        datasets.append({
            'label': y,
            'data': counts[y],
            'backgroundColor': colors[i % len(colors)]
        })
    return jsonify({'labels': x_values, 'datasets': datasets})
