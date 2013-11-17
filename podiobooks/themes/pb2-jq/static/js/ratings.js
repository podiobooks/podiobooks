$(function(){

	var article = $("#titleArticle");
	var cover = article.find(".title-details-header-cover");

	cover.wrap("<div class='title-details-header-cover-wrap' />");



	var ratingPlacement = $("<div id='titleRating' class='rating-widget-wrap' />").insertAfter(cover);
	$("<p class='rating-instructions'>Rate this Podiobook</p>").insertBefore(ratingPlacement);

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

});
