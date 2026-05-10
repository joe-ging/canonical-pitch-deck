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

const bCtx = document.getElementById('tcoBar').getContext('2d');
let bC;

function iB() {
    if (bC) bC.destroy();
    bC = new Chart(bCtx, {
        type: 'bar',
        data: {
            labels: ['AWS', 'GCP', 'Azure', 'Canonical'],
            datasets: [{
                label: '3yr TCO ($M)',
                data: [39.8, 38.4, 35.8, 18.4],
                backgroundColor: ['#2b192e', '#4285f4', '#00a4ef', '#772953'],
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

// Function to check if current slide contains the TCO chart
function checkAndInitChart() {
    const currentSlide = Reveal.getCurrentSlide();
    if (currentSlide && currentSlide.querySelector('#tcoBar')) {
        iB();
    }
}

// Trigger on slide change
Reveal.on('slidechanged', e => {
    checkAndInitChart();
});

// Trigger on initial load
Reveal.on('ready', e => {
    checkAndInitChart();
});
