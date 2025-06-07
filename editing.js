function collectData() {
    const questions = document.querySelectorAll('.question-box');
    let data = [];

    questions.forEach((box, index) => {
        const questionText = box.querySelector('.question').innerText.trim();
        const label = box.querySelector('.label-input').value.trim();
        const answers = [];

        box.querySelectorAll('form label').forEach(labelEl => {
            const answerText = labelEl.innerText.trim();
            if (answerText) answers.push(answerText);
        });

        data.push({ question: questionText, label: label, answers: answers });
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
