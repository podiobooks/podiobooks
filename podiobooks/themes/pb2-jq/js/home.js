$(function(){
	
	if ($("body").hasClass("home")){
		
		$("#featured_shelfPageContainer").pbShelf({
			"cookie": "featured_cat", 
			"checkCookie": true,
			"clearShelfFirst": false
		});
		
		$("#top_titles_shelfPageContainer").pbShelf({
			"cookie": "toprated_author", 
			"checkCookie": true,
			"clearShelfFirst": false
		});
		
		$("#recent_titles_shelfPageContainer").pbShelf({
			"cookie": "latest_cat",
			"checkCookie": true,
			"clearShelfFirst": false
		});
		
		//$(".half-shelf>.shelf, .quarter-shelf>.shelf").pbShelf();
				
	}
});
