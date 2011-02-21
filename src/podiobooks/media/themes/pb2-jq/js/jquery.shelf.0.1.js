(function( $ ){

	$.fn.pbShelf = function( options ) {
  
		var settings = {
			'url' 		: 		'/'
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
			var progress = $("<p class='shelf-ajax-loader'><img src='" + siteVars("img") + "ajax-loader-bar.gif'/></p>");
			l(siteVars("img"));
			progress.appendTo(shelf);
			
			
			shelf.addClass('fun-shelf');
			
			var leftArrow = $("<a class='shelf-arrow shelf-arrow-left' href='#'>previous</a>");
			var rightArrow = $("<a class='shelf-arrow shelf-arrow-right' href='#'>next</a>");
			
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
					
					progress.remove();
					
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
				}
			});
		});
	};
})( jQuery );