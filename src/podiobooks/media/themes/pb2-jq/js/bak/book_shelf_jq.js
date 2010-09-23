/* Attaches a jQuery jCarouselLite object to a given shelf
 * 
 * shelfId: String with the CSS ID of the shelf to attach to (e.g. 'featuredPodiobooksShelf')
 * shelfItemWidth: Integer representing the number of pages the shelf should have (4)
 */
function attachCarousel(shelfId, shelfItemWidth){
	var shelfSelector = "#" + shelfId; //jQuery wants the ids prefaced with #
	var shelfPageCount = $(shelfSelector + ' ul li').size();
	
	/* Build array of page jump-to buttons, and produce HTML from it */
	var shelfControllerButtons = []; // Used below to tell jCarouselList what our controls are
	var shelfControllerHTML = ""; // Used to build the HTML for the page buttons
	if (shelfPageCount > 1) { //Don't build controls for only one page of items
		for (var i = shelfPageCount-1; i >= 0; i--) { //Have to count all the way down to page 0
			var buttonId = shelfId + "_page_" + i + "_button";
			shelfControllerButtons[i] = "#" + buttonId;
			shelfControllerHTML += '<div id="' + buttonId + '" class="pb-shelf-controller-button"><div class="pb-shelf-controller-icon"></div></div>';
		}
	} else {
		shelfControllerHTML = ""; //Wipe out the button HTML if there is only one page.
	}
	$(shelfSelector + 'Controller').html(shelfControllerHTML); //Update controller HTML with new buttons
	
	/* Attach the jCarouselLite Object to the shelf */
    $(shelfSelector).jCarouselLite({
        btnNext: shelfSelector + "Container .pb-shelf-end-right",
        btnPrev: shelfSelector + "Container .pb-shelf-end-left",
        scroll: 1,
        visible: 1,
        circular: false,
        speed: 800,
        easing: "easeInQuad",
        btnGo: shelfControllerButtons,
        afterEnd: function(a){
            setCarouselButtons(shelfId, $(a).attr('id'));
        }
    });
	
	// This line should be a fadeIn(), but the timing is off with the jCarouselLite delay
	$(shelfSelector).css('opacity', 1);  //Reveal styled div now to avoid FOUC
	
    /* Switch the right shelf end image to the the arrow version */
	if (shelfPageCount > 1) {
		$(shelfSelector + "Container .pb-shelf-end-right").removeClass("disabled");
		/* Light up the first Page Controller Button */
		setCarouselButtons(shelfId, shelfId + '_page_0');
	} else {
		$(shelfSelector + "Container .pb-shelf-end-left").addClass("disabled");
		$(shelfSelector + "Container .pb-shelf-end-right").addClass("disabled");
	}
}

/* Sets the buttons to the correct selected state based on the current page -
 * Called from the afterEnd hook in the carousel.
 */
function setCarouselButtons(shelfId, pageId){
    $('#' + shelfId + 'Controller .pb-shelf-controller-button').removeClass('selected');
    $('#' + pageId + '_button').addClass('selected');
}