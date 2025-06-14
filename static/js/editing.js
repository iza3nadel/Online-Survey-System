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
    isDirty = false;
    form.submit();
}

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.icon[alt="arrow-down"]').forEach(function(btn) {
        btn.addEventListener('click', function() {
            const questionBox = btn.closest('.question-box');
            const nextBox = questionBox.nextElementSibling;
            if (nextBox && nextBox.classList.contains('question-box') && !nextBox.querySelector('#add-question-form')) {
                questionBox.parentNode.insertBefore(nextBox, questionBox);
                updateQuestionNumbers();
            }
        });
    }); // <-- zamknięcie pętli arrow-down

    document.querySelectorAll('.icon[alt="arrow-up"]').forEach(function(btn) {
        btn.addEventListener('click', function() {
            const questionBox = btn.closest('.question-box');
            const prevBox = questionBox.previousElementSibling;
            if (prevBox && prevBox.classList.contains('question-box') && !prevBox.querySelector('#add-question-form')) {
                questionBox.parentNode.insertBefore(questionBox, prevBox);
                updateQuestionNumbers();
            }
        });
    }); // <-- zamknięcie pętli arrow-up

    document.querySelectorAll('.icon[alt="delete"]').forEach(function(btn) {
        btn.addEventListener('click', function() {
            const questionBox = btn.closest('.question-box');
            if (confirm('Czy na pewno chcesz usunąć to pytanie?')) {
                questionBox.remove();
                updateQuestionNumbers();
            }
        });
    }); // <-- zamknięcie pętli delete
});

function updateQuestionNumbers() {
    document.querySelectorAll('.question-box').forEach((box, idx) => {
        const headerSpan = box.querySelector('.question-header span');
        if (headerSpan) {
            headerSpan.textContent = `Pytanie ${idx + 1}`;
        }
    });
}

let isDirty = false;

// Oznacz stronę jako "zmienioną" przy edycji pól
document.addEventListener('input', function(e) {
    if (
        e.target.classList.contains('editable-answer') ||
        e.target.classList.contains('label-input') ||
        e.target.classList.contains('question')
    ) {
        isDirty = true;
    }
});

// Oznacz stronę jako "zmienioną" przy przesuwaniu lub usuwaniu pytań
document.addEventListener('click', function(e) {
    if (
        e.target.classList.contains('icon') &&
        (e.target.alt === 'arrow-up' || e.target.alt === 'arrow-down' || e.target.alt === 'delete')
    ) {
        isDirty = true;
    }
});

// Ostrzeżenie przy próbie wyjścia
window.addEventListener('beforeunload', function(e) {
    if (isDirty) {
        e.preventDefault();
        e.returnValue = '';
    }
});

// Po zapisaniu zmian resetuj flagę
function saveQuestions() {
    const data = collectData();

    fetch('/save_questions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ questions: data })
    }).then(response => {
        if (response.ok) {
            alert("Pytania zapisane!");
            isDirty = false; // <-- reset flagi po zapisie
        } else {
            alert("Błąd zapisu.");
        }
    });
}