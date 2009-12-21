dojo.provide("pbwidgets.book_shelf.BookShelf");

dojo.require("dijit.layout.StackContainer");
dojo.require("dijit.layout.ContentPane");
dojo.declare( "pbwidgets.book_shelf.BookShelf",
	[dijit.layout.StackContainer],
{
	_setupChild: function(/*dijit._Widget*/ child){
		this.inherited(arguments);

		// Start the nodes with 0 opacity so the fade in works the first time
		dojo.style(child.domNode,"opacity",0);
	},
	
	_showChild: function(/*dijit._Widget*/ page){
		
		dojo.fadeIn({ 
        	node: page.domNode,
			duration:500
		}).play();
		
		this.inherited(arguments);
	},

	_hideChild: function(/*dijit._Widget*/ page){
		
		dojo.fadeOut({ 
        	node: page.domNode,
			duration:500
		}).play();
		
		this.inherited(arguments);
	},
} );