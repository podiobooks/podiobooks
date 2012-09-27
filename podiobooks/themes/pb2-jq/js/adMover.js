$(function(){
	$('[data-move-ad]').each(function(){
		var wrapper = $(this);
		target = "#" + wrapper.data("move-ad");
		wrapper.appendTo(target);
	});
});
