/**
 * Created by browsable on 2016. 10. 22..
 */

var xmlHttp;

function createXMLHttpRequest() {
    if(window.ActiveXObject) {
        xmlHttp = new ActiveXObject("Microsoft.XMLHTTP");
    } else if(window.XMLHttpRequest) {
        xmlHttp = new XMLHttpRequest();
    }
}
function reqHTTP(href, method) {
    createXMLHttpRequest();
    var url = location.href;
    url = url.substr(0, url.lastIndexOf('/'));
    url += href;
    var inputURL = $('input[name="url"]').val();
    xmlHttp.onreadystatechange = function() {
        if(xmlHttp.readyState == 4) {
            if(xmlHttp.status == 200) {
                if (xmlHttp.responseText == 'scraping')
                    //window.location.href = "/scraping?url=" + inputURL
                    reqScrapHTTP('/scraping','GET',inputURL);
                else
                    document.getElementById("content").innerHTML = xmlHttp.response
            }
        }
    };
    xmlHttp.open(method, url, true);
    xmlHttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8");
    xmlHttp.setRequestHeader("Cache-Control", "no-cache");
    xmlHttp.setRequestHeader("Pragma", "no-cac  he");
    xmlHttp.send("url="+inputURL);
}

function reqScrapHTTP(href, method, inputURL) {
    createXMLHttpRequest();
    var url = location.href;
    url = url.substr(0, url.lastIndexOf('/'));
    url += href+"?url="+inputURL;
    console.log(url)
    xmlHttp.onreadystatechange = function() {
        if(xmlHttp.readyState == 4) {
            if(xmlHttp.status == 200) {
                var newWindow = window.open("about:blank");
                location.href = url;
                newWindow.innerHTML=xmlHttp.response
            }
        }
    };
    xmlHttp.open(method, url, true);
    xmlHttp.send(null);
}