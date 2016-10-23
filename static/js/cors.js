var submit_form = function () {
    event.preventDefault();
    var inputURL = encodeURIComponent($('input[name="url"]').val());
    var origin = location.href;
    $.ajax({
        url: "https://www.h2perf.com/feo",
        type: "POST",
        data: {'url': inputURL},
        beforeSend: function (xhr) {
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.setRequestHeader('X-PINGOTHER','pingpong');
        },
        crossDomain: true,
        crossOrigin: true,
        success: function (data) {
            console.log(data);
            if (data == 'scraping')
                window.location.href = "/scraping?url=" + inputURL;
            else
                document.getElementById("content").innerHTML = data;
        },
        error: function (data) {
            console.log(data);
        },
    });
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

var makeDELETERequest = function () {
    // Make the DELETE request.
    event.preventDefault();
    var inputURL = encodeURIComponent($('input[name="url"]').val());
    $.ajax({
        url: "https://www.h2perf.com/feo",
        type: "GET",
        data: {'url': inputURL},
        // beforeSend: function (xhr) {
        //     xhr.setRequestHeader('Access-Control-Allow-Origin', '*');
        //     xhr.setRequestHeader('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS');
        //     xhr.setRequestHeader('Access-Control-Max-Age', '3600');
        //     xhr.setRequestHeader('Access-Control-Allow-Headers', 'Origin,Accept,X-Requested-With,Content-Type,Access-Control-Request-Method,Access-Control-Request-Headers,Authorization, DNT,X-Mx-ReqToken,Keep-Alive,User-Agent,If-Modified-Since,Cache-Control,Content-Type');
        //     //xhr.withCredentials = true;
        // },
        contentType: 'application/x-www-form-urlencoded;charset=UTF-8',
        success: function (data) {
            console.log(data);
            if (data == 'scraping')
                window.location.href = "/scraping?url=" + inputURL;
            else
                document.getElementById("content").innerHTML = data;
        }
    });
};