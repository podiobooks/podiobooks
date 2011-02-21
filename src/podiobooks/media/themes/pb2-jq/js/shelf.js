$(function(){
	
	$("#featured-shelf").pbShelf({"url" : "/lazy/featured/"});
	$("#featured-shelf2").pbShelf({"url" : "/lazy/featured/"});
	
	
	$(".genre-change select").each(function(){
		var ele = $(this);
		ele.change(function(){
			l(ele.val());
			ele.parents(".shelf").pbShelf({"url" : "/lazy/featured/" + ele.val()});
		});
	});
	
});
