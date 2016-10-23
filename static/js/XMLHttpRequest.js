/**
 * Created by browsable on 2016. 10. 22..
 */

var xmlHttp;

function createXMLHttpRequest() {
    if (window.ActiveXObject) {
        xmlHttp = new ActiveXObject("Microsoft.XMLHTTP");
    } else if (window.XMLHttpRequest) {
        xmlHttp = new XMLHttpRequest();
    }
}
function reqHTTP(href, method) {
    createXMLHttpRequest();
    var inputURL = encodeURIComponent($('input[name="url"]').val());
    var url = "https://www.h2perf.com"+href;
    xmlHttp.onreadystatechange = function () {
        if (xmlHttp.readyState == 4) {
            if (xmlHttp.status == 200) {
                if (xmlHttp.responseText == 'scraping')
                //window.location.href = "/scraping?url=" + inputURL
                    reqScrapHTTP('/scraping', 'GET', inputURL);
                else
                    document.getElementById("content").innerHTML = xmlHttp.response
            }
        }
    };
    // xmlHttp.open(method, url, true);
    // xmlHttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8");
    // xmlHttp.setRequestHeader("Cache-Control", "no-cache");
    // xmlHttp.setRequestHeader("Pragma", "no-cache");
    // xmlHttp.send("url=" + encodeURIComponent(inputURL));
    xmlHttp.open(method, url, true);
    xmlHttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8");
    xmlHttp.setRequestHeader("Access-Control-Allow-Origin", "https://www.");
    xmlHttp.setRequestHeader("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE,OPTIONS");
    xmlHttp.setRequestHeader("Access-Control-Max-Age", "3600");
    xmlHttp.setRequestHeader("Access-Control-Allow-Headers", "Origin,Accept,X-Requested-With,Content-Type,Access-Control-Request-Method,Access-Control-Request-Headers,Authorization");
    xmlHttp.send("url="+inputURL);
}

function reqScrapHTTP(href, method, inputURL) {
    createXMLHttpRequest();
    var url = location.href;
    url = url.substr(0, url.lastIndexOf('/'));
    url += href + "?url=" + inputURL;
    console.log(url)
    xmlHttp.onreadystatechange = function () {
        if (xmlHttp.readyState == 4) {
            if (xmlHttp.status == 200) {
                var newWindow = window.open("about:blank");
                location.href = url;
                newWindow.innerHTML = xmlHttp.response
            }
        }
    };
    xmlHttp.open(method, url, true);
    xmlHttp.setRequestHeader("Access-Control-Allow-Origin", "*");
    xmlHttp.setRequestHeader("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE,OPTIONS");
    xmlHttp.setRequestHeader("Access-Control-Max-Age", "3600");
    xmlHttp.setRequestHeader("Access-Control-Allow-Headers", "Access-Control-Request-Method,Access-Control-Request-Headers,Authorization");
    xmlHttp.send(null);
}
//
// $('input[name="url"]').bind('keydown', function (e) {
//     var url = $('input[name="url"]').val();
//     if (e.keyCode == 13) {
//         if (url !== "") {
//             reqHTTP("/feo","GET")
//         } else {
//             e.preventDefault()
//         }
//     }
//
// });