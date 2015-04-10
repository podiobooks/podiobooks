$(function () {
	$(".title-footer").clone().appendTo("#titleArticle");

	$(".title-tabs").each(function(){
		$(this).tabs({
			ajaxOptions:{
				error:function (xhr, status, index, anchor) {
					$(anchor.hash).html("Sorry, an error occurred, and this tab couldn't be loaded.");
				}
			},
			beforeLoad: function(event, ui){
				var loader = $("#loaderGif");
				loader.appendTo(ui.panel);
				loader.show();
			},
			load: function(event, ui){
				var loader = $("#loaderGif");
				loader.hide();
				loader.appendTo("body");
			}
		});
	});

	var myPlaylist = [];

	var cover = $(".title-details-header-cover .cover-image").attr("src");
	var author = $('.title-details-header [itemprop="author"] [itemprop="name"]').text();

	var placement = $(".title-details-extras .consumption-box");

	// if ($(".title-details-extras .award-show").length > 0){
	// 	placement = $(".award-show");
	// }

	var playerWrap = $("<div class='player-wrap'><h2 class='player-wrap-title'>Episode Player</h2></div>").insertAfter(placement);

	$(".episode-list-item").each(function(){
		var item = $(this);
		myPlaylist.push({
			mp3: item.find(".episode-audio-link").attr("href"),
			title: item.find(".episode-list-title").text(),
			artist: author,
			// rating:4,
			// buy:'#',
			// price:'0.99',
			duration: item.data("duration"),
			cover: cover,
			description: item.find(".episode-list-description p").text()
		});
	});

	playerWrap.ttwMusicPlayer(myPlaylist, {
		autoPlay:false,
		description:"",
		jPlayer:{
			swfPath: siteVars('swf')
		}
	});

});
