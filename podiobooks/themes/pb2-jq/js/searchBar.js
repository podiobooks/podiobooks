$(function(){
	var searchTrigger = $("<a class='search-bar-trigger' data-icon='L' href='#'>Search</a>").appendTo(".nav-bar");
	searchTrigger.click(function(ev){
		ev.preventDefault();
		$(".search").show().find('input[type="text"]').focus();
	});	
});
