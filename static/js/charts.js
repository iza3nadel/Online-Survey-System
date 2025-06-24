let myChart = null;
let labelToText = {};


async function loadQuestionLabels() {
    const res = await fetch('/api/question-labels');
    const labels = await res.json();
    const select = document.getElementById('question-label-select');
    select.innerHTML = '<option value="">-- Wybierz pytanie --</option>';
    labels.forEach(label => {
    const opt = document.createElement('option');
    opt.value = label;
    opt.textContent = label;
    select.appendChild(opt);
    });
}
loadQuestionLabels();


async function loadQuestionLabelsXY() {
    const res = await fetch('/api/question-labels');
    const labels = await res.json();
    const res2 = await fetch('/api/question-labels-texts');
    labelToText = await res2.json();
    const xSelect = document.getElementById('x-label-select');
    const ySelect = document.getElementById('y-label-select');
    xSelect.innerHTML = '<option value="">-- Wybierz --</option>';
    ySelect.innerHTML = '<option value="">-- Wybierz --</option>';
    labels.forEach(label => {
    const optX = document.createElement('option');
    optX.value = label;
    optX.textContent = label;
    xSelect.appendChild(optX);
    const optY = document.createElement('option');
    optY.value = label;
    optY.textContent = label;
    ySelect.appendChild(optY);
    });
}
loadQuestionLabelsXY();

document.getElementById('generate-btn').onclick = async function() {
    const chartType = document.getElementById('chart-type-select').value;
    let xLabel = document.getElementById('x-label-select').value;
    let yLabel = document.getElementById('y-label-select').value;
    if (chartType === 'pie') {
    if (!xLabel) {
        alert('Wybierz etykietę X!');
        return;
    }
    yLabel = null;
    } else {
    if (!xLabel || !yLabel || xLabel === yLabel) {
        alert('Wybierz dwie różne etykiety!');
        return;
    }
    }
    let url;
    if (chartType === 'pie') {
    url = `/api/chart-data?label=${encodeURIComponent(xLabel)}`;
    } else {
    url = `/api/chart-data-xy?x_label=${encodeURIComponent(xLabel)}&y_label=${encodeURIComponent(yLabel)}`;
    }
    const res = await fetch(url);
    const data = await res.json();
    if (chartType === 'pie') {
    if (!data.length || !data[0].answers.length) {
        alert('Brak danych do wyświetlenia wykresu dla wybranej etykiety.');
        return;
    }
    const pieLabels = data[0].answers.map(a => a.text);
    const pieData = data[0].answers.map(a => a.count);
    if (myChart) myChart.destroy();
    const ctx = document.getElementById('myChart').getContext('2d');
    myChart = new Chart(ctx, {
        type: 'pie',
        data: {
        labels: pieLabels,
        datasets: [{
            data: pieData,
            backgroundColor: pieLabels.map(() => '#' + Math.floor(Math.random()*16777215).toString(16))
        }]
        },
        options: {
        responsive: true,
        plugins: { legend: { display: true } }
        }
    });
    return;
    }

    if (!data.labels.length || !data.datasets.length) {
    alert('Brak danych do wyświetlenia wykresu dla wybranych etykiet.');
    return;
    }
    if (myChart) myChart.destroy();
    const ctx = document.getElementById('myChart').getContext('2d');
    if (chartType === 'pie') {
 
    const pieLabels = data.datasets.map(ds => ds.label);
    const pieData = data.datasets.map(ds => ds.data.reduce((a, b) => a + b, 0));
    myChart = new Chart(ctx, {
        type: 'pie',
        data: {
        labels: pieLabels,
        datasets: [{
            data: pieData,
            backgroundColor: data.datasets.map(ds => ds.backgroundColor)
        }]
        },
        options: {
        responsive: true,
        plugins: { legend: { display: true } }
        }
    });
    } else {
    myChart = new Chart(ctx, {
        type: chartType,
        data: {
        labels: data.labels,
        datasets: data.datasets
        },
        options: {
        responsive: true,
        plugins: { legend: { display: true } },
        scales: {
            x: {
            title: {
                display: true,
                text: labelToText[xLabel] || xLabel
            }
            },
            y: {
            title: {
                display: true,
                text: labelToText[yLabel] || yLabel
            }
            }
        }
        }
    });
    }
};


document.getElementById('chart-type-select').addEventListener('change', function() {
    const ySelect = document.getElementById('y-label-select');
    if (this.value === 'pie') {
    ySelect.disabled = true;
    ySelect.value = '';
    } else {
    ySelect.disabled = false;
    }
});

document.getElementById('download-btn').onclick = function() {
    const canvas = document.getElementById('myChart');
    const link = document.createElement('a');
    link.href = canvas.toDataURL('image/png');
    link.download = 'wykres.png';
    link.click();
};
