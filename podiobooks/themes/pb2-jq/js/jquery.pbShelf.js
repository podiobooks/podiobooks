
/*
 * Podiobooks Shelf plugin
 * Custom carousel bookshelves for Podiobooks
 * 
 * 
 * Version: 0.9
 * 
 * 
 * History:
 * 
 * 0.1: Initial plugin creation
 * 0.2: Internalized checking for change form, adding binding for onChange
 * 0.3: Added some more settings for custom classes
 * 0.4: Shelf position indicator
 * 0.5: Support for shelves that don't need ajax calls
 * 0.6: Uses 'find' instead of 'children' for digging up relevant shelf peices
 * 0.7: Allows for shelf creation based on static content (i.e. no need to ajax on first load)
 * 0.8: Allows blank incoming cookies to delete the existing cookie
 * 0.9 Dynamic touch-sliding for adjustable-width shelves; Shelf width no longer needs to be a full item width; Callback hooks for "after movement" of shelves
 * 
 */

(function( $ ){

	$.fn.pbShelf = function( options ) {
  
		var settings = {
			"cookie"		 : 		null,
			"shelfItem"		 : 		".shelf-item",
			"shelfItemCover" : 		".shelf-cover",
			"clearShelfFirst":		false,
			"afterMoveEnd"	 : 		function(titlesDeep, perSlide){},
			"url"			 : 		null
		};
		
		/*
		 * Debugging function for logging the current shelf status
		 */
		
		
		return this.each(function(){
			
			if (options){
				$.extend(settings, options);
			}
			
			var status = function(){
				l("cur: " + cur);
				l("where: " + where);
				l("maxWidth: "  + maxWidth);
				l("itemWidth: " + itemWidth);
				l("numItems: " + numItems);
				l("numSteps : " + numSteps);
				l("curStep : " + curStep);
				l("maxLeft : " + maxLeft);
				l("==================");
			};
			
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
			var maxLeft = 0;
			var shelfViewBoundaries = [];
			
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
					var modSettings = settings;					
					modSettings.url = sel.parents("form").attr("action") + sel.val() + '/';
					modSettings.clearShelfFirst = true;
					shelf.pbShelf(modSettings);
				});				
			}
			
			var loadImages = function(){
				
				// How many images in-advance we want to load (it'll actually be this number, minus 1')
				var perLoad = 5;
				
				// calculate how many items per shelf we have
				var perSlide = Math.floor(shelf.width() / itemWidth);
				
				var items = shelf.find(".shelf-item");				
				
				// calculate a 'start' and 'end' range for how many shelf items to check
				// we are going to check whether or not there are enough images pre-loaded
				// for the next set of shelf items to display on-slide
				var start = where;				
				var end = start + (perSlide * perLoad);				
				if (end > items.length){
					end = items.length;
				}
				
				// Build a 'set' of unloaded images
				var loadMore = true;
				var set = [];
				for (var i = start-1; i < end; i++){
					if (set.length < 1){
						set = $(items[i]).find('[data-image-src]');						
					}
					else{						
						set = set.add($(items[i]).find('[data-image-src]'));
					}
				}
				
				// If we aren' running into an issue, don't load any more images yet
				if (set.length + 1 < perSlide * perLoad){
					loadMore = false;
				}
				
				// If we are running up against the end of the shelf, finish out the image loads
				if (end === items.length){
					loadMore = true;
				}				
				
				// If we have decided to load a set images
				// Load them now				
				if (loadMore){
					for (var i = start-1; i < end; i++){					
						$(items[i]).find('[data-image-src]').each(function(){							
							var a = $(this);
							var src = a.data("image-src");							
							var img = $("<img data-title-slug='" + a.data("title-slug") + "' class='shelf-cover' alt='Cover for " + a.data("title-name") + "' src='" + src + "' />");							
							a.html(img);
							a.removeAttr("data-image-src");
						});					
					}		
				}						
			};
	
			var makeShelf = function(){
				
				shelfSteps = $("<ul class='shelf-step'/>").prependTo(shelf);
				
				/*
				 * If the appended data has shelf items,
				 * proceed with building shelf functionality
				 */
				if(shelf.find(settings.shelfItem).length){
					
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
					wholeShelf.width(maxWidth + 100);
					
					
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
							
							var shelfWidth = shelf.width();
							var targ = cur + parseInt(shelfWidth / itemWidth) * itemWidth;
														
							if (targ < maxLeft){
								cur = targ;
							}
							else{
								cur = maxLeft;
								targ = maxLeft;
							}
							
							where = cur / itemWidth;
							
							wholeShelf.animate({
								left: -targ
							},600,"easeOutCirc");
						}						
						handleArrows();						
					});
				}
				
				if (leftArrow){
					leftArrow.click(function(e){
						
						e.preventDefault();
						
						if (cur > 0){
							
							var shelfWidth = shelf.width();
							
							// accomidates for the far-right being offset at the left of the shelf
							var targ = parseInt(cur / itemWidth) * itemWidth - parseInt(shelfWidth / itemWidth) * itemWidth;
							
							if (cur % itemWidth != 0){
								targ += itemWidth;
							}
							
							
							if (targ <= 0){
								cur = 0;
								targ = 0;
							}
							else{
								cur = targ
							}
							
							where = cur / itemWidth;
							if (where < 0){
								where = 0;
							}
							
														
							wholeShelf.animate({
								left: -targ
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
				$(window).unbind("resize", handleArrows);
				$(window).bind("resize", handleArrows);
				
				
				/*
				 * User jquery.event.move plugin
				 * to animate shelf movement 
				 * on touch devices
				 */
				if (wholeShelf && $("html").hasClass("touch")){
					/*
					wholeShelf.bind("movestart", function(e){
						
						if ((e.distX > e.distY && e.distX < -e.distY) || (e.distX < e.distY && e.distX > -e.distY)) {
							e.preventDefault();
  						}
					}).bind("move", function(e){
						var startLeft = parseInt(wholeShelf.css("left").replace("px", ""));
						wholeShelf.css({"left": startLeft + (e.deltaX)});
					}).bind("moveend", function(e){
						
						var endLeft = parseInt(wholeShelf.css("left").replace("px", ""));
						var shelfWidth = shelf.width();
						
						if (endLeft > 0){	// Far left
							wholeShelf.animate({"left": 0}, 400, "easeOutCirc", function(){
								cur = 0;
								where = cur / itemWidth;
								handleArrows();
							});
						}
						else if (-(endLeft) > maxLeft){	// Far Right
							
							wholeShelf.animate({"left": -(maxLeft)}, 400, "easeOutCirc", function(){
								cur = maxLeft;
								where = cur / itemWidth;
								handleArrows();
							});
						}
						else{
							var whereToGo = parseInt(endLeft / itemWidth);
							if (e.deltaX < 0){
								whereToGo -= 1;
							}
							whereToGo = whereToGo * itemWidth;
							
							if (-(whereToGo) > maxLeft){
								whereToGo = -(maxLeft);
							}
							
							wholeShelf.animate({"left": whereToGo}, 400, "easeOutCirc", function(){
								cur = -(parseInt(wholeShelf.css("left").replace("px", "")));
								where = cur / itemWidth;
								handleArrows();
							});
						}
					});
					*/
					
					var xxx;
					var startLeft;
					var movingThisShelf = false;
					
					
					document.addEventListener('touchstart', function(event){
						movingThisShelf = false;
						var touch = event.touches[0];
						startLeft = parseInt(wholeShelf.css("left").replace("px", ""));
						xxx = touch.pageX;
						var yyy = touch.pageY;
						
						if (xxx > shelfViewBoundaries[0][0] && yyy > shelfViewBoundaries[0][1]){
							if (xxx < shelfViewBoundaries[0][0] + shelfViewBoundaries[1] && yyy < shelfViewBoundaries[0][1] + shelfViewBoundaries[2]){
								movingThisShelf = true;
							}
						}
					});
					
					document.addEventListener('touchmove', function(event){
						
						if (movingThisShelf){
							
							var touch = event.touches[0];
							var x = touch.pageX
							var diff = xxx - x;
							
							if (diff > 10 || diff < -10){
								event.preventDefault();	
							}							
							
							
							wholeShelf.css({"left": startLeft - (diff)});
						}
					}, false);
					
					document.addEventListener('touchend', function(event){
						
						if (movingThisShelf){
							
							var endLeft = parseInt(wholeShelf.css("left").replace("px", ""));
							var shelfWidth = shelf.width();
							
							var touch = event.changedTouches[0];
							var x = touch.pageX
							var diff = xxx - x;
							
							
							if (endLeft > 0){	// Far left
								
								wholeShelf.animate({"left": 0}, 400, "easeOutCirc", function(){
									cur = 0;
									where = cur / itemWidth;
									handleArrows();
								});
								
							}
							else if (-(endLeft) > maxLeft){	// Far Right
								
								wholeShelf.animate({"left": -(maxLeft)}, 400, "easeOutCirc", function(){
									cur = maxLeft;
									where = cur / itemWidth;
									handleArrows();
								});
							}
							else{
								var whereToGo = parseInt(endLeft / itemWidth);
								
								if (diff > 0){
									whereToGo -= 1;
								}
								whereToGo = whereToGo * itemWidth;
								
								if (-(whereToGo) > maxLeft){
									whereToGo = -(maxLeft);
								}
								
								wholeShelf.animate({"left": whereToGo}, 400, "easeOutCirc", function(){
									cur = -(parseInt(wholeShelf.css("left").replace("px", "")));
									where = cur / itemWidth;
									handleArrows();
								});
							}
						}
						movingThisShelf = false;
					});
				}
				
			};
			
			
			/*
			 * If we have a cookie name to set, set it 
			 * based on the currently selected form>select
			 */
			if(settings.cookie){
				var val = shelf.find("form select").val();
				if (val != ""){
					$.cookie(settings.cookie, val, {expires:7});
				}
				else{
					$.cookie(settings.cookie, "None", {expires: -1});
				}
			}		
			
			
			/*
			 * Right/left shelf arrows
			 * create, added/removed to/from shelf later
			 */			
			leftArrow = $("<a class='shelf-arrow shelf-arrow-left' href='#'><span data-icon='<' aria-hidden='true'></span><span class='visuallyhidden'>Next Page</span></a>");
			rightArrow = $("<a class='shelf-arrow shelf-arrow-right' href='#'><span data-icon='>' aria-hidden='true'></span><span class='visuallyhidden'>Previous Page</span></a>");
			
			
			/*
			 * Swift step: 
			 * Moving via position dots
			 */
			var bindSwiftStep = function(a, i, per){
				a.unbind("click");
				a.click(function(e){
					e.preventDefault();
					var targ;
					
					if ( i >= 0 ){
						var px = i * per * itemWidth;
						if (px > maxWidth - shelf.width()){
							px = maxWidth - shelf.width();
						}
						
						targ = "-" + (px) + "px";
						where = px / itemWidth;
						cur = px;
						
					}
					else{
						targ = -(maxLeft);
						cur = maxLeft;
						where = cur / itemWidth;
					}
					
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
			 		
			 		// Set a bunch of "global" variables
			 		maxLeft = itemWidth * numItems - shelf.width();
			 		
				 	numSteps = Math.ceil(maxWidth / shelf.width());
				 	
				 	var perSlide = Math.floor(shelf.width() / itemWidth);	
				 	
				 	// Figure out where we are on the shelf before the latest movement
				 	if (cur >= maxLeft){
				 		curStep = Math.ceil((cur / itemWidth) / perSlide);
				 	}	
				 	else{
				 		curStep = Math.floor((cur / itemWidth) / perSlide);				 			
				 	}
				 	
				 	// If we are into the shelf but not yet at the end, increment the current step
				 	if (cur > 0 && cur < Math.floor(shelf.width() / itemWidth) * itemWidth){
				 		curStep += 1;
				 	}
				 	
				 	// if we aren't yet at the end of the shelf, but we will be next time, adjust it so it doesn't show the 'last' dot
				 	if (cur < maxLeft && cur + parseInt(shelf.width() / itemWidth) * itemWidth >= maxLeft){
				 		curStep = numSteps - 2;
				 	}
				 	
				 	// Adjust for shelves with only 2 pages
				 	if (curStep >= numSteps){
				 		curStep = numSteps - 1;
				 	}
				 	
				 	// build shelf step dots, fill in the correct one
				 	for (var i = 0; i < numSteps; i++){
				 		var li;
				 		var iPlus = i + 1;
				 		
				 		if (i == curStep){
				 			li = $("<li><a class='shelf-step-cur' href='#'><span class='visuallyhidden'>Page " + iPlus + "</span></a></li>").appendTo(shelfSteps);
				 		}
				 		else{
				 			li = $("<li><a href='#'><span class='visuallyhidden'>Page " + iPlus + "</span></a></li>").appendTo(shelfSteps);
				 		}
				 		
				 		circ = li.find("a");
				 		
				 		if (i < numSteps - 1){
				 			bindSwiftStep(circ, i, perSlide);
				 		}
				 		else{
				 			bindSwiftStep(circ);	
				 		}				 		
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
			 	loadImages();
			 	drawShelfBoundaries();
			 	settings.afterMoveEnd((Math.round(where) + perSlide), perSlide);
			 };
			 
			 
			var drawShelfBoundaries = function(){
				var view = shelf.find(".shelf-view");
				var offset = view.offset();
				var topLeft = [offset.left, offset.top];
				var w = view.width();
				var h = view.height();
				
				//$("<div style='background:#f00' />").css({"position": "absolute", "left": offset.left, "top": offset.top, "width": w, "height": h, "z-index": "99"}).appendTo("body");
				shelfViewBoundaries = [topLeft, w, h];
				//l(shelfViewBoundaries);
			};
			 
			/*
			 * Hiding/showing arrows 
			 * based on shelf position
			 */
			var handleArrows = function(){
				if (cur == 0){
					leftArrow.addClass("hidden");
				}
				else{
					leftArrow.removeClass("hidden");
				}
				if (cur < maxWidth - shelf.width()){
					rightArrow.removeClass("hidden");
				}
				else{
					rightArrow.addClass("hidden");
				}
				
				handleShelfPosition();
				
			};
			
			var progress = $(".shelf-ajax-loader");
			if (progress.length < 1){
				progress = $("<p class='shelf-ajax-loader'><img src='" + siteVars("img") + "ajax-loader-bar.gif'/></p>");
				progress.appendTo($("body"));
			}
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
			loadImages();			
		});
	};
})( jQuery );


						