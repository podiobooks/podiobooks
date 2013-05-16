$(function () {
	$(".title-tabs").each(function(){
		$(this).tabs({
	    	ajaxOptions:{
		        error:function (xhr, status, index, anchor) {
		            $(anchor.hash).html("Sorry, an error occurred, and this tab couldn't be loaded.");
	            }
	        }
    	});
    });
});