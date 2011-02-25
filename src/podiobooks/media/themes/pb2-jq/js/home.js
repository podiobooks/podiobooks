$(function(){
	if ($("body").hasClass("home")){
		if ($("body").width() < 501){
			$("#djDebug").remove();
		}
		
		
		$("#featured-shelf").pbShelf({
			"url" : "/lazy/featured/",
			"cookie": "featured_cat", 
			"checkCookie": true
		});
		
		$("#top-rated-shelf").pbShelf({
			"url" : "/lazy/top-rated/",
			"cookie": "toprated_cat", 
			"checkCookie": true
		});
			
		
	}
});
