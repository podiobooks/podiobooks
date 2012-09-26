$(function(){
	
	$(".consume-list").each(function(){
		var list = $(this);
		
		var slug = list.data("title-slug");
		
		list.find("#consume-itunes>a").each(function(){
			$(this).click(function(){
				_gaq.push(['_trackEvent', 'Consume', 'DetailPage-ViewInITunes', slug]);
			});				
		});
		
		
		list.find("#consume-amazon>a").each(function(){
			$(this).click(function(){
				_gaq.push(['_trackEvent', 'Consume', 'DetailPage-BuyFromAmazon', slug]);
			});
		});
		
		list.find("#consume-smashwords>a").each(function(){
			$(this).click(function(){
				_gaq.push(['_trackEvent', 'Consume', 'DetailPage-BuyFromSmashwords', slug]);
			});
		});
		
		list.find("#consume-rss>a").each(function(){
			$(this).click(function(){
				_gaq.push(['_trackEvent', 'Consume', 'DetailPage-RSSFeed', slug]);
			});
		});
		
		list.find("#consume-rss>a").each(function(){
			$(this).bind("contextmenu", function(){
				_gaq.push(['_trackEvent', 'Consume', 'DetailPage-RSSFeedRC', slug]);
			});
		});
		
		
		
	});
	
	$(".donate-box").each(function(){
		var wrapper = $(this);
		var slug = wrapper.data("title-slug");
		
		wrapper.find("#title-donate-submit").each(function(){
			
			var btn = $(this);
			var form = btn.parents("form");
			
			var amount = form.find('input[name="amount"]').val();
			
			form.bind("submit", function(){
				_gaq.push(['_trackEvent', 'Donate', 'DetailPage-Donate', slug, amount]);
			});
			
		});	
	});
	
	
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
