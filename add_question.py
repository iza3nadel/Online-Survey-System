from app import db, app
from app import Question, Answer

with app.app_context():
    # Pytanie 1
    question = Question(text="W jakim jesteś wieku?", label="wiek")
    db.session.add(question)
    db.session.commit() 
    

    odp1 = Answer(text="18 - 25 lat", question_id=question.id)
    odp2 = Answer(text="26 - 39 lat", question_id=question.id)
    odp3 = Answer(text="40 - 54 lata", question_id=question.id)
    odp4 = Answer(text="55 - 69 lat", question_id=question.id)
    odp5 = Answer(text="+70 lat", question_id=question.id)
    
    db.session.add_all([odp1, odp2, odp3, odp4, odp5])
    db.session.commit()
    
    print("Pytanie i odpowiedzi dodane do bazy.")

    # Pytanie 2
    q2 = Question(text="Jaka jest twoja płeć?", label="Płeć")
    db.session.add(q2)
    db.session.commit()
    db.session.add_all([
        Answer(text="Kobieta", question_id=q2.id),
        Answer(text="Mężczyzna", question_id=q2.id),
        Answer(text="Osoba niebinarna", question_id=q2.id),
        Answer(text="Wolę nie podawać", question_id=q2.id)
    ])
    db.session.commit()

    # Pytanie 3
    q3 = Question(text="Jakie masz wykształcenie?", label="Wykształcenie")
    db.session.add(q3)
    db.session.commit()
    db.session.add_all([
        Answer(text="Podstawowe", question_id=q3.id),
        Answer(text="Średnie", question_id=q3.id),
        Answer(text="Zawodowe", question_id=q3.id),
        Answer(text="Wyższe", question_id=q3.id)
    ])
    db.session.commit()

    # Pytanie 4
    q4 = Question(text="Gdzie mieszkasz?", label="Miasto")
    db.session.add(q4)
    db.session.commit()
    db.session.add_all([
        Answer(text="Wieś", question_id=q4.id),
        Answer(text="Miasto do 50 tys. mieszkańców", question_id=q4.id),
        Answer(text="Miasto 50-500 tys. mieszkańców", question_id=q4.id),
        Answer(text="Miasto powyżej 500 tys. mieszkańców", question_id=q4.id)
    ])
    db.session.commit()

    # Pytanie 5
    q5 = Question(text="Czy jesteś osobą wierzącą?", label="Wiara")
    db.session.add(q5)
    db.session.commit()
    db.session.add_all([
        Answer(text="Tak", question_id=q5.id),
        Answer(text="Tak, ale niepraktykującą", question_id=q5.id),
        Answer(text="Nie", question_id=q5.id)
    ])
    db.session.commit()

    # Pytanie 6
    q6 = Question(text="Jaka jest twoja syt. materialna?", label="SytuacjaMaterialna")
    db.session.add(q6)
    db.session.commit()
    db.session.add_all([
        Answer(text="Bardzo dobra", question_id=q6.id),
        Answer(text="Dobra", question_id=q6.id),
        Answer(text="Umiarkowana", question_id=q6.id),
        Answer(text="Zła", question_id=q6.id)
    ])
    db.session.commit()

    # Pytanie 7
    q7 = Question(text="Czy to twój pierwszy udział w wyborach?", label="PierwszyUdział")
    db.session.add(q7)
    db.session.commit()
    db.session.add_all([
        Answer(text="Tak", question_id=q7.id),
        Answer(text="Nie", question_id=q7.id)
    ])
    db.session.commit()

    # Pytanie 8
    q8 = Question(text="Na kogo zagłosowałeś?", label="Kandydat")
    db.session.add(q8)
    db.session.commit()
    db.session.add_all([
        Answer(text="Nawrocki Karol", question_id=q8.id),
        Answer(text="Trzaskowski Rafał", question_id=q8.id)
    ])
    db.session.commit()

    # Pytanie 9
    q9 = Question(text="Co wpłynęło na Twój wybór?", label="Motywacja")
    db.session.add(q9)
    db.session.commit()
    db.session.add_all([
        Answer(text="Program polityczny", question_id=q9.id),
        Answer(text="Wybór tzw. 'mniejszego zła'", question_id=q9.id),
        Answer(text="Emocje", question_id=q9.id),
        Answer(text="Oddałem/am głos nieważny", question_id=q9.id)
    ])
    db.session.commit()
