/*
 * Podiobooks Shelf plugin
 * Custom carousel bookshelves for Podiobooks
 *
 *
 * Version: 0.9.1
 *
 *
 * History:
 *
 * 0.1: 	Initial plugin creation
 * 0.2: 	Internalized checking for change form, adding binding for onChange
 * 0.3: 	Added some more settings for custom classes
 * 0.4: 	Shelf position indicator
 * 0.5: 	Support for shelves that don't need ajax calls
 * 0.6: 	Uses 'find' instead of 'children' for digging up relevant shelf peices
 * 0.7: 	Allows for shelf creation based on static content (i.e. no need to ajax on first load)
 * 0.8: 	Allows blank incoming cookies to delete the existing cookie
 * 0.9: 	Dynamic touch-sliding for adjustable-width shelves
 *			Shelf width no longer needs to be a full item width
 *			Callback hooks for "after movement" of shelves;
 *			Adding option for turning off positioning of shelf steps
 * 0.9.1:	Native touch events
 * 			Easing to settings
 *			Rubber Band Strength to settings
 *
 */

(function( $ ){

	$.fn.pbShelf = function( options ) {
  
		var settings = {
			"cookie"				:		null,
			"shelfItem"				:		".shelf-item",
			"shelfItemCover"		:		".shelf-cover",
			"clearShelfFirst"		:		false,
			"afterMoveEnd"			:		function(titlesDeep, perSlide){},
			"url"					:		null,
			"positionShelfSteps"	:		true,
			"ajaxLoaderImage"		:		"img/ajax-loading.gif",
			"easeFunction"			:		"easeOutCirc",
			"rubberBandStrength"	:		3
		};
		
		return this.each(function(){
			
			if (options){
				$.extend(settings, options);
			}
			
			if (!($.easing)){
				settings.easeFunction = null;
			}
			
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
				l("maxLeft : " + maxLeft);
				l("shelfViewBoundaries" + shelfViewBoundaries);
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
			var shelfViewBoundaries = []; // [[<offset left>, <offset top>], <shelf width>, <shelf height>]
			
			/*
			 * Some shelf element localization
			 */
			var wholeShelf;
			
			var shelf = $(this);
			
			var shelfSteps;
			var leftArrow;
			var rightArrow;
						
			/*
			 * Store the shelf as local variable,
			 * Set shelf height
			 *
			 * (otherwise it compresses when elements are removed)
			 */
			shelf.height(shelf.height());
			
			
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
						itemWidth = parseInt(item.width(), 10) + parseInt(item.css("padding-left"), 10) + parseInt(item.css("padding-right"), 10) + parseInt(item.css("margin-left"), 10) + parseInt(item.css("margin-right"), 10);
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
							var targ = cur + parseInt(shelfWidth / itemWidth, 10) * itemWidth;
														
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
							}, 600, settings.easeFunction);
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
							var targ = parseInt(cur / itemWidth, 10) * itemWidth - parseInt(shelfWidth / itemWidth, 10) * itemWidth;
							
							if (cur % itemWidth !== 0){
								targ += itemWidth;
							}
							
							
							if (targ <= 0){
								cur = 0;
								targ = 0;
							}
							else{
								cur = targ;
							}
							
							where = cur / itemWidth;
							if (where < 0){
								where = 0;
							}
							
														
							wholeShelf.animate({
								left: -targ
							}, 600, settings.easeFunction);
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
				 * Native touch events
				 * to animate shelf movement
				 * on touch devices
				 */
				if (wholeShelf && $("html").hasClass("touch")){
					
					var startX;
					var startY;
					
					var startLeft;
					var movingThisShelf = false;
					
					var slidingShelf = false;
					var scrollingInstead = false;
					var xxx = 0;
					var yyy = 0;

					document.addEventListener('touchstart', function(event){
						
						movingThisShelf = false;
						slidingShelf = false;
						scrollingInstead = false;
						xxx = 0;
						yyy = 0;
						
						var touch = event.touches[0];
						
						startLeft = parseInt(wholeShelf.css("left").replace("px", ""), 10);
						startX = touch.pageX;
						startY = touch.pageY;
						
						if (startX > shelfViewBoundaries[0][0] && startY > shelfViewBoundaries[0][1]){
							if (startX < shelfViewBoundaries[0][0] + shelfViewBoundaries[1] && startY < shelfViewBoundaries[0][1] + shelfViewBoundaries[2]){
								movingThisShelf = true;
							}
						}
					}, false);
					
					document.addEventListener('touchmove', function(event){
						
						if (movingThisShelf){
							
							var touch = event.touches[0];
							var x = touch.pageX;
							var y = touch.pageY;
							var deltaX;
							var deltaY;
							
							if (startX > x){	// sliding finger left
								deltaX = startX - x;
							}
							else{				// sliding finger right
								deltaX = -(x - startX);
							}
							
							if (startY > y){	// sliding finger up
								deltaY = startY - y;
							}
							else{				// sliding finger down
								deltaY = -(y - startY);
							}
							
							// If we havent yet decided whether we are sliding a shelf or scrolling,
							// Make that decision now
							if (!slidingShelf && !scrollingInstead){
								var xxx = Math.abs(deltaX);
								var yyy = Math.abs(deltaY);

								if (xxx > 10 && xxx > yyy){
									slidingShelf = true;
								}
								else if (yyy > 10 & !scrollingInstead){
									scrollingInstead = true;
								}
							}

							// If we're sliding, prevent scrolling
							if (slidingShelf){
								event.preventDefault();
							}
							
							// As long as we haven't decided that we are scrolling,
							// move the shelf
							if (!scrollingInstead){								
								var whereTo = startLeft - (deltaX);
								
								if (whereTo > 0){
									whereTo /= settings.rubberBandStrength;
								}
								else if (-(whereTo) > maxLeft){
									whereTo = -(maxLeft) + ((whereTo + maxLeft) / settings.rubberBandStrength);									
								}
								
								wholeShelf.css({"left": whereTo});
							}
						}
					}, false);
					
					document.addEventListener('touchend', function(event){
						
						if (movingThisShelf){
							
							var endLeft = parseInt(wholeShelf.css("left").replace("px", ""), 10);
							var shelfWidth = shelf.width();
							
							var touch = event.changedTouches[0];
							var x = touch.pageX;
							var diff = startX - x;
							var diffY = Math.abs(Math.abs(touch.pageY) - Math.abs(startY));
														
							if (endLeft > 0){	// Far left
								
								wholeShelf.animate({"left": 0}, 400, settings.easeFunction, function(){
									cur = 0;
									where = cur / itemWidth;
									handleArrows();
								});
								
							}
							else if (-(endLeft) > maxLeft){	// Far Right
								
								wholeShelf.animate({"left": -(maxLeft)}, 400, settings.easeFunction, function(){
									cur = maxLeft;
									where = cur / itemWidth;
									handleArrows();
								});
							}
							else{
								var whereToGo = parseInt(endLeft / itemWidth, 10);
								
								if (diff > 0 && Math.abs(diffY) < Math.abs(diff) && !scrollingInstead){
									whereToGo -= 1;
								}
								whereToGo = whereToGo * itemWidth;
								
								if (-(whereToGo) > maxLeft){
									whereToGo = -(maxLeft);
								}
								
								wholeShelf.animate({"left": whereToGo}, 400, settings.easeFunction, function(){
									cur = -(parseInt(wholeShelf.css("left").replace("px", ""), 10));
									where = cur / itemWidth;
									handleArrows();
								});
							}
						}
						movingThisShelf = false;
						slidingShelf = false;
						scrollingInstead = false;
						xxx = 0;
						yyy = 0;

					}, false);
				}
			};
			
			
			/*
			 * If we have a cookie name to set, set it
			 * based on the currently selected form>select
			 */
			if(settings.cookie){
				var val = shelf.find("form select").val();
				if (val !== ""){
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
					}, 600, settings.easeFunction);
					
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
					if (cur < maxLeft && cur + parseInt(shelf.width() / itemWidth, 10) * itemWidth >= maxLeft){
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
					if (settings.positionShelfSteps){
						shelfSteps.css({'left':(shelf.width() / 2 - shelfSteps.width() / 2) / shelf.width() * 100 + "%"});
					}


					/*
					* If there is only 1 step and there
					* are less shelf items than shelf spaces,
					* hide the shelf progress indicator
					*/
					if (numSteps < 2 && shelf.find(settings.shelfItem).length < perSlide){
						shelfSteps.children().remove();
					}
					loadImages();
					drawShelfBoundaries();
					settings.afterMoveEnd((Math.round(where) + perSlide), perSlide);
				}
			};
			 
			
			/*
			 * Figure out where the boundaries of each shelf are
			 */
			var drawShelfBoundaries = function(){
				var view = shelf.find(".shelf-view");
				var offset = view.offset();
				var topLeft = [offset.left, offset.top];
				var w = view.width();
				var h = view.height();
				shelfViewBoundaries = [topLeft, w, h];
			};
			
			
			/*
			 * Hiding/showing arrows
			 * based on shelf position
			 */
			var handleArrows = function(){
				if (cur === 0){
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
				progress = $("<p class='shelf-ajax-loader'><img src='" + settings.ajaxLoaderImage + "' /></p>");
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