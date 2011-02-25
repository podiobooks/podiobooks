/*
 * History:
 * 
 * 0.1: Initial plugin creation
 * 0.2: Internalized checking for change form, adding binding for onChange
 * 0.3: Added some more settings for custom classes
 * 0.4: Shelf position indicator
 */
(function( $ ){

	$.fn.pbShelf = function( options ) {
  
		var settings = {
			'url' 			: 		'/',
			"cookie"		: 		null,
			"checkCookie"	: 		false,
			"shelfItem"		: 		".shelf-item",
			"shelfItemCover": 		".shelf-cover"
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
						
			/*
			 * Store the shelf as local variable,
			 * Set shelf height 
			 * 
			 * (otherwise it compresses when elements are removed)
			 */
			var shelf = $(this);
			shelf.height(shelf.height());
			
			
			/*
			 * Remove all content from shelf,
			 * except for the select box
			 * 
			 * This allows the plugin to call itself,
			 * instead of the calling script needing to declare
			 * an on-change event for the select box
			 */
			shelf.children().each(function(){
				if (!($(this).is("form"))){
					$(this).html("");
					$(this).remove();
				}
			});
			
			
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
	
			/*
			 * If we should be checking the cookie,
			 * check it, then set the inital select box value
			 */
			if (settings.checkCookie){
				if($.cookie(settings.cookie)){
					if (shelf.has("form select")){
						shelf.find("form select").val($.cookie(settings.cookie));
						settings.url += $.cookie(settings.cookie);
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
			 * Ajax Progress element image, 
			 * appears in middle of shelf during onchange ajax call
			 * 
			 * Create it, append it to the body for caching, 
			 * move it into the shelf and show
			 */ 
			var progress = $("<p class='shelf-ajax-loader'><img src='" + siteVars("img") + "ajax-loader-bar.gif'/></p>");
			progress.appendTo($("body")).hide();
			progress.appendTo(shelf).show();
			
			
			/*
			 * Right/left shelf arrows
			 * create, added/removed to/from shelf later
			 */
			var leftArrow = $("<a class='shelf-arrow shelf-arrow-left' href='#'></a>");
			var rightArrow = $("<a class='shelf-arrow shelf-arrow-right' href='#'></a>");
						
			/*
			 * Debugging function for logging the current shelf status
			 */
			var status = function(){
				l("cur: " + cur);
				l("where: " + where);
				l("maxWidth: "  + maxWidth);
				l("itemWidth: " + itemWidth);
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
			};
			
			/*
			 * Big beefy ajax workhorse
			 */
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
							img.load(function(){
								loader.remove();
								img.fadeIn();
								
							});
						});
						
						/*
						 * while the covers are loading, hide the progress bar
						 */
						progress.hide();
						
						/*
						 * Find all the shelf items,
						 * add up their total widths
						 */
						var shelfItems = shelf.find(settings.shelfItem);
						var w = 0;
						shelfItems.each(function(){
							itemWidth = parseInt($(this).width()) + parseInt($(this).css("padding-left")) + parseInt($(this).css("padding-right")) + parseInt($(this).css("margin-left")) + parseInt($(this).css("margin-right"));
							w += itemWidth;
						});
						maxWidth = w;
						
						/*
						 * Wrap all the shelf items,
						 * create a "field of vision"
						 */
						shelf.children(settings.shelfItem).wrapAll("<div class='whole-shelf'/>");
						var wholeShelf = shelf.children(".whole-shelf");
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
						progress.hide();
					}
					
					
					/*
					 * Click events for right and left arrows
					 */
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
						status();
					});
					
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
						status();
					});
					
					/*
					 * Use the jquery.touchSwipe plugin
					 * to have swipes trigger click events 
					 * on the arrows
					 */
					wholeShelf.swipe({
						swipeLeft:function(event){
							rightArrow.trigger("click");	
						},
						swipeRight:function(event){
							leftArrow.trigger("click");
						},
						allowPageScroll:"vertical"						
					});					
				}
			});
		});
	};
})( jQuery );