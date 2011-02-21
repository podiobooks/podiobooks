$(function(){
	
	$("#featured-shelf").pbShelf({
		"url" : "/lazy/featured/",
		"cookie": "featured_cat", 
		"checkCookie": true
	});
	
	/*
	$(".genre-change select").each(function(){
		var ele = $(this);
		ele.change(function(){
			
			l(ele.val());
			
			var shelf = ele.parents(".shelf");
			var frm = shelf.find("form");
			shelf.pbShelf({
				"url" : frm.attr("action") + ele.val(), 
				"cookie":"featured_cat"
			});
		});
	});
	*/
});
