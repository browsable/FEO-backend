var submit_form = function () {
    event.preventDefault();
    var inputURL = encodeURIComponent($('input[name="url"]').val());
    var origin = location.href;
    $.ajax({
        url: origin + "feo",
        type: "POST",
        data: {'url': inputURL},
        contentType: 'application/x-www-form-urlencoded;charset=UTF-8',
        success: function (response) {
            if (response == 'scraping')
                window.location.href = "/scraping?url=" + inputURL;
            else
                document.getElementById("content").innerHTML = response;
        },
        error: function (error) {
            console.log(error);
        }

    });
    $('input[name="url"]').focus().select();
};

$('#btsubmit').click(submit_form);

$('input[name="url"]').bind('keydown', function (e) {
    var url = $('input[name="url"]').val();
    if (e.keyCode == 13) {
        if (url !== "") {
            submit_form()
        } else {
            e.preventDefault()
        }
    }

});

/**
 * Created by browsable on 2016. 10. 20..
 */
