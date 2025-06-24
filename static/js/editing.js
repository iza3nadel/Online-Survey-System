function collectData() {
    const data = [];

    document.querySelectorAll('.question-box').forEach(box => {
        const questionText = box.querySelector('.question').innerText.trim();

        const label = box.querySelector('.label-input').innerText.trim();

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
    }); 

    document.querySelectorAll('.icon[alt="arrow-up"]').forEach(function(btn) {
        btn.addEventListener('click', function() {
            const questionBox = btn.closest('.question-box');
            const prevBox = questionBox.previousElementSibling;
            if (prevBox && prevBox.classList.contains('question-box') && !prevBox.querySelector('#add-question-form')) {
                questionBox.parentNode.insertBefore(questionBox, prevBox);
                updateQuestionNumbers();
            }
        });
    });

    document.querySelectorAll('.icon[alt="delete"]').forEach(function(btn) {
        btn.addEventListener('click', function() {
            const questionBox = btn.closest('.question-box');
            if (confirm('Czy na pewno chcesz usunąć to pytanie?')) {
                questionBox.remove();
                updateQuestionNumbers();
            }
        });
    }); 


    if (document.getElementById('add-answer-btn')) {
        document.getElementById('add-answer-btn').onclick = function() {
            const container = document.getElementById('answers-list-container');
            const count = container.querySelectorAll('label').length + 1;
            const label = document.createElement('label');
            label.innerHTML = `<input type="radio" name="new_question">
                <span contenteditable="true" class="editable-answer">Odpowiedź ${count}</span>`;
            container.appendChild(label);
            container.appendChild(document.createElement('br'));
        };
    }
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


document.addEventListener('input', function(e) {
    if (
        e.target.classList.contains('editable-answer') ||
        e.target.classList.contains('label-input') ||
        e.target.classList.contains('question')
    ) {
        isDirty = true;
    }
});


document.addEventListener('click', function(e) {
    if (
        e.target.classList.contains('icon') &&
        (e.target.alt === 'arrow-up' || e.target.alt === 'arrow-down' || e.target.alt === 'delete')
    ) {
        isDirty = true;
    }
});


window.addEventListener('beforeunload', function(e) {
    if (isDirty) {
        e.preventDefault();
        e.returnValue = '';
    }
});


function saveQuestions() {
    const data = collectData();

    fetch('/save_questions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ questions: data })
    }).then(response => {
        if (response.ok) {
            alert("Pytania zapisane!");
            isDirty = false; 
        } else {
            alert("Błąd zapisu.");
        }
    });
}