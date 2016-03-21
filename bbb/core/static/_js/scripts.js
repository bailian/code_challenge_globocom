$(document).ready(function(){
    $('#wall-vote').on('click', function(e){
        e.preventDefault();
        $('div.popin').css('display', 'block');
    });

    $('div.options ul li').on('click', function(e){
        e.preventDefault();
        $('div.options ul li figure').removeClass('selected');
        $(this).find('figure').addClass('selected');
        $('#id_vote').val($(this).attr('data-participant'));
    });

    $.buildGraph = function(data_voting){
        var data_series = [];
        for(var i = 0; i < data_voting.result.participants.length; i++){
            data_series.push(data_voting.result.participants[i].votes);
        }
        var chart = new Chartist.Pie('.ct-chart',
            {
                series: data_series,
                labels: ['', '']
            }, {
                width: 360,
                height: 260,
                donut: true,
                donutWidth: 30,
                startAngle: 210,
                total: data_voting.result.total_votes,
                showLabel: false,
                plugins: [
                    Chartist.plugins.fillDonut({
                        items: [
                            {
                                content: '',
                            },
                            {
                                content: data_voting.time_to_finish,
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
    };

    $('#popin-vote').on('click', function(e){
        e.preventDefault();
        if($('#id_vote').val() != ''){
            $('div.options').hide();
            $('div.popin').addClass('popin-result');
            $('div.results').show();
            $.ajax({
                url: "/voting/",
                type: 'post',
                data: $('form[name="voting"]').serialize(),
                success: function(data){
                    if(data.status){
                        $.buildGraph(data);
                        $('div.result p').text("<span>Parabéns!</span> Seu voto para <span>"+ data.participant.name +"</span> foi enviado com sucesso.");
                    }else{
                        $('div.result p').text(data.msg);
                    }
                },
                error: function(data){
                    console.log(data);
                }
            });
        }
    });

    $('.close').on('click', function(e){
        e.preventDefault();
        $('div.options').find('figure').removeClass('selected');
        $('div.options').show();
        $('div.results').hide();
        $('div.popin').removeClass('popin-result');
        $('div.popin').css('display', 'none');
    })
});