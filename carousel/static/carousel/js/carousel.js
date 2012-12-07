$(function(){
    // TODO: this should be moved to the project's static files.
    $('.carousel').each(function(){
        $(this).cycle({
            'timeout': 800,
            'pause': 1,
            'speed': 'fast'
        });
    });
});
