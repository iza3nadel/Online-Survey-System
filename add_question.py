from app import db, app
from app import Question, Answer

with app.app_context():
    # Tworzymy pytanie
    question = Question(text="W jakim jesteś wieku?")
    db.session.add(question)
    db.session.commit()  # Najpierw zapisujemy, by mieć id pytania
    
    # Dodajemy odpowiedzi powiązane z pytaniem
    odp1 = Answer(text="18 – 25 lat", question_id=question.id)
    odp2 = Answer(text="26 – 39 lat", question_id=question.id)
    odp3 = Answer(text="40 – 54 lata", question_id=question.id)
    odp4 = Answer(text="55 – 69 lat", question_id=question.id)
    odp5 = Answer(text="+70 lat", question_id=question.id)
    
    db.session.add_all([odp1, odp2, odp3, odp4, odp5])
    db.session.commit()
    
    print("Pytanie i odpowiedzi dodane do bazy.")
