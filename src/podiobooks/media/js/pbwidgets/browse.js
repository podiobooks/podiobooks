dojo.require("dojo.fx");
dojo.require("dojo.fx.easing");
	
dojo.addOnLoad(function(){	
	
	var pbBrowseDict = {
		images:'/media/themes/pb2/images/',
		incol:9,	// Actually 1 more than the value here
		cols:6,
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
							'marginTop': '10px',
							'borderTop': 'solid 1px #fff',
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
				load: function(data){
					
					var whatsLeft = data.length;
					var cur = 0;
					var pg = 0;
					var currentList = 0;
					
					// while there are entries left, make pages
					while (whatsLeft > 0) {
						
						// make first page visible
						var disp;
						if (pg == 0)
							 disp = 'block';
						else
							disp = 'none';
						
						// pace the page
						dojo.place(
							dojo.create('div',{
								'id':'pb-browseby-' + ttl + '-lists-page' + pg,
								'class':'pb-browseby-' + ttl + '-lists-page',
								'style': {
									'float':'left',
									'display':disp
								}
							}),'pb-browseby-' + ttl + '-lists'
						);
						
						var perCol;
						if (whatsLeft / pbBrowseDict.cols > pbBrowseDict.incol) 
							perCol = pbBrowseDict.incol;
						else 
							perCol = parseInt(whatsLeft / pbBrowseDict.cols);
						
						var addTo = data.length % pbBrowseDict.cols;
						
						for (var i = currentList; i < currentList + pbBrowseDict.cols; i++) {
							
							var ulId = 'pb-browseby-' + ttl + '-list' + i;
							var ul = dojo.create('ul', {
								'id': ulId,
								'style': {
									'float': 'left',
									'width': '145px',
									'padding': '5px'
								}
							});
							
							dojo.place(ul, 'pb-browseby-' + ttl + '-lists-page' + pg);
							
							if (addTo > 0) 
								perCol += 1;
							
							for (var j = cur; j < (cur + perCol); j++) {
								dojo.place("<li style='margin:3px 0px 0px 0px'><a href='" + node + data[j].fields.slug + "'>" + pbBrowseDict.browseby(ttl).name(data[j]) + "</a></li>", 'pb-browseby-' + ttl + '-list' + i);
								whatsLeft--;
							}
							cur += perCol;
							
							
							if (addTo > 0) 
								perCol--;
								
							addTo--;
							
						}
						currentList += pbBrowseDict.cols;
						pg++;
					}
					
					var pages = dojo.query('.pb-browseby-' + ttl + '-lists-page').length;
					if (pages > 1){
						dojo.place(
							dojo.create('div',{
								'class':'pb-browseby-lists-pagers',
								'innerHTML':"<p><a class='pb-browseby-lists-pager' id='pb-browseby-" + ttl + "-lists-pager-prev' href='#'>Prev</a> | <a class='pb-browseby-lists-pager' id='pb-browseby-" + ttl + "-lists-pager-next' href='#'>Next</a></p>",
								'style':{
									//'border':'solid',
									'textAlign':'right'
								}
							}),'pb-browseby-' + ttl + '-lists','first'
						);
						
						dojo.query('.pb-browseby-lists-pager').forEach(
							function(aNode){
								dojo.query(aNode).onclick(function(ev){
									dojo.stopEvent(ev);
									var myArr = dojo.attr(aNode,'id').split('-');
									var forward
									
									if (myArr[myArr.length-1].toLowerCase() == 'next')
										forward = true;
									else
										forward = false;
									
									if (forward)
									{
										var curPg;
										var nextPg;
										dojo.query('.pb-browseby-' + ttl + '-lists-page').forEach(
											function(pgNode){
												if (curPg && !nextPg)
													nextPg = pgNode;
												
												if (dojo.style(pgNode,'display') != 'none')
													curPg = pgNode;
											}
										);
										if (nextPg) {
											dojo.style(curPg, 'display', 'none');
											dojo.style(nextPg, 'display', 'block');
											
										}
									}
									else{
										var curPg;
										var last;
										var lastPg;
										dojo.query('.pb-browseby-' + ttl + '-lists-page').forEach(
											function(pgNode){												
												if (dojo.style(pgNode, 'display') != 'none') {
													curPg = pgNode;
													lastPg = last;
												}
												else 
													last = pgNode;	
											}
										);
										if (lastPg) {
											dojo.style(curPg, 'display', 'none');
											dojo.style(lastPg, 'display', 'block');
										}
									}
									listPagerCheckAndHide(ttl);
								});
							}
						);
												
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
				listPagerCheckAndHide(ttl);
			});
		}
	);	
});

function listPagerCheckAndHide(ttl){
	dojo.query('.pb-browseby-' + ttl + '-lists-page').forEach(function(node,index,arr){
		if (dojo.style(node,'display') != 'none'){
			
			//alert("pb-browseby-" + ttl + "-lists-pager-prev");
			
			if (index == 0)				
				dojo.style(dojo.byId("pb-browseby-" + ttl + "-lists-pager-prev"),'visibility','hidden');
			else if (index == (arr.length-1))
				dojo.style(dojo.byId("pb-browseby-" + ttl + "-lists-pager-next"),'visibility','hidden');
			else{
				dojo.style(dojo.byId("pb-browseby-" + ttl + "-lists-pager-prev"),'visibility','visible');
				dojo.style(dojo.byId("pb-browseby-" + ttl + "-lists-pager-next"),'visibility','visible');
			}
				
		}
	});
}
