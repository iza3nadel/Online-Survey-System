from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index_page():
    return render_template("index.html")

@app.route("/main")
def main_page():
    return render_template("main.html")

@app.route("/form")
def form_page():
    return render_template("form.html")

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/registration")
def registration_page():
    return render_template("registration.html")

@app.route("/admin")
def admin_page():
    return render_template("admin.html")

@app.route("/charts")
def charts_page():
    return render_template("charts.html")

@app.route("/editing")
def editing_page():
    return render_template("editing.html")

@app.route("/form2")
def form2_page():
    return render_template("form2.html")
