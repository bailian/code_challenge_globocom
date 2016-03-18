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
    });

    $('.close').on('click', function(e){
        e.preventDefault();
        $('div.popin').css('display', 'none');
    })
});