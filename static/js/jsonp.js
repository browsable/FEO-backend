/**
 * Created by browsable on 2016. 10. 22..
 */
var submit = function () {
    event.preventDefault();
    var inputURL = encodeURIComponent($('input[name="url"]').val());
    var origin = location.href;
    $.ajax({
        dataType: "jsonp",
        url: origin+"feo",
        type: "GET",
        data: {'url':inputURL},
        success: function(data){
            console.log("success:"+data);
             if (data.responseText == 'scraping')
                    window.location.href = "/scraping?url=" + inputURL;
                else
                    document.getElementById("content").innerHTML = data.responseText
        }
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