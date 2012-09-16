$(function(){
	$(".nav-bar .search-keywords").bind("focus", function(ev){
		$(".nav-bar").addClass("nav-bar-searching");
	});
	$(".nav-bar .search-keywords").bind("blur", function(ev){
		$(".nav-bar").removeClass("nav-bar-searching");
	});
	$(".nav-bar .search-submit").click(function(ev){
		if ($(".nav-bar .search-keywords").val() == "" || (!($(".nav-bar").hasClass("nav-bar-searching")) && $(window).width() < 501)){
			ev.preventDefault();
			$(".nav-bar .search-keywords").trigger("focus");
		}
	});
	
	$(".search-additional-fields input").change(function(){
		var form = $(this).parents("form");
		var container = $(this).parents(".search-additional-fields");
		
		form.trigger("submit");
		
		container.addClass("search-additional-fields-thinking")
		
	});
});
