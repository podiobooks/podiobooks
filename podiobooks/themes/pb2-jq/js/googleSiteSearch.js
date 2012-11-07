/* 
 * Use V2 of searach API 
 * https://developers.google.com/custom-search/docs/element#cse-element
 * https://developers.google.com/custom-search/docs/element#supported_attributes
 */
$(function(){
    if ($("body").hasClass("search-results")){
        google.setOnLoadCallback(function () {     
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
        });
    }
});