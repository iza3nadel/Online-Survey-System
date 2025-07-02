# System Ankietyzacji Wyborczej – Dokumentacja

## Spis treści
1. Opis projektu
2. Struktura katalogów
3. Instalacja i uruchomienie
4. Opis głównych plików i modułów
5. Modele bazy danych
6. Blueprinty i routing
7. Szablony i statyczne zasoby
8. Eksport danych
9. Dodawanie pytań do bazy
10. Bezpieczeństwo i uwierzytelnianie

---

## 1. Opis projektu
System Ankietyzacji Wyborczej to aplikacja webowa napisana w Pythonie (Flask), służąca do przeprowadzania anonimowych ankiet wyborczych, zarządzania pytaniami, analizowania wyników i eksportu danych. Projekt jest podzielony na logiczne moduły (blueprinty), co ułatwia rozwój i utrzymanie.

## 2. Struktura katalogów
```
System-Ankietyzacji-Wyborczej/
├── app.py                # Główny plik uruchomieniowy, rejestracja blueprintów
├── models.py             # Modele bazy danych, inicjalizacja db i bcrypt
├── auth.py               # Blueprint logowania, rejestracji, wylogowania
├── admin.py              # Blueprint panelu admina, edycji pytań, eksportu, wykresów
├── survey.py             # Blueprint ankiety, pytań, podziękowania
├── api.py                # Blueprint endpointów AJAX/JSON
├── add_question.py       # Skrypt do inicjalnego ładowania pytań do bazy
├── requirements.txt      # Lista zależności Pythona
├── instance/
│   └── users.db          # Plik bazy danych SQLite
├── static/
│   ├── css/              # Pliki stylów CSS
│   ├── js/               # Pliki JavaScript
│   └── pictures/         # Obrazy
└── templates/            # Szablony HTML (Jinja2)
```

## 3. Instalacja i uruchomienie
1. **Klonowanie repozytorium:**
   ```bash
   git clone <adres_repozytorium>
   cd System-Ankietyzacji-Wyborczej
   ```
2. **Utworzenie i aktywacja środowiska wirtualnego:**
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # Windows
   # lub
   source venv/bin/activate      # Linux/Mac
   ```
3. **Instalacja zależności:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Uruchomienie aplikacji:**
   ```bash
   flask run
   # lub
   python app.py
   ```
5. **Dostęp:**
   Przeglądarka: http://127.0.0.1:5000/

## 4. Opis głównych plików i modułów
- **app.py** – Inicjalizuje aplikację, rejestruje blueprinty, ustawia bazę i logowanie.
- **models.py** – Definiuje modele SQLAlchemy: User, Question, Answer, Response, SurveyResponse. Inicjalizuje db i bcrypt.
- **auth.py** – Obsługuje logowanie, rejestrację, wylogowanie (blueprint `auth`).
- **admin.py** – Panel admina, edycja pytań, eksport, wykresy (blueprint `admin`).
- **survey.py** – Obsługa ankiety, pytań, podziękowania (blueprint `survey`).
- **api.py** – Endpointy AJAX/JSON do wykresów i etykiet (blueprint `api`).
- **add_question.py** – Skrypt do inicjalnego ładowania pytań i odpowiedzi do bazy.

## 5. Modele bazy danych (`models.py`)
- **User** – użytkownicy (id, username, email, password)
- **Question** – pytania ankietowe (id, text, label)
- **Answer** – możliwe odpowiedzi (id, text, question_id)
- **Response** – odpowiedzi użytkowników (id, survey_id, question_label, answer_text)

## 6. Blueprinty i routing
- **auth** – `/login`, `/registration`, `/logout`
- **admin** – `/admin`, `/editing`, `/charts`, `/export-responses`
- **survey** – `/`, `/main`, `/form`, `/form/<int:question_number>`, `/thank_you`
- **api** – `/api/question-labels`, `/api/question-labels-texts`, `/api/chart-data`, `/api/chart-data-xy`

## 7. Szablony i statyczne zasoby
- **templates/** – szablony HTML z dziedziczeniem (base.html, base_auth.html, index.html, main.html, login.html, registration.html, admin.html, editing.html, charts.html, form2.html, thankYou.html)
- **static/css/** – style CSS dla poszczególnych widoków
- **static/js/** – JavaScript (np. obsługa wykresów, edycji pytań)
- **static/pictures/** – obrazy używane w aplikacji

## 8. Eksport danych
- Eksport odpowiedzi do pliku CSV (Excel-friendly, UTF-8 BOM) dostępny z panelu admina.
- Każda odpowiedź w osobnej kolumnie, nagłówki zgodne z pytaniami.

## 9. Dodawanie pytań do bazy
- Skrypt `add_question.py` pozwala na szybkie załadowanie przykładowych pytań i odpowiedzi do bazy.
- Po uruchomieniu skryptu pytania i odpowiedzi są widoczne w aplikacji.

## 10. Bezpieczeństwo i uwierzytelnianie
- Hasła użytkowników są hashowane (bcrypt).
- Dostęp do panelu admina, edycji pytań, eksportu i wykresów wymaga logowania.
- Flask-Login zarządza sesją użytkownika.
