/*
 * History:
 * 
 * 0.1: Initial plugin creation
 * 0.2: Internalized checking for change form, adding binding for onChange
 * 0.3: Added some more settings for custom classes
 * 0.4: Shelf position indicator
 * 0.5: Support for shelves that don't need ajax calls
 * 0.6: Uses 'find' instead of 'children' for digging up relevant shelf peices
 * 0.7: Allows for shelf creation based on static content (i.e. no need to ajax on first load)
 */
(function( $ ){

	$.fn.pbShelf = function( options ) {
  
		var settings = {
			"cookie"		 : 		null,
			"checkCookie"	 : 		false,
			"shelfItem"		 : 		".shelf-item",
			"shelfItemCover" : 		".shelf-cover",
			"clearShelfFirst":		true
		};
		
		/*
		 * Debugging function for logging the current shelf status
		 */
		var status = function(){
			l("cur: " + cur);
			l("where: " + where);
			l("maxWidth: "  + maxWidth);
			l("itemWidth: " + itemWidth);
			l("numItems: " + numItems);
			l("numSteps : " + numSteps);
			l("curStep : " + curStep);
		};
		
		return this.each(function(){
			
			if (options){
				$.extend(settings,options);
			}
			
			
			/*
			 * Shelf status variables
			 */
			var where = 0;			// How many "titles in" the user is (integer, 0-# of books)
			var cur = 0;			// current number of pixles have been shoved left
			var maxWidth = 0;		// maximum number of pixels the shelf can move to the left
			var itemWidth = 0;		// how wide each .shelf-item is
			var numItems = 0;
			var numSteps = 0;
			var curStep = 0;
			
			/*
			 * Some shelf element localization
			 */
			var wholeShelf;
			
			var shelf = $(this);
			shelf.height(shelf.height());
			
			var shelfSteps;
			var leftArrow;
			var rightArrow;
						
			/*
			 * Store the shelf as local variable,
			 * Set shelf height 
			 * 
			 * (otherwise it compresses when elements are removed)
			 */
			
			
			/*
			 * If the shelf has a select box,
			 * bind the on-change event to reset the plugin
			 */
			if (shelf.has("form select")){
				var sel = shelf.find("form select");
				
				sel.unbind("change");
				
				sel.change(function(){
					if (settings.cookie){
						shelf.pbShelf({
							"url" : sel.parents("form").attr("action") + sel.val(), 
							"cookie":settings.cookie							
						});
					}
					else{
						shelf.pbShelf({"url" : sel.parents("form").attr("action") + sel.val()});
					}
				});				
			}
			
			
	
			var makeShelf = function(){
				
				shelfSteps = $("<ul class='shelf-step'/>").prependTo(shelf);
				
				/*
				 * If the appended data has shelf items,
				 * proceed with building shelf functionality
				 */
				if(shelf.find(settings.shelfItem).length){
					
					
					/*
					 * Find all shelf items that arent marked as covers being loaded
					 */
					$(shelf).find(settings.shelfItemCover).find("img:not(.shelf-cover-loading)").each(function(){
						
						
						var img = $(this);
						
						/*
						 * Hide the image, replace it with a progress loader graphic
						 */
						img.hide();
						var loader = $("<img class='shelf-cover-loading' src='" + siteVars("img") + "loading.gif' />").appendTo(img.parents(".shelf-cover"));
						
						/*
						 * Once the real cover has loaded,
						 * remove the loader graphic, fade in the cover
						 */
						img.imagesLoaded(function(){
							img.unbind("load");
							loader.remove();
							img.fadeIn();
							
						});
					});
					
					
					/*
					 * while the covers are loading, hide the progress bar
					 */
					if (progress){
						progress.hide();
					}
					
					
					/*
					 * Find all the shelf items,
					 * add up their total widths
					 */
					var shelfItems = shelf.find(settings.shelfItem);
					var w = 0;
					shelfItems.each(function(){
						var item = $(this);
						numItems++;						
						itemWidth = parseInt(item.width()) + parseInt(item.css("padding-left")) + parseInt(item.css("padding-right")) + parseInt(item.css("margin-left")) + parseInt(item.css("margin-right"));
						w += itemWidth;
					});
					maxWidth = w;
					
					/*
					 * Wrap all the shelf items,
					 * create a "field of vision"
					 */
					shelf.find(settings.shelfItem).wrapAll("<div class='whole-shelf'/>");
					wholeShelf = shelf.find(".whole-shelf");
					wholeShelf.wrap("<div class='shelf-view'/>");
					
					
					/*
					 * Append the right/left arrows,
					 * let the arrow handler figure out
					 * if they should be shown or hidden
					 */
					leftArrow.appendTo(shelf);
					rightArrow.appendTo(shelf);
					handleArrows();
				}
				else{
					/*
					 * If there were no returned shelf items,
					 * Just hide the progress bar
					 */
					handleArrows();
					progress.hide();
				}
				
				
				/*
				 * Click events for right and left arrows
				 */
				if (rightArrow){
					rightArrow.click(function(e){
						e.preventDefault();
						if (cur < maxWidth - shelf.width()){
							where += shelf.width() / itemWidth;
							if (where * itemWidth > maxWidth - shelf.width()){
								where = (maxWidth - shelf.width()) / itemWidth;
							}
							var targ = "-" + (where * itemWidth) + "px";
							
							
							cur = where * itemWidth;
							
							wholeShelf.animate({
								left:targ
							},600,"easeOutCirc");
						}
						handleArrows();
					});
				}
				
				if (leftArrow){
					leftArrow.click(function(e){
						e.preventDefault();
						
						if (cur > 0){							
							where -= shelf.width() / itemWidth;
							if (where < 0){
								where = 0;
							}
							var targ = "-" + (where * itemWidth) + "px";
							cur = where * itemWidth;							
							wholeShelf.animate({
								left:targ
							},600,"easeOutCirc");
						}
						handleArrows();
					});
				}
				/*
				 * Add arrow/positioner to window resize
				 * 
				 * I don't know if there are serious 
				 * performance implications here...
				 * 
				 */
				$(window).unbind("resize",handleArrows);
				$(window).bind("resize",handleArrows);
				
				
				/*
				 * Use the jquery.touchSwipe plugin
				 * to have swipes trigger click events 
				 * on the arrows
				 */
				if (wholeShelf){
					wholeShelf.swipe({
						swipeLeft:function(event){
							rightArrow.trigger("click");	
						},
						swipeRight:function(event){
							leftArrow.trigger("click");
						},
						allowPageScroll:"vertical",
						fallbackToMouseEvents: false					
					});
				}
			};
			
			
			/*
			 * If we should be checking the cookie,
			 * check it, then set the inital select box value
			 */
			var select = shelf.find("form select");
			
			if (settings.checkCookie){
				if (select.length > 0){
					if($.cookie(settings.cookie)){
						select.val($.cookie(settings.cookie));
						settings.url += $.cookie(settings.cookie);
					}
					else{
						settings.url += select.val();
					}					
				}
			}
			
			
			/*
			 * If we have a cookie name to set, set it 
			 * based on the currently selected form>select
			 */
			if(settings.cookie){
				$.cookie(settings.cookie,shelf.find("form select").val(),{expires:7});
			}		
			
			
			
			/*
			 * Right/left shelf arrows
			 * create, added/removed to/from shelf later
			 */			
			leftArrow = $("<a class='shelf-arrow shelf-arrow-left' href='#'></a>");
			rightArrow = $("<a class='shelf-arrow shelf-arrow-right' href='#'></a>");
			
			
			
			/*
			 * Swift step: 
			 * Moving via position dots
			 */
			var bindSwiftStep = function(a,i,per){
				a.unbind("click");
				a.click(function(e){
					e.preventDefault();
										
					var px = i * per * itemWidth;
					if (px > maxWidth - shelf.width()){
						px = maxWidth - shelf.width();
					}
					
					var targ = "-" + (px) + "px";
					where = px / itemWidth;
					cur = px;
					
					wholeShelf.animate({
						left:targ
					},600,"easeOutCirc");
					
					handleArrows();
				});
			};
				
			/*
			 * Current shelf position
			 */
			 var handleShelfPosition = function(){
			 	shelfSteps.children().remove();
			 	
			 	if (shelf.find(settings.shelfItem).length){
			 		
				 	// make sure we always round up
				 	numSteps = Math.ceil(maxWidth / shelf.width());	
				 	var perSlide = Math.floor(shelf.width() / itemWidth);
				 	
				 	curStep = Math.ceil((cur / itemWidth) / perSlide);
				 	
				 	for (var i = 0; i < numSteps; i++){
				 		var li;
				 		if (i == curStep){
				 			li = $("<li><a class='shelf-step-cur' href='#'></a></li>").appendTo(shelfSteps);
				 		}
				 		else{
				 			li = $("<li><a href='#'></a></li>").appendTo(shelfSteps);
				 		}
				 		
				 		circ = li.find("a");
				 		
				 		bindSwiftStep(circ,i,perSlide);
				 	}
				 	
				 	
				 	/*
				 	 * Center the step indicator based on percentage
				 	 */
				 	shelfSteps.css({'left':(shelf.width() / 2 - shelfSteps.width() / 2) / shelf.width() * 100 + "%"});
				 	
				 	
				 	/*
				 	 * If there is only 1 step and there 
				 	 * are less shelf items than shelf spaces,
				 	 * hide the shelf progress indicator
				 	 */
				 	if (numSteps < 2 && shelf.find(settings.shelfItem).length < perSlide){
				 		shelfSteps.children().remove();
				 		
				 	}
			 	}
			 };
			 
			 
			/*
			 * Hiding/showing arrows 
			 * based on shelf position
			 */
			var handleArrows = function(){
				
				if (cur == 0){
					leftArrow.hide();
				}
				else{
					leftArrow.show();
				}
				if (cur < maxWidth - shelf.width()){
					rightArrow.show();
				}
				else{
					rightArrow.hide();
				}
				//status();
				handleShelfPosition();
								
			};
			
			var progress = $("<p class='shelf-ajax-loader'><img src='" + siteVars("img") + "ajax-loader-bar.gif'/></p>");
			progress.appendTo($("body"));
			
			/*
			 * Ajax workhorse
			 */
			if (settings.url && settings.clearShelfFirst){
				
				/*
				 * Remove all content from shelf,
				 * except for the select box
				 * 
				 * This allows the plugin to call itself,
				 * instead of the calling script needing to declare
				 * an on-change event for the select box
				 */
				shelf.children().each(function(){
					var item = $(this);
					if (!(item.is("form"))){
						item.html("");
						item.remove();
					}
				});
				
				/*
				 * Ajax Progress element image, 
				 * appears in middle of shelf during onchange ajax call
				 * 
				 * Create it, append it to the body for caching, 
				 * move it into the shelf and show
				 */ 
				
				progress.appendTo(shelf).show();
			
				
				$.ajax({
					method:"get",
					url:settings.url,
					success:function(data){
						
						/*
						 * Ajax request should return HTML
						 * 
						 * Append all data to the shelf
						 */
						$(data).appendTo(shelf);
						makeShelf();			
					}
				});
			}
			else{				
				makeShelf();
			}
			shelf.addClass("pbShelf");
		});
	};
})( jQuery );


						