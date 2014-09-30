$(function(){

	var csrfSafeMethod = function(method) {
		// these HTTP methods do not require CSRF protection
		return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	};

	var hasLocalStorage = $("html").hasClass("localstorage");

	var getCurrentStorage = function(slug){

		var currentlyStored = localStorage.getItem(slug);

		// corrects tampering
		if (currentlyStored !== "-1" && currentlyStored !== "1"){
			localStorage.removeItem(slug);
			currentlyStored = localStorage.getItem(slug);
		}

		return currentlyStored;
	};


	if ($("#titleArticle").length > 0 && hasLocalStorage){


		var waitingBar = $("<img id='loaderGif' src='" + siteVars("img") + "ajax-loader-bar.gif' />").hide().appendTo("body");
		var article = $("#titleArticle");
		var slug = article.data("title-slug");
		var placement = article.find(".title-details-rail h1");
		placement.wrap("<div class='title-details-header-cover-wrap clearfix' />");
		var ratingPlacement = $("<div id='titleRating' class='rating-widget-wrap' />").insertAfter(placement);
		$("<p class='rating-instructions'>Rate this Podiobook</p>").insertBefore(ratingPlacement);

		var postData = {};

		var currentStorage = getCurrentStorage(slug);
		if (currentStorage){
			postData = {"in_storage": currentStorage};
		}

		$.ajax('/rate/' + slug + '/', {
			data: postData
		}).success(function(data){
			if (data.widget){
				ratingPlacement.html($(data.widget));
			}
			if (data.titleSlug){
				localStorage.setItem(data.titleSlug, data.userRating);
			}
		});


		$("#titleArticle").on("click", ".rate-title", function(ev){

			ev.preventDefault();


			// CSRF protection
			var csrftoken = $.cookie('csrftoken');
			$.ajaxSetup({
				crossDomain: false, // obviates need for sameOrigin test
				beforeSend: function(xhr, settings) {
					if (!csrfSafeMethod(settings.type)) {
						xhr.setRequestHeader("X-CSRFToken", csrftoken);
					}
				}
			});

			// Correct layout bouncing, show waiting gif
			ratingPlacement.height(ratingPlacement.height());
			ratingPlacement.empty();
			waitingBar.show().appendTo(ratingPlacement);

			var lnk = $(this);
			var href = lnk.attr("href");
			var postData = {};

			var currentStorage = getCurrentStorage(slug);
			if (currentStorage){
				postData = {"in_storage": currentStorage};
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

				if (data.titleSlug){
					localStorage.setItem(data.titleSlug, data.userRating);
				}
			});
		});
	}
});
