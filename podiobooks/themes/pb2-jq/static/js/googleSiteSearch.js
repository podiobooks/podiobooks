/*
 * Use V2 of searach API
 * https://developers.google.com/custom-search/docs/element#cse-element
 * https://developers.google.com/custom-search/docs/element#supported_attributes
 */


if (google && google.setOnLoadCallback){
	google.setOnLoadCallback(function () {
	    if ($("body").hasClass("search-results-page")){
	        google.search.Csedr.addOverride("pb_");
	        google.search.cse.element.render({
	            div: "cse",
	            tag: 'search',
	            attributes: {
	                resultsUrl: '/search/snip/',
	                webSearchResultSetSize: 20,
	                webSearchSafesearch: "active",
	                enableHistory: true,
	                newWindow: false,
	                linkTarget: null
	            }
	        });
	    }
	});
}

