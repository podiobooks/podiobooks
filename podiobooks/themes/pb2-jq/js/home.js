$(function(){
	if ($("body").hasClass("home")){
		
		$("#featured_shelfPageContainer").pbShelf({
			"url" : "/featured/",
			"cookie": "featured_cat", 
			"checkCookie": true
		});
		
		$("#top_titles_shelfPageContainer").pbShelf({
			"url" : "/top-rated/",
			"cookie": "toprated_cat", 
			"checkCookie": true
		});
		
		$(".half-shelf>.shelf, .quarter-shelf>.shelf").pbShelf();
				
	}
});
