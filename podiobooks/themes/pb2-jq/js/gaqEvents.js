$(function () {

    /*
     * GA events for elements in the 'ways to consume this book' list
     *
     * The .consume-list template is actually repeated in the markup
     * 		So, we're going to handle each iteration of the list separately.
     */
    $(".consume-list").each(function () {
        var list = $(this);

        var slug = list.data("title-slug");

        list.find("#consume-itunes>a").each(function () {
            $(this).click(function () {
                _gaq.push(['_trackEvent', 'Consume', 'DetailPage-ViewInITunes', slug]);
            });
        });


        list.find("#consume-amazon>a").each(function () {
            $(this).click(function () {
                _gaq.push(['_trackEvent', 'Consume', 'DetailPage-BuyFromAmazon', slug]);
            });
        });

        list.find("#consume-smashwords>a").each(function () {
            $(this).click(function () {
                _gaq.push(['_trackEvent', 'Consume', 'DetailPage-BuyFromSmashwords', slug]);
            });
        });

        list.find("#consume-rss>a").each(function () {
            $(this).click(function () {
                _gaq.push(['_trackEvent', 'Consume', 'DetailPage-RSSFeed', slug]);
            });
        });

        list.find("#consume-rss>a").each(function () {
            $(this).bind("contextmenu", function () {
                _gaq.push(['_trackEvent', 'Consume', 'DetailPage-RSSFeedRC', slug]);
            });
        });


    });
	
	
    /*
     * GA events for elements in the 'Donate to this author' form
     *
     * The .donate-box template is actually repeated in the markup
     * 		So, we're going to handle each iteration of the list separately.
     */
    $(".donate-box").each(function(){
    	
    	var box = $(this);
    	var slug = box.data("title-slug");
    	
    	box.find("#title-donate-submit").click(function(){
			var form = $(this).parents("form");
			var amount = parseInt(form.find('input[name="amount"]').val());
			_gaq.push(['_trackEvent', 'Donate', 'DetailPage-Donate', slug, amount]);
    	});
    	
    });

    /*
     * GA events for homepage shelves
     */
    $(".shelf").delegate(".shelf-item-heading a", "click", function(){
        var link = $(this);
        link.click(function (ev) {
            var slug = link.data("title-slug");
            if (slug) {
                _gaq.push(['_trackEvent', 'Widgets', 'HomePage-ShelfTitleClick', slug, 1]);
            }
        });
    });
    
	$(".shelf").delegate(".shelf-cover", "click", function(){
        var img = $(this);
        var link = img.parent();
        link.click(function (ev) {
            var slug = img.data("title-slug");
            if (slug) {
                _gaq.push(['_trackEvent', 'Widgets', 'HomePage-ShelfTitleClick', slug, 0]);
            }
        });
    });

    $(".shelf-wrapper").delegate(".shelf-select-form select", "change", function (ev) {
        _gaq.push(['_trackEvent', 'Widgets', 'HomePage-ShelfDropDown', $(this).val()]);
    });

});
