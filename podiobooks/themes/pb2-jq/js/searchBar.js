$(function(){
	
	var navBar = $(".nav-bar");
	var keywords = navBar.find(".search-keywords");
	
	keywords.bind("focus", function(ev){
		navBar.addClass("nav-bar-searching");
	}).bind("blur", function(ev){
		navBar.removeClass("nav-bar-searching");
	});
	
	navBar.find(".search-submit").click(function(ev){
		if (keywords.val() == "" || (!(navBar.hasClass("nav-bar-searching")) && $(window).width() < 501)){
			ev.preventDefault();
			keywords.trigger("focus");
		}
	});
	
	$(".search-additional-fields input").change(function(){
		var form = $(this).parents("form");
		var container = $(this).parents(".search-additional-fields");		
		form.trigger("submit");		
		container.addClass("search-additional-fields-thinking");		
	});
	
});
