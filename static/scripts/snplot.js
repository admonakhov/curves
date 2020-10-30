var ctx = document.getElementById('plotarea').getContext('2d');
var colors = ['rgba(237, 0, 79, 1)', 'rgba(178, 0, 237, 1)','rgba(87, 0, 237, 1)','rgba(0, 94, 255, 1)','rgba(0, 255, 251, 1)','rgba(0, 255, 123, 1)']
var options =  {
			responsive: true,
			fill: false,
			scales: {
				xAxes: [{
					display: true,
					type: 'logarithmic'
				}],
				yAxes: [{
					display: true
				}]
			}
		    };

var chart = new Chart(ctx, {
    type: 'line',

    data: {
        datasets: [{
            fill: false,
            data: [],
        }, {
            data: [],
            fill: false,
        }]
            },
    options: options
});

function makedataset(x,y,len)
{

    var data= new Array();
    for(let i =0; i<len; i++)
    {
        data.push( {'x':(x[i]*1), 'y':(y[i]*1)});
    }
    return data;
}


function add(X, Y, len, key='S-N curve ', id=0)
{
    chart.data.datasets[0].backgroundColor = colors[id*1];
    chart.data.datasets[0].data = makedataset(X,Y, len);
    chart.data.datasets[0].showLine = false;
    chart.data.datasets[0].label = key;
    chart.update();
}
function add_regression(X, Y, len, key='S-N curve ', id=0)
{

    chart.data.datasets[1].backgroundColor = colors[id*1];
    chart.data.datasets[1].borderColor = colors[id*1];
    chart.data.datasets[1].borderWidth = 1;
    chart.data.datasets[1].pointStyle = 'line';
    chart.data.datasets[1].data = makedataset(X,Y, len);
    chart.data.datasets[1].label = key + ' regression';
    chart.update();

}
function together(X, Y, len, key='S-N curve ', id=0)
{
    let graph = chart.data.datasets;
    graph.push({

    })
    chart.update();
}
