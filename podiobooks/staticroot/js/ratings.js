$(function(){
	/*
	var csrftoken = $.cookie("csrftoken");
	function csrfSafeMethod(method) {
	    // these HTTP methods do not require CSRF protection
	    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	}
	
	$.ajaxSetup({
	    crossDomain: false, // obviates need for sameOrigin test
	    beforeSend: function(xhr, settings) {
	        if (!csrfSafeMethod(settings.type)) {
	            xhr.setRequestHeader("X-CSRFToken", csrftoken);
	        }
	    }
	});
	
	
	$(".shelf-item-rating").each(function(){
		
		$(this).triggeredMenu({
			target: "promoteTitleMenu"
		});
	});
	
	$(".shelf-item-rating").each(function(){
		var rating = $(this);
		$(this).click(function(){
			
			var url = rating.data("promote");			
			$.ajax({
				url: url,
				success: function(data){
					l(data);
				}, 
				dataType: "json",
				type: 'POST'
			});
			
		});
	});
	*/
	
});