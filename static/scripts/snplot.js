 var ctx = document.getElementById('plotarea').getContext('2d');
    var chart = new Chart(ctx, {
    type: 'scatter',
    data: {
        datasets: [{
            label: 'Кривая усталости',
            data: [{
                x: 1000,
                y: 200
            }, {
                x: 100000,
                y: 100
            }]
        }]
    },
    options: {
        scales: {
            xAxes: [{
                type: 'logarithmic',
                position: 'bottom'
            }]
        }
    }
});