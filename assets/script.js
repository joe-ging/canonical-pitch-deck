Reveal.initialize({
    hash: true,
    center: true,
    transition: 'fade',
    width: 1920,
    height: 1080,
    margin: 0.04,
    controls: true,
    progress: true
});

// Color palette inspired by Canonical Cloud Pricing Report 2022
// Each provider gets a distinct, non-purple color. Canonical stays Aubergine.
const COLORS = {
    canonical: '#772953',  // Canonical Aubergine (purple)
    aws:       '#E95420',  // Ubuntu Orange (warm, stands out)
    azure:     '#0078D4',  // Azure Blue
    gcp:       '#34A853',  // Google Green
};

// --- Cumulative Line Chart (s14_tco_chart.html) ---
let lineChart;
function initLineChart() {
    const canvas = document.getElementById('tcoLine');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (lineChart) lineChart.destroy();

    lineChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Year 0', 'Year 1', 'Year 2', 'Year 3'],
            datasets: [
                {
                    label: 'AWS',
                    data: [0, 13.3, 26.6, 39.8],
                    borderColor: COLORS.aws,
                    backgroundColor: COLORS.aws + '18',
                    borderWidth: 6,
                    pointRadius: 8,
                    pointBackgroundColor: COLORS.aws,
                    fill: false,
                    tension: 0.2
                },
                {
                    label: 'GCP',
                    data: [0, 12.8, 25.6, 38.4],
                    borderColor: COLORS.gcp,
                    backgroundColor: COLORS.gcp + '18',
                    borderWidth: 6,
                    pointRadius: 8,
                    pointBackgroundColor: COLORS.gcp,
                    fill: false,
                    tension: 0.2
                },
                {
                    label: 'Azure',
                    data: [0, 11.9, 23.8, 35.8],
                    borderColor: COLORS.azure,
                    backgroundColor: COLORS.azure + '18',
                    borderWidth: 6,
                    pointRadius: 8,
                    pointBackgroundColor: COLORS.azure,
                    fill: false,
                    tension: 0.2
                },
                {
                    label: 'Canonical',
                    data: [0, 12.0, 15.2, 18.4],
                    borderColor: COLORS.canonical,
                    backgroundColor: COLORS.canonical + '30',
                    borderWidth: 10,
                    pointRadius: 10,
                    pointBackgroundColor: COLORS.canonical,
                    fill: true,
                    tension: 0.2
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: {
                duration: 3000,
                easing: 'easeInOutQuart'
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 45,
                    ticks: {
                        font: { size: 30 },
                        callback: v => '$' + v + 'M'
                    },
                    title: {
                        display: true,
                        text: 'Cumulative Cost ($M)',
                        font: { size: 28, weight: 'bold' }
                    }
                },
                x: {
                    ticks: { font: { size: 34, weight: 'bold' } }
                }
            },
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        font: { size: 28, weight: 'bold' },
                        usePointStyle: true,
                        pointStyle: 'line',
                        padding: 30
                    }
                },
                tooltip: {
                    callbacks: {
                        label: c => c.dataset.label + ': $' + c.raw + 'M'
                    }
                }
            }
        }
    });
}

// --- Bar Chart for s13 TCO table backup (if still used) ---
let barChart;
function initBarChart() {
    const canvas = document.getElementById('tcoBar');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (barChart) barChart.destroy();

    barChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['AWS', 'GCP', 'Azure', 'Canonical'],
            datasets: [{
                label: '3yr TCO ($M)',
                data: [39.8, 38.4, 35.8, 18.4],
                backgroundColor: [COLORS.aws, COLORS.gcp, COLORS.azure, COLORS.canonical],
                borderRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: { duration: 2000, easing: 'easeOutQuart' },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 45,
                    ticks: { font: { size: 32 }, callback: v => '$' + v + 'M' }
                },
                x: {
                    ticks: { font: { size: 40, weight: 'bold' } }
                }
            },
            plugins: {
                legend: { display: false },
                tooltip: { callbacks: { label: c => '$' + c.raw + 'M' } }
            }
        }
    });
}

// Smart init: find whichever chart canvas is on the current slide
function initChartsOnSlide() {
    const currentSlide = Reveal.getCurrentSlide();
    if (!currentSlide) return;
    if (currentSlide.querySelector('#tcoLine')) initLineChart();
    if (currentSlide.querySelector('#tcoBar')) initBarChart();
}

Reveal.on('slidechanged', () => initChartsOnSlide());
Reveal.on('ready', () => initChartsOnSlide());
