$(function(){
	var menu = $("<aside class='site-menu' id='site-menu' />").appendTo("body");
	
	$(".nav-bar>ul").each(function(){
		$(this).clone().appendTo(menu);
	});
	$("<ul><li><a href='" + siteVars("home") + "'>Home</a></li></ul>").prependTo(menu);
	var triggers = $("<ul class='menu-triggers' />").prependTo(".nav-bar");
	var menuTrigger = $("<li><a href='#' class='menu-trigger' id='site-menu-trigger'><img src='" + siteVars("img") + "pb-logo-icon.png' /></a></li>").appendTo(triggers);
	
	$("#site-menu-trigger").triggeredMenu({
		target: "site-menu",
		activeMenuClass: "menu-active",
		activateCallback: function(){
			$(".pg").width($(".pg").width());
			$(".pg").css("marginLeft", $(".site-menu").width());
			$("body, html").addClass("site-menu-active");
		},
		deactivateCallback: function(){
			$(".pg").css("width","").css("marginLeft", "");
			$("body, html").removeClass("site-menu-active");
		}
	});
	
});
