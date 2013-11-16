$(function(){

	var article = $("#titleArticle");
	var ratingPlacement = $("<div id='titleRating' class='rating-widget-wrap' />").insertAfter(article.find(".title-details-header-cover"));
	var waitingBar = $("<img src='" + siteVars("img") + "ajax-loader-bar.gif' />").hide().appendTo("body");
	article.each(function(){

		var slug = article.data("title-slug");
		$.ajax('/rate/' + slug + '/').success(function(data){
			if (data.widget){
				ratingPlacement.html($(data.widget));
			}
		});
	});

	$("#titleArticle").on("click", ".rate-title", function(ev){
		ev.preventDefault();

		ratingPlacement.height(ratingPlacement.height());
		ratingPlacement.empty();

		waitingBar.show().appendTo(ratingPlacement);
		var lnk = $(this);
		var href = lnk.attr("href");
		$.ajax(
			href,
			{type: "POST"}
		).success(function(data){
			if (data.widget){
				ratingPlacement.height('');
				waitingBar.hide().appendTo("body");
				ratingPlacement.html($(data.widget));
			}

		});
	});



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
	*/

});
