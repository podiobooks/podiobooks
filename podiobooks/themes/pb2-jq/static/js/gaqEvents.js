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
     * GA events for elements in the 'Tip this author' form
     *
     * The .tipjar-box template is actually repeated in the markup
     * 		So, we're going to handle each iteration of the list separately.
     */
    $(".tipjar-box").each(function(){

		var box = $(this);
		var slug = box.data("title-slug");

		box.find("#title-tipjar-submit").click(function(){
			var form = $(this).parents("form");
			var amount = parseInt(form.find('input[name="amount"]').val());
			_gaq.push(['_trackEvent', 'TipJar', 'DetailPage-TipJar', slug, amount]);
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


    /*
     * Shelf 'next' button
     */
    $(".shelf-wrapper").delegate(".shelf-arrow-left", "click", function(){

		var arrow = $(this);
		var rightArrow = arrow.siblings(".shelf-arrow-right");
		var numClicks = parseInt(rightArrow.data("num-clicks"));

		if (!numClicks){
			numClicks = 0;
		}
		else{
			numClicks -= 1;
		}

		rightArrow.data("num-clicks", numClicks);
    });
    $(".shelf-wrapper").delegate(".shelf-arrow-right", "click", function(){

		var arrow = $(this);
		var numClicks = parseInt(arrow.data("num-clicks"));

		var shelf = arrow.parents(".shelf").find(".shelf-pages");
		var threshold = parseInt(shelf.data("threshold"));

		if (!threshold){
			threshold = 0;
			shelf.data("threshold", threshold);
		}


		if (!numClicks){
			numClicks = 1;
			arrow.data("num-clicks", numClicks);
		}
		else{
			numClicks++;
			arrow.data("num-clicks", numClicks);
		}

		if (numClicks > threshold){
			threshold += 1;
			shelf.data("threshold", threshold);
			_gaq.push(['_trackEvent', 'Widgets', 'HomePage-ShelfNextButton', shelf.attr("id"), (numClicks+1)]);
		}

    });

    $("#titleArticle").on("click", ".rate-title", function(ev){
		var vote = $(this).find(".visuallyhidden:first").text();
		var slug = $("#titleArticle").data('title-slug');
		var voteValue;

		if (vote === 'Promote'){
			voteValue = 1;
		}
		else{
			voteValue = 0;
		}

		_gaq.push(['_trackEvent', 'Rating', 'DetailPage-RatingWidget', slug, voteValue]);
    });

});
