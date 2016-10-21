$(function () {
    $('#btsubmit').click(function () {
        var url = $('input[name="url"]').val();
        $.ajax({
            url: '/feo',
            data: $('form').serialize(),
            type: 'POST',
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
    });
});
function captureReturnKey(e) {
    if (e.keyCode == 13 && e.srcElement.type != 'textarea')
        return false;
}

/**
 * Created by browsable on 2016. 10. 20..
 */
