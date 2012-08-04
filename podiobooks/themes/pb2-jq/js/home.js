$(function(){
	if ($("body").hasClass("home")){
		
		if ($("body").width() < 501){
			$("#djDebug").remove();
		}
		
		$("#featured-shelf").pbShelf({
			"url" : "/featured/",
			"cookie": "featured_cat", 
			"checkCookie": true
		});
		
		$("#top-rated-shelf").pbShelf({
			"url" : "/top-rated/",
			"cookie": "toprated_cat", 
			"checkCookie": true
		});
		
		$(".half-shelf>.shelf, .quarter-shelf>.shelf").pbShelf();
				
	}
});
