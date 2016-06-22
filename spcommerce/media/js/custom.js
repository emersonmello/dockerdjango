$("document").ready(function(){
    $('.add-basket-item').click(function(event) {
        event.preventDefault();
        event.stopImmediatePropagation();
        var url = $(this).attr('href');
        var element = $(this);
        var csrftoken = getCookie('csrftoken');
        $.ajax({
            type: "POST",
            url: url,
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },
            success: function (data) {
                $('a.basket_size').text(data.data)
            },
            error: function (error) {
            }
        });
		return false;
    });
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    };
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
})