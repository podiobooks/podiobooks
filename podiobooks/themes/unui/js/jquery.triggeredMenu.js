(function( $ ){
	var oneResize = false;
	
	var generallyFine = function(trigger, menu){
		if (!(menu.hasClass("menu-active"))){
			return false;
		}
		return true;
	};
	
	var clickOK = function(ev, trigger, menu){
		
		if (!generallyFine(trigger, menu)){
			return false;
		}
		
		
		return (			
			$(".menu-trigger-active").length > 0) 
			&& ($(ev.target).parents(".triggered-menu").length < 1)
			&& (!($(ev.target).hasClass("triggered-menu"))
			&& (ev.target != trigger.get(0))
			&& ($($(ev.target).parent()).get(0) != trigger.get(0))
		)
	};
	
	var getRealHeight = function(ele){
		
		var tot = parseInt(ele.height());
		
		tot += parseInt(ele.css("padding-top").replace("px", ""));
		tot += parseInt(ele.css("padding-bottom").replace("px", ""));
		
		return tot;
	};
	
	var methods = {
		closeMenu: function(trigger, menu, additionalActiveClass, callback){
			oneResize = false;
			if (!trigger){
				trigger = $(".menu-trigger");
			}
			
			trigger.removeClass("menu-trigger-active");
			menu.removeClass("menu-active").removeClass(additionalActiveClass);
			
			//trigger.focus();
			
			callback(trigger, menu);
		},
		openMenu: function(trigger, menu, additionalActiveClass, callback, fromSide){
			
			trigger.addClass("menu-trigger-active");
			
			var top = parseInt(trigger.offset().top + getRealHeight(trigger))  - 3;
			var left = parseInt(trigger.offset().left) - parseInt(menu.css("borderLeftWidth").replace("px", ""));
			
			if ($(window).width() <= 600){
				left -= 25;
				top += 2;	
			}
			
			if (fromSide == "right"){
				left = 0;
				menu.addClass("right-edge-triggered-menu");
				menu.css({"top": top, "right": left});
			}
			else{
								
				if (left < 0){
					left = 0;
					menu.addClass("left-edge-triggered-menu");
				}
				else{
					menu.removeClass("left-edge-triggered-menu");
				}
				menu.css({"top": top, "left": left});
			}
			
			menu.addClass(additionalActiveClass).addClass("menu-active");
			
			callback(trigger, menu);
						
		}
	};
	
	
	$.fn.triggeredMenu = function( options ) {  
	
		var settings = {
			"target": null,						// ID of target, WITHOUT the pound sign ( '#' )
			"activeMenuClass": "menu-active",	// A CSS class to add to active menus. Active menus will automatically be given a 'menu-active' class
			"activateCallback": function(){},	// callback funciton to execute after the activation of a triggered menu
			"deactivateCallback": function(){},	// callback funciton to execute after the deactivation of a triggered menu
			"fromSide": null
		};
		
		return this.each(function() {        
			// If options exist, lets merge them with our default settings
			if ( options ) { $.extend( settings, options ); }
			
			/*
			 * Get our variables together 
			 */			 			
			var trigger = $(this);
			trigger.addClass("menu-trigger");
			
			var menu;			
			if ( !settings.target ){				
				menu = $("#" + trigger.data("trigger-menu"));
			}
			else{
				menu = $("#" + settings.target);	
			}
			
			
			/*
			 * Bind some global events
			 * 		safeguard against duplication
			 */
			if (!(menu.hasClass("triggered-menu"))){
				
				menu.addClass("triggered-menu")
				
				
				/*
				 * Main open/close event
				 */
				trigger.bind("click", function(event){		
			
					event.preventDefault();				
					
					if (menu.hasClass("menu-active")){
						methods.closeMenu.apply(this, Array(trigger, menu, settings.activeMenuClass, settings.deactivateCallback));
					}
					
					else{
						methods.openMenu.apply(this, Array(trigger, menu, settings.activeMenuClass, settings.activateCallback, settings.fromSide));
					}
				});
				
				
				/*
				 * Additional Close Events
				 */
				$(window).resize(function(){
					if (generallyFine(trigger, menu)){
						if (oneResize){	
							// this fixes what seems to be a bug in iOS where drawing the menu causes a "flash" resize
							// it was closing the menu the first time it was opened
							methods.closeMenu.apply(this, Array(trigger, menu, settings.activeMenuClass, settings.deactivateCallback));
						}
						else{
							oneResize = true;
						}
					}
				});
				
				$(window).keyup(function(event){
					if (event.which == 27 && trigger.hasClass("menu-trigger-active")){
						methods.closeMenu.apply(this, Array(trigger, menu, settings.activeMenuClass, settings.deactivateCallback));
					}
				});
				
				var triggerFocused = false;
				
				trigger.blur(function(){
					triggerFocused = false;
					
				});
				
				trigger.focus(function(){
					triggerFocused = true;
					
				});				
				
				
				$(window).keydown(function(event){					
					if (trigger.hasClass("menu-trigger-active")){
						if (event.which == 9 && triggerFocused){
							if ($(":focus").get(0) == trigger.get(0)){
								menu.find(":first").attr("tabIndex", "0");
								menu.find(":first").focus();
								menu.find(":first").attr("tabIndex", "");
								
							}
						}						
					}
				});
				
				$("body").click(function(ev){
					if (clickOK(ev, trigger, menu)){
						methods.closeMenu.apply(this, Array(trigger, menu, settings.activeMenuClass, settings.deactivateCallback));
					}
				});
			}
		});
	};
})( jQuery );