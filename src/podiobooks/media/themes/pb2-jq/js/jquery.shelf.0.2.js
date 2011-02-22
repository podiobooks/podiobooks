/*
 * History:
 * 
 * 0.1: Initial plugin creation
 * 0.2: Internalized checking for change form, adding binding for onChange
 */
(function( $ ){

	$.fn.pbShelf = function( options ) {
  
		var settings = {
			'url' 			: 		'/',
			"cookie"		: 		null,
			"checkCookie"	: 		false
		};
		
		return this.each(function(){
			
			if (options){
				$.extend(settings,options);
			}
			
			var where = 0;
			var cur = 0;
			var maxWidth = 0;
			var itemWidth = 0;
						
			var shelf = $(this);
			shelf.height(shelf.height());
			
			shelf.children().each(function(){
				if (!($(this).is("form"))){
					$(this).html("");
					$(this).remove();
				}
			});
			
			
			
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
	
			if (settings.checkCookie){
				if($.cookie(settings.cookie)){
					if (shelf.has("form select")){
						shelf.find("form select").val($.cookie(settings.cookie));
						settings.url += $.cookie(settings.cookie);
					}					
				}
			}
			
			if(settings.cookie){
				$.cookie(settings.cookie,shelf.find("form select").val(),{expires:7});
			}		
			
			var progress = $("<p class='shelf-ajax-loader'><img src='" + siteVars("img") + "ajax-loader-bar.gif'/></p>");
			
			progress.appendTo($("body")).hide();
			progress.appendTo(shelf).show();
			
			shelf.addClass('fun-shelf');
			
			var leftArrow = $("<a class='shelf-arrow shelf-arrow-left' href='#'></a>");
			var rightArrow = $("<a class='shelf-arrow shelf-arrow-right' href='#'></a>");
			
			
			
			var status = function(){
				l("cur: " + cur);
				l("where: " + where);
				l("maxWidth: "  + maxWidth);
				l("itemWidth: " + itemWidth);
			};
				
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
			
			
			$.ajax({
				method:"get",
				url:settings.url,
				success:function(data){
					
					$(data).appendTo(shelf);
					
					if(shelf.find(".shelf-item").length){
						
						$(shelf).find(".shelf-cover img:not(.shelf-cover-loading)").each(function(){
							
							var img = $(this);
							
							img.hide();
							var l = $("<img class='shelf-cover-loading' src='" + siteVars("img") + "loading.gif' />").appendTo(img.parents(".shelf-cover"));
							
							img.load(function(){
								l.remove();
								img.fadeIn();
								
							});
						});
						
						progress.hide();
						
						var shelfItems = shelf.find(".shelf-item");
						var w = 0;
						
						shelfItems.each(function(){
							itemWidth = parseInt($(this).width()) + parseInt($(this).css("padding-left")) + parseInt($(this).css("padding-right")) + parseInt($(this).css("margin-left")) + parseInt($(this).css("margin-right"));
							w += itemWidth;
						});
						
						maxWidth = w;
						
						shelf.children("div").wrapAll("<div class='whole-shelf'/>");
						var wholeShelf = shelf.children(".whole-shelf");
						wholeShelf.wrap("<div class='shelf-view'/>");
						
						
						
						leftArrow.appendTo(shelf);
						rightArrow.appendTo(shelf);
						
						handleArrows();
					}
					else{
						progress.hide();
					}
					
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
					
					wholeShelf.swipe({
						swipeLeft:function(event){
							rightArrow.trigger("click");	
						},
						swipeRight:function(event){
							leftArrow.trigger("click");
						},
						swipeStatus:function(event, phase, direction, distance){
							/*
							if (direction == "left" && cur < maxWidth - shelf.width()){
								wholeShelf.animate({"left": parseInt(wholeShelf.css("left").replace("px","")) - distance},1);
								cur -= parseInt(wholeShelf.css("left").replace("px","")) - distance;
								status();
							}
							if (direction == "right" && cur > 0){
								wholeShelf.animate({"left":parseInt(wholeShelf.css("left").replace("px","")) + distance},1);
								cur += parseInt(wholeShelf.css("left").replace("px","")) + distance;
								status();								
							} 
							*/				
						},
						allowPageScroll:"vertical"						
					});
					
				}
			});
		});
	};
})( jQuery );