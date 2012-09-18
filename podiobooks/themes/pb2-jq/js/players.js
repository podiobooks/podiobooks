$(function(){
	
	var episodes = $(".episode-audio-link:first");
	var placement = $(".title-description p:first");
	var htmlAudio = $("html").hasClass("audio");
	// check for HTML5 audio capabilities first
	if (episodes.length > 0){
		// check for MP3 capabilities
		var browserAudio = new Audio();
		episodes.each(function(){
			
			var link = $(this);
			var href = link.attr("href");
			var audio = $("<aside id='title-first-chapter-player' class='first-chapter'></aside>").insertBefore(placement);
			
			if (htmlAudio && browserAudio && browserAudio.canPlayType("audio/mpeg")){
				$("<h2>Play First Chapter</h2><audio controls><source src='" + href + "' type='audio/mp3' codecs='mp3'></audio>").appendTo(audio);
				
			}
			else{
				var replaceMe = $("<span id='replaceMeYo' />").appendTo(audio);
				AudioPlayer.embed(replaceMe.attr("id"), {
					autostart:"no",
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
				
				$("<h2>Play First Chapter</h2>").prependTo(audio);
			}
			$(".title-details-infobar").insertAfter(audio);
		});
	}
	
});
