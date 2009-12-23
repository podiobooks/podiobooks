dojo.provide("pbwidgets.book_shelf.BookShelf");

dojo.require("dijit.layout.StackContainer");
dojo.require("dijit.layout.ContentPane");
dojo.declare( "pbwidgets.book_shelf.BookShelf",
	[dijit.layout.StackContainer],
{
	_showChild: function(/*dijit._Widget*/ page){
		
		this.inherited(arguments);
		
		dojo.style(page.domNode,"opacity",0);
		
		dojo.fadeIn({ 
	        node: page.domNode,
			duration:500,
		}).play();
	},
} );
