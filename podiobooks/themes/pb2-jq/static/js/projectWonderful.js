$(function(){

	var loadAds = function(){
		function pw_load(){
			if(arguments.callee.z)return;else arguments.callee.z=true;
			var d=document;var s=d.createElement('script');
			var x=d.getElementsByTagName('script')[0];
			s.type='text/javascript';s.async=true;
			s.src='//www.projectwonderful.com/pwa.js';
			x.parentNode.insertBefore(s,x);
		}
		if (window.attachEvent){
			window.attachEvent('DOMContentLoaded',pw_load);
			window.attachEvent('onload',pw_load);
		}
		else{
			window.addEventListener('DOMContentLoaded',pw_load,false);
			window.addEventListener('load',pw_load,false);
		}
	};

	if ($(".title-details-extras").length > 0){
		var pWonderfulContainer = $('<div id="titleDetailsPWonderfulSky" class="wide-skyscraper-ad" />').insertAfter("#wide-skyscraper-ad");
		$('<div id="pw_adbox_70791_3_0"></div><script type="text/javascript"></script><noscript><map name="admap70791" id="admap70791"><area href="http://www.projectwonderful.com/out_nojs.php?r=0&c=0&id=70791&type=3" shape="rect" coords="0,0,160,600" title="" alt="" target="_blank" /></map><table cellpadding="0" cellspacing="0" style="width:160px;border-style:none;background-color:#ffffff;"><tr><td><img src="http://www.projectwonderful.com/nojs.php?id=70791&type=3" style="width:160px;height:600px;border-style:none;" usemap="#admap70791" alt="" /></td></tr><tr><td style="background-color:#ffffff;" colspan="1"><center><a style="font-size:10px;color:#0000ff;text-decoration:none;line-height:1.2;font-weight:bold;font-family:Tahoma, verdana,arial,helvetica,sans-serif;text-transform: none;letter-spacing:normal;text-shadow:none;white-space:normal;word-spacing:normal;" href="http://www.projectwonderful.com/advertisehere.php?id=70791&type=3" target="_blank">Ads by Project Wonderful!  Your ad here, right now: $0</a></center></td></tr></table></noscript>').appendTo("#titleDetailsPWonderfulSky");
	}

	loadAds();

});
