$(function(){
	
	$(".shelf-item-heading a").each(function(){
		var link = $(this);
		link.click(function(ev){
			var slug = link.data("title-slug");
			if (slug){
				_gaq.push(['_trackEvent', 'Widgets', 'HomePage-ShelfTitleClick', slug, 1]);	
			}
		});
	});
	
	$(".shelf-cover").each(function(){
		var img = $(this);
		var link = img.parent();
		link.click(function(ev){
			var slug = img.data("title-slug");
			if (slug){
				_gaq.push(['_trackEvent', 'Widgets', 'HomePage-ShelfTitleClick', slug, 0]);
			}
		});
	});
	
	$(".shelf-wrapper").delegate(".shelf-select-form select", "change", function(ev){
		_gaq.push(['_trackEvent', 'Widgets', 'HomePage-ShelfDropDown', $(this).val()]);
	});
	
});
