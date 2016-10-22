$(function() {
    var submit_form = function(e) {
      $.getJSON($SCRIPT_ROOT + '/feo', {
        url: $('input[name="url"]').val()
      }, function(data) {
          console.log(data)
          if(data=='scraping')
                    window.location.href = "/scraping?url="+url
                else
                   document.getElementById("content").innerHTML = response

        $('input[name=url]').focus().select();
      });
      return false;
    };
    $('#btsubmit').bind('click', submit_form);
    $('input[name="url"]').bind('keydown', function(e) {
      if (e.keyCode == 13) {
        submit_form(e);
      }
    });
    $('input[name="url"]').focus();
  });