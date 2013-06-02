$(function(){
	function tweetGo(d,s,id){
		var js,fjs=d.getElementsByTagName(s)[0];
		if(!d.getElementById(id)){
			js=d.createElement(s);js.id=id;
			js.src="//platform.twitter.com/widgets.js";
			fjs.parentNode.insertBefore(js,fjs);
		}
	};
	if ($(".twitter-share-button").length > 0){
		tweetGo(document,"script","twitter-wjs");
	}
	
	
	function plusGo() {
        var po = document.createElement('script'); po.type = 'text/javascript'; po.async = true;
        po.src = 'https://apis.google.com/js/plusone.js';
        var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(po, s);
   };
    if ($(".g-plusone").length > 0){
    	plusGo();
    }
    
    
	if ($(".fb-like").length > 0){
		likeGo(document, 'script', 'facebook-jssdk');
	}
    
});
