$(document).ready(function(){
    $('#wall-vote').on('click', function(e){
        e.preventDefault();
        $('div.popin').css('display', 'block');
    });

    $('div.options ul li').on('click', function(e){
        e.preventDefault();
        $('div.options ul li figure').removeClass('selected');
        $(this).find('figure').addClass('selected');
    });

    $('#popin-vote').on('click', function(e){
        e.preventDefault();
        $('div.options').hide();
        $('div.popin').addClass('popin-result');
        $('div.results').show();
        //$.ajax({
        //    url: "/cities/" + state,
        //
        //    success: function(data){
        //
        //    },
        //    error: function(data){
        //
        //    }
        //});

        //google.charts.load("current", {packages:["corechart"]});
        //google.charts.setOnLoadCallback(drawChart);
        //function drawChart() {
        //    var data = google.visualization.arrayToDataTable([
        //        ['Task', 'Hours per Day'],
        //        ['Work',     11],
        //        ['Eat',      2],
        //        //['Commute',  2],
        //        //['Watch TV', 2],
        //        //['Sleep',    7]
        //    ]);
        //
        //    var options = {
        //        title: '',
        //        pieHole: 0.4,
        //        legend: {
        //            position:'none',
        //        },
        //        pieSliceText: 'percentage',
        //    };
        //
        //    var chart = new google.visualization.PieChart(document.getElementById('chart_div'));
        //    chart.draw(data, options);
        //}

        var chart = new Chartist.Pie('.ct-chart',
            {
                series: [160, 60 ],
                labels: ['', '']
            }, {
                width: 360,
                height: 260,
                donut: true,
                donutWidth: 30,
                startAngle: 210,
                total: 260,
                showLabel: false,
                plugins: [
                    Chartist.plugins.fillDonut({
                        items: [
                            {
                                content: '',
                                //position: 'center',
                                //offsetY : 0,
                                //offsetX: 0
                            }, {
                                content: '<h3>Faltam 10 dias<span class="small">mph</span></h3>',
                                position: 'center',
                                offsetY : 0,
                                offsetX: 0
                            }
                        ]
                    })
                ],
            });

        chart.on('draw', function(data) {
            if(data.type === 'slice' && data.index == 0) {
                // Get the total path length in order to use for dash array animation
                var pathLength = data.element._node.getTotalLength();

                // Set a dasharray that matches the path length as prerequisite to animate dashoffset
                data.element.attr({
                    'stroke-dasharray': pathLength + 'px ' + pathLength + 'px'
                });

                // Create animation definition while also assigning an ID to the animation for later sync usage
                var animationDefinition = {
                    'stroke-dashoffset': {
                        id: 'anim' + data.index,
                        dur: 1200,
                        from: -pathLength + 'px',
                        to:  '0px',
                        easing: Chartist.Svg.Easing.easeOutQuint,
                        fill: 'freeze'
                    }
                };

                // We need to set an initial value before the animation starts as we are not in guided mode which would do that for us
                data.element.attr({
                    'stroke-dashoffset': -pathLength + 'px'
                });

                // We can't use guided mode as the animations need to rely on setting begin manually
                // See http://gionkunz.github.io/chartist-js/api-documentation.html#chartistsvg-function-animate
                data.element.animate(animationDefinition, true);
            }
        });
    });

    $('.close').on('click', function(e){
        e.preventDefault();
        $('div.options').show();
        $('div.results').hide();
        $('div.popin').removeClass('popin-result');
        $('div.popin').css('display', 'none');
    })
});