function l(msg){
	if(window.console){
		console.log(msg);	
	}
}

$(function(){
	if ($("body").width() < 501){
		$("#djDebug").remove();
	}	
});
