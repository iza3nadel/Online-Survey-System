from app import db, app

with app.app_context():
    db.create_all()
    print("Baza danych została utworzona!")