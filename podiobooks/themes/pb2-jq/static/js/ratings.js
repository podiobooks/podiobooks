$(function(){

	var hasLocalStorage = $("html").hasClass("localstorage");

	var article = $("#titleArticle");
	var slug = article.data("title-slug");

	var cover = article.find(".title-details-header-cover");

	cover.wrap("<div class='title-details-header-cover-wrap' />");

	var ratingPlacement = $("<div id='titleRating' class='rating-widget-wrap' />").insertAfter(cover);
	$("<p class='rating-instructions'>Rate this Podiobook</p>").insertBefore(ratingPlacement);

	var waitingBar = $("<img src='" + siteVars("img") + "ajax-loader-bar.gif' />").hide().appendTo("body");

	var postData = {};

	if (hasLocalStorage && localStorage.getItem(slug)){
		postData = {"in_storage": localStorage.getItem(slug)};
	}

	$.ajax('/rate/' + slug + '/', {
		data: postData
	}).success(function(data){
		if (data.widget){
			ratingPlacement.html($(data.widget));
		}
	});


	$("#titleArticle").on("click", ".rate-title", function(ev){
		ev.preventDefault();

		ratingPlacement.height(ratingPlacement.height());
		ratingPlacement.empty();

		waitingBar.show().appendTo(ratingPlacement);

		var lnk = $(this);
		var href = lnk.attr("href");
		var postData = {};

		if (hasLocalStorage && localStorage.getItem(slug)){
			postData = {"in_storage": localStorage.getItem(slug)};
		}

		$.ajax(href, {
			type: "POST",
			data: postData
		}).success(function(data){
			if (data.widget){
				ratingPlacement.height('');
				waitingBar.hide().appendTo("body");
				ratingPlacement.html($(data.widget));
			}

			if (data.titleSlug && hasLocalStorage){
				localStorage.setItem(data.titleSlug, data.userRating);
			}

		});
	});
});
