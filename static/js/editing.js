function collectData() {
    const data = [];
    // Pobierz wszystkie boxy z pytaniami
    document.querySelectorAll('.question-box').forEach(box => {
        const questionText = box.querySelector('.question').innerText.trim();
        // Pobierz tag (etykietę)
        const label = box.querySelector('.label-input').innerText.trim();
        // Pobierz odpowiedzi
        const answers = Array.from(box.querySelectorAll('.editable-answer'))
            .map(a => a.innerText.trim())
            .filter(a => a.length > 0);

        if (questionText && label && answers.length > 0) {
            data.push({ question: questionText, label: label, answers: answers });
        }
    });
    return data;
}

function saveQuestions() {
    const data = collectData();

    fetch('/save_questions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ questions: data })
    }).then(response => {
        if (response.ok) {
            alert("Pytania zapisane!");
        } else {
            alert("Błąd zapisu.");
        }
    });
}

function submitNewQuestion() {
    const questionText = document.getElementById('new-question-text').innerText.trim();
    const label = document.getElementById('new-question-label').innerText.trim();
    const answers = Array.from(document.querySelectorAll('.answers-list .editable-answer'))
        .map(a => a.innerText.trim())
        .filter(a => a.length > 0);

    if (!questionText || !label || answers.length < 2) {
        alert('Uzupełnij pytanie, etykietę i przynajmniej dwie odpowiedzi!');
        return;
    }

    // Tworzymy ukryty formularz do wysłania danych przez POST
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = '/add_question';

    const qInput = document.createElement('input');
    qInput.type = 'hidden';
    qInput.name = 'question_text';
    qInput.value = questionText;
    form.appendChild(qInput);

    const lInput = document.createElement('input');
    lInput.type = 'hidden';
    lInput.name = 'question_label';
    lInput.value = label;
    form.appendChild(lInput);

    answers.forEach(a => {
        const aInput = document.createElement('input');
        aInput.type = 'hidden';
        aInput.name = 'answers';
        aInput.value = a;
        form.appendChild(aInput);
    });

    document.body.appendChild(form);
    form.submit();
}