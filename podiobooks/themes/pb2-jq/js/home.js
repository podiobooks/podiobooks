$(function(){
	
	if ($("body").hasClass("home")){
		
		$("#featured_shelfPageContainer").pbShelf({
			"cookie": "featured_by_category", 
			"checkCookie": true,
			"clearShelfFirst": false
		});
		
		$("#top_titles_shelfPageContainer").pbShelf({
			"cookie": "top_rated_by_author", 
			"checkCookie": true,
			"clearShelfFirst": false
		});
		
		//$(".half-shelf>.shelf, .quarter-shelf>.shelf").pbShelf();
				
	}
});
