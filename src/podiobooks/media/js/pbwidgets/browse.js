
	dojo.require("dojo.fx");
	dojo.require("dojo.fx.easing");
	
dojo.addOnLoad(function(){	
	
	var pbBrowseDict = {
		images:'/media/themes/pb2/images/',
		browseby:function(what){
			switch(what.toLowerCase()){
				case 'author':
					return {
						url:'contributors',
						name: function(a){
							return a.fields.display_name;
						}
					};
					break;
				case 'category':
					return {
						url: 'categories',
						name: function(a){
							return a.fields.name;
						}
					};
					break;
				default:
					return null;
					break;
			}
		}
	};
	
	dojo.place(dojo.create( "div", {
		'class': 'pb-browse-lists',
		'style':{
			'float':'left',
			'width:':'930px'
		}
	}),dojo.byId('pb-header-menubar'),'last');
	
	dojo.query('.browseby').forEach(
		function(node,index,arr){
			var ttl = dojo.attr(node,'title').toLowerCase().replace('browse by','');
			ttl = dojo.trim(ttl);
			dojo.attr(node, 'id', 'pb-browseby-' + ttl);
			dojo.place(
				dojo.create(
					'div',{
						'id':'pb-browseby-' + ttl + '-lists',
						'style':{
							'width':'100%',
							'display':'none',
							'float':'left'
						}
					}
				),
				dojo.query('.pb-browse-lists')[0]
			);
			
			dojo.xhrGet({
				url: '/json/' + pbBrowseDict.browseby(ttl).url,
				handleAs:"json",
				load:function(data){				
					var perCol = parseInt(data.length / 6);
					var addTo = data.length % 6;
					
					var cur = 0;
					for (var i = 0; i < 6; i++){
						var ulId = 'pb-browseby-' + ttl + '-list' + i;
						var ul = dojo.create(
							'ul',{
								'id':ulId, 
								'style':{
									'marginTop':'10px',
									'borderTop':'solid 1px #fff',
									'float':'left',
									'width':'145px',
									'padding':'5px'
								} 
							}
						);
						dojo.place(ul,'pb-browseby-' + ttl + '-lists');
						if (addTo > 0)
							perCol += 1;
							
						for (var j = cur; j < (cur + perCol); j++)
							dojo.place("<li style='margin:3px 0px 0px 0px'><a href='" + node + data[j].fields.slug + "'>" + pbBrowseDict.browseby(ttl).name(data[j]) + "</a></li>",'pb-browseby-' + ttl + '-list' + i);
							
						cur += perCol;
						
						if (addTo > 0)
							perCol--;
						addTo--;
					}	
				}
			});
			
			dojo.query(node).onclick(function(e){
				
				dojo.stopEvent(e);
				
				var lists = dojo.byId('pb-browseby-' + ttl + '-lists');
				if (dojo.hasClass(lists, 'pb-browseby-expanded')) 
				{
					dojo.removeClass(lists, 'pb-browseby-expanded');
					dojo.fx.wipeOut({
						onBegin: function(){dojo.style(node,'background','url(' + pbBrowseDict.images + 'arrow-right.png) center right no-repeat')},
						node: lists
					}).play();
				}
				else 
				{
					var show = dojo.fx.wipeIn({
						node: lists,
						onBegin: function(){
							dojo.style(node,'background','url(' + pbBrowseDict.images + 'arrow-down.png) center right no-repeat');
							dojo.addClass(lists, 'pb-browseby-expanded');
						},
						onEnd: function(){
							
						},
						easing: dojo.fx.easing.bounceOut,
						duration:800
					});
					
					var exp = dojo.query('.pb-browseby-expanded');
					if (exp.length > 0) {
						exp = exp[0];
						var hide = dojo.fx.wipeOut({
							onBegin: function(){
								dojo.query('.browseby').forEach(function(lnk){
									dojo.style(lnk, 'background', 'url(' + pbBrowseDict.images + 'arrow-right.png) center right no-repeat');
								});
							},
							node: exp,
							onEnd: function(){
								dojo.removeClass(exp, 'pb-browseby-expanded');
							}
						});
						
						dojo.fx.chain([hide, show]).play();
					}
					else
						show.play();
				}
			});
		}
	);	
});
