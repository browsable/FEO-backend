/**
 * Created by browsable on 2016. 10. 22..
 */
var submit = function () {
    event.preventDefault();
    var inputURL = $('input[name="url"]').val();
    var origin = location.href;
    $.getJSON(origin + "feo?url=" + inputURL,
        function (data) {
            console.log('성공 - ', data);
            if (data.responseText == 'scraping')
                window.location.href = "/scraping?url=" + inputURL;
            else
                document.getElementById("content").innerHTML = data.responseText
        });
};

$('#btsubmit').click(submit);

$('input[name="url"]').bind('keydown', function (e) {
    var url = $('input[name="url"]').val();
    if (e.keyCode == 13) {
        if (url !== "") {
            submit()
        } else {
            e.preventDefault()
        }
    }

});