$(function(){
	$(".shelf").each(function(){
		var shelf = $(this);
		shelf.height(shelf.height());
		
		shelf.addClass('fun-shelf');
		
		$.ajax({
			method:"get",
			url:"/lazy/featured/",
			success:function(data){
				
				$(data).appendTo("#featured-shelf");
				
				$("#featured-shelf>div").wrapAll("<div class='whole-shelf'/>");
				$("#featured-shelf>.whole-shelf").wrap("<div class='shelf-view'/>");
				
				var leftArrow = $("<a class='shelf-arrow shelf-arrow-left' href='#'>previous</a>").appendTo(shelf);
				var rightArrow = $("<a class='shelf-arrow shelf-arrow-right' href='#'>next</a>").appendTo(shelf);
		
				rightArrow.click(function(e){
					e.preventDefault();
					if (where < 3){
						where++;
						
						var targ = "-" + (($(".whole-shelf>div:first").width()+12) * where) + "px";
						
						$(".whole-shelf").animate({
							left:targ
						},600,"easeOutCirc");
					}
				});
				
				leftArrow.click(function(e){
					e.preventDefault();
					if (where > 0){
						where--;
						
						var targ = "-" + (($(".whole-shelf>div:first").width()+12) * where) + "px";
						
						$(".whole-shelf").animate({
							left:targ
						},600,"easeOutCirc");
					}
				});
				
			}
		});
		
		
		
	});
	
});
// Todo: Localize as $.data
var where = 0;