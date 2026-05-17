Reveal.initialize({
    hash: true,
    center: true,
    transition: 'fade',
    width: 1920,
    height: 1080,
    margin: 0.04,
    controls: true,
    progress: false // We use our own progress bar
});

// ─── Color Palette (Canonical Report 2022) ───
const C = {
    canonical: '#772953',
    aws:       '#E95420',
    azure:     '#0078D4',
    gcp:       '#34A853',
};

// ─── Progress Bar + Slide Counter ───
const progressFill = document.getElementById('progress-fill');
const slideCounter = document.getElementById('slide-counter');

function updateProgress() {
    const total = Reveal.getTotalSlides();
    const current = Reveal.getSlidePastCount() + 1;
    const pct = ((current) / total) * 100;
    progressFill.style.width = pct + '%';
    slideCounter.textContent = current + ' / ' + total;
}

// ─── Cumulative Line Chart (Animated Draw) ───
let lineChart;
function initLineChart() {
    const canvas = document.getElementById('tcoLine');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (lineChart) lineChart.destroy();

    // Start with zeros, then animate to real values
    const realData = {
        aws:       [0, 13.3, 26.6, 39.8],
        gcp:       [0, 12.8, 25.6, 38.4],
        azure:     [0, 11.9, 23.8, 35.8],
        canonical: [0, 12.0, 15.2, 18.4],
    };

    lineChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Year 0', 'Year 1', 'Year 2', 'Year 3'],
            datasets: [
                {
                    label: 'AWS',
                    data: [0, 0, 0, 0],
                    borderColor: C.aws,
                    borderWidth: 5,
                    pointRadius: 7,
                    pointBackgroundColor: C.aws,
                    fill: false,
                    tension: 0.25
                },
                {
                    label: 'GCP',
                    data: [0, 0, 0, 0],
                    borderColor: C.gcp,
                    borderWidth: 5,
                    pointRadius: 7,
                    pointBackgroundColor: C.gcp,
                    fill: false,
                    tension: 0.25
                },
                {
                    label: 'Azure',
                    data: [0, 0, 0, 0],
                    borderColor: C.azure,
                    borderWidth: 5,
                    pointRadius: 7,
                    pointBackgroundColor: C.azure,
                    fill: false,
                    tension: 0.25
                },
                {
                    label: 'Canonical',
                    data: [0, 0, 0, 0],
                    borderColor: C.canonical,
                    backgroundColor: C.canonical + '20',
                    borderWidth: 9,
                    pointRadius: 9,
                    pointBackgroundColor: C.canonical,
                    fill: true,
                    tension: 0.25,
                    borderDash: []
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: { duration: 1200, easing: 'easeOutQuart' },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 45,
                    ticks: {
                        font: { size: 28 },
                        callback: v => '$' + v + 'M'
                    },
                    title: {
                        display: true,
                        text: 'Cumulative Cost ($M)',
                        font: { size: 26, weight: 'bold' }
                    }
                },
                x: { ticks: { font: { size: 32, weight: 'bold' } } }
            },
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        font: { size: 26, weight: 'bold' },
                        usePointStyle: true,
                        pointStyle: 'circle',
                        padding: 30
                    }
                },
                tooltip: {
                    titleFont: { size: 22 },
                    bodyFont: { size: 20 },
                    callbacks: {
                        label: c => c.dataset.label + ': $' + c.raw.toFixed(1) + 'M'
                    }
                }
            }
        }
    });

    // Progressive animation: reveal data point by point
    const steps = [
        { idx: 1, delay: 600 },   // Year 1
        { idx: 2, delay: 1400 },  // Year 2
        { idx: 3, delay: 2200 },  // Year 3
    ];

    steps.forEach(step => {
        setTimeout(() => {
            lineChart.data.datasets[0].data[step.idx] = realData.aws[step.idx];
            lineChart.data.datasets[1].data[step.idx] = realData.gcp[step.idx];
            lineChart.data.datasets[2].data[step.idx] = realData.azure[step.idx];
            lineChart.data.datasets[3].data[step.idx] = realData.canonical[step.idx];
            lineChart.update('active');
        }, step.delay);
    });
}

// ─── Slide-Aware Chart Init ───
function initChartsOnSlide() {
    const slide = Reveal.getCurrentSlide();
    if (!slide) return;
    if (slide.querySelector('#tcoLine')) initLineChart();
}

// ─── Event Listeners ───
Reveal.on('slidechanged', (event) => {
    updateProgress();
    initChartsOnSlide();
    localStorage.setItem('syncSlide', event.indexh);
    syncToCloud(event.indexh);
});
Reveal.on('ready', (event) => {
    updateProgress();
    initChartsOnSlide();
    localStorage.setItem('syncSlide', event.indexh);
    syncToCloud(event.indexh);
});

// ─── Cloud Sync (Multi-device) ───
const urlParams = new URLSearchParams(window.location.search);
const syncKey = urlParams.get('sync');

function syncToCloud(index) {
    if (!syncKey) return;
    fetch(`/api/sync/${syncKey}/${index}`, {
        method: 'POST'
    }).catch(err => console.error('Sync error:', err));
}

window.addEventListener('storage', (e) => {
    if (e.key === 'syncSlide') {
        const slideIndex = parseInt(e.newValue);
        if (!isNaN(slideIndex) && slideIndex !== Reveal.getState().indexh) {
            Reveal.slide(slideIndex);
        }
    }
});
