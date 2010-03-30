/* Attaches a jQuery jCarouselLite object to a given shelf
 * 
 * shelfId: String with the CSS ID of the shelf to attach to ('featuredPodiobooksShelf')
 * shelfTitleWidth: Integer representing the number of pages the shelf should have (4)
 */
function attachCarousel(shelfId, shelfTitleWidth){
	var shelfSelector = "#" + shelfId; //jQuery wants the ids prefaced with #
	
	/* Build array of page jump-to buttons, and produce HTML from it */
	var shelfControllerButtons = []; // Used below to tell jCarouselList what our controls are
	var shelfControllerHTML = ""; // Used to build the HTML for the page buttons
	for (var i = shelfTitleWidth; i > -1; i--) {
		var buttonId = shelfId + "_page_" + i + "_button";
		shelfControllerButtons[i] = "#" + buttonId;
		shelfControllerHTML += '<div id="' + buttonId + '" class="pb-shelf-controller-button"><div class="pb-shelf-controller-icon"></div></div>';
	}
	$(shelfSelector + 'Controller').append(shelfControllerHTML);
	
	/* Attach the jCarouselLite Object to the shelf */
    $(shelfSelector).jCarouselLite({
        btnNext: shelfSelector + "Container .pb-shelf-end-right",
        btnPrev: shelfSelector + "Container .pb-shelf-end-left",
        scroll: 1,
        visible: 1,
        circular: false,
        speed: 1000,
        easing: "easeInQuad",
        btnGo: shelfControllerButtons,
        afterEnd: function(a){
            setCarouselButtons(shelfId, $(a).attr('id'));
        }
    });
    /* Switch the right shelf end image to the the arrow version */
    $(shelfSelector + "Container .pb-shelf-end-right").removeClass("disabled");
	/* Light up the first Page Controller Button */
    setCarouselButtons(shelfId, shelfId + '_page_0');
}

/* Sets the buttons to the correct selected state based on the current page -
 * Called from the afterEnd hook in the carousel.
 */
function setCarouselButtons(shelfId, pageId){
    $('#' + shelfId + 'Controller .pb-shelf-controller-button').removeClass('selected');
    $('#' + pageId + '_button').addClass('selected');
}