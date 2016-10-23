$(function () {
    var submit_form = function () {
        var inputURL = encodeURIComponent($('input[name="url"]').val());
        var origin = location.href;
        $.getJSON('/', {
            url: inputURL
        }, function (data) {
            if (data.notice != 'scraping') {
                document.getElementById("h3url").innerHTML = data.url + "&nbsp;";
                var h3 = document.createElement("H3");                       // Create a <p> element
                var t = document.createTextNode("is tested");      // Create a text node
                h3.appendChild(t);
                document.getElementById("myflew").appendChild(h3);           // Append <p> to <div> with id="myDIV"
                document.getElementById("h3notice").innerHTML = data.notice;
            } else {
                console.log(origin + 'scraping?url='+data.url);
                window.location.href = origin + 'scraping?url='+data.url;
            }
        });
    };
    $('#btsubmit').bind('click', submit_form);

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
    return false;
});