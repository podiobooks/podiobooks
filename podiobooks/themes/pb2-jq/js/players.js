$(function(){
	
	var episodes = $(".episode-audio-link:first");
	var placement = $(".title-description p:first");
	var htmlAudio = $("html").hasClass("audio");
	var slug = $(episodes).parents("article").data("title-slug");
	var canPlayMp3 = false;
	if (htmlAudio){
		var browserAudio = new Audio();
		if(browserAudio && browserAudio.canPlayType("audio/mpeg")){
			canPlayMp3 = true;
		}
	}
	
	
	/* 
	 * href is location of audio file, 
	 * ele is where to put this thing, 
	 * autoPlay is whether or not the player should start automatically  
	 */
	var createHTML5Player = function(ele, href, autoPlay){	
		
		var str = ""
		
		if (autoPlay){
			str = " autoplay='autoplay' ";
		}
		
		$("<audio controls" + str + "><source src='" + href + "' type='audio/mp3' codecs='mp3'></audio>").appendTo(ele);
		
		var audioPlayer = ele.find("audio");
		audioPlayer.bind("play", function(){
			_gaq.push(['_trackEvent', 'Audio', 'DetailPage-First-Play', slug]);
		});
		
		_gaq.push(['_trackEvent', 'Audio', 'DetailPage-HTML5', slug]);
		
	};
	
	/* 
	 * href is location of audio file, 
	 * replaceMe is an element that will be replaced by the player
	 * autoPlay is whether or not the player should start automatically
	 *  
	 */
	var createFlashPlayer = function(replaceMe, href, autoPlay){
		
		if (autoPlay){ autoPlay = "yes"; }
		else{ autoPlay = "no"; }
		
		AudioPlayer.embed(replaceMe.attr("id"), {
			autostart:autoPlay,
			loop:"no",
			animation:"yes",
			remaining:"no",
			noinfo:"yes",
			initialvolume:100,
			buffer:5,
			width:290,
			download:"yes",
			transparentpagebg:"yes",
			bg:"d9e4f0",
			leftbg:"a9d4f9",
			lefticon:"06539e",
			voltrack:"06539e",
			volslider:"fefefe",
			rightbg:"06539e",
			rightbghover:"a9d4f9",
			righticon:"fefefe",
			righticonhover:"fefefe",
			loader:"06539e",
			track:"fefefe",
			tracker:"06539e",
			border:"06539e",
			skip:"666666",
			text:"6b6b6b", 
			soundFile:href
		});	
		
		_gaq.push(['_trackEvent', 'Audio', 'DetailPage-Flash', slug]);
	};
	
	
	if (episodes.length > 0){
		episodes.each(function(){
			
			var link = $(this);
			var href = link.attr("href");
			var audio = $("<aside id='title-first-chapter-player' class='first-chapter'></aside>").insertBefore(placement);
			
			if (canPlayMp3){					
				createHTML5Player(audio, href);
			}
			else{
				var flashReplaceMe = $("<span id='replaceMeYo' />").appendTo(audio);
				createFlashPlayer(flashReplaceMe, href);
			}
			
			$("<h2>Play First Chapter</h2>").prependTo(audio);
			$(".title-details-infobar").insertAfter(audio);
			
		});
	}
	
	/*
	$(".episode-list-title>a").each(function(i){
		$(this).click(function(ev){
			ev.preventDefault();
			var flashReplaceMe = $("<span id='play-ep-" + i + "' />").appendTo($(this).parents(".episode-list-item"));
			if (canPlayMp3){
				createHTML5Player(flashReplaceMe, $(this).attr("href"), true);
			}
			else{
				createFlashPlayer(flashReplaceMe, $(this).attr("href"), true);
			}
			
		});
	});
	
	*/
	
});
