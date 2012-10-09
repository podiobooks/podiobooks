$(function(){
	
	var gaqPush = function(shelf, titlesDeep, perSlide){
		
		var shelfPages = shelf.find(".shelf-pages");
		var threshold = parseInt(shelfPages.data("swipe-threshold"));
		
		if(!threshold){
			threshold = perSlide;
			shelfPages.data("swipe-threshold", threshold);
		}
		
		if (titlesDeep > threshold){
			threshold = titlesDeep;
			shelfPages.data("swipe-threshold", threshold);
		}
	};
	
	if ($("body").hasClass("home")){
		
		$("#featured_shelfPageContainer").pbShelf({
			"cookie": "featured_by_category",
			"afterMoveEnd": function(titlesDeep, perSlide){
				gaqPush($("#featured_shelfPageContainer"), titlesDeep, perSlide);
			}
		});
		
		$("#top_titles_shelfPageContainer").pbShelf({
			"cookie": "top_rated_by_author",
			"afterMoveEnd": function(titlesDeep, perSlide){
				gaqPush($("#top_titles_shelfPageContainer"), titlesDeep, perSlide);
			}
		});
		
		$("#recent_titles_shelfPageContainer").pbShelf({
			"cookie": "recent_by_category",
			"afterMoveEnd": function(titlesDeep, perSlide){
				gaqPush($("#recent_titles_shelfPageContainer"), titlesDeep, perSlide);
			}
		});
		
	}
});
