from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = "tajny klucz" 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    label = db.Column(db.String(100))
    answers = db.relationship('Answer', backref='question', cascade="all, delete", lazy=True)

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True,nullable=False)
    password = db.Column(db.String(150),nullable=False)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def index_page():
    return render_template("index.html")

@app.route("/main")
def main_page():
    return render_template("main.html")

@app.route("/form")
def form_page():
    question = Question.query.first()
    return render_template("form.html", question=question)

@app.route("/form/<int:question_number>")
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
    return render_template("form2.html", question=question, question_number=question_number, next_number=next_number, prev_number=prev_number)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('admin_page'))
        else:
            flash('Błędna nazwa użytkownika lub hasło', 'danger')
    
    return render_template('login.html')

@app.route("/registration", methods=['GET', 'POST'])
def registration_page():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('Użytkownik o tej nazwie lub e-mailu już istnieje!', 'danger')
            return redirect(url_for('registration_page'))
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Konto zostało utworzone! Możesz się teraz zalogować.', 'success')
        return redirect(url_for('login'))

    return render_template("registration.html")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main_page'))

@app.route("/admin")
@login_required
def admin_page():
    return render_template("admin.html", username=current_user.username)

@app.route("/charts")
@login_required
def charts_page():
    return render_template("charts.html")


@app.route("/editing")
@login_required
def editing_page():
    questions = Question.query.all()
    return render_template("editing.html", questions=questions)



@app.route('/save_questions', methods=['POST'])
@login_required
def save_questions():
    data = request.get_json()
    if not data or 'questions' not in data:
        return jsonify({'error': 'Brak danych'}), 400

    # Wyczyść stare pytania i odpowiedzi
    Answer.query.delete()
    Question.query.delete()
    db.session.commit()

    # Dodaj nowe pytania i odpowiedzi
    for q in data['questions']:
        question = Question(text=q['question'], label=q['label'])
        db.session.add(question)
        db.session.flush()  # żeby mieć question.id
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
    db.session.flush()  # Żeby mieć new_q.id

    for a in answers:
        if a.strip():
            db.session.add(Answer(text=a.strip(), question_id=new_q.id))
    db.session.commit()
    flash('Dodano nowe pytanie!', 'success')
    return redirect(url_for('editing_page'))


if __name__ == "__main__":
    app.run(debug=True)
