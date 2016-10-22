$(function () {
    var submit_form = function () {
        event.preventDefault();
        var url = $('input[name="url"]').val();
        $.ajax({
            url: '/feo',
            data: $('form').serialize(),
            type: 'POST',
            contentType: 'application/x-www-form-urlencoded;charset=UTF-8',
            success: function (response) {
                if(response=='scraping')
                    window.location.href = "/scraping?url="+url
                else
                    document.getElementById("content").innerHTML = response
            },
            error: function (error) {
                console.log(error);
            }

        });
        $('input[name="url"]').focus().select();
    };
    $('#btsubmit').click(submit_form);

    $('input[name="url"]').bind('keydown', function(e) {
        var url = $('input[name="url"]').val();
        if(url!==""){
        if (e.keyCode == 13) {
          var url = $('input[name="url"]').val();
            submit_form()
      }}

    });
});


/**
 * Created by browsable on 2016. 10. 20..
 */
