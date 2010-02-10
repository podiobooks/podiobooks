dojo.provide("pbwidgets.book_desc.BookDesc");

dojo.require("dijit._Widget");
dojo.require("dijit._Templated");
dojo.require("dojo.io.script");
dojo.require("dijit.Tooltip");

dojo.declare(
"pbwidgets.book_desc.BookDesc",
[dijit._Widget, dijit._Templated],
{
    templatePath: dojo.moduleUrl("pbwidgets", "book_desc/BookDesc.html"),
	   
    //titleID Property is used to figure out which book we need to pull up (default to a known working title)
    descUrl: '/title/summary/99/',
	
    postCreate: function(){
       // Don't do anything because all the magic happens in _showDescription
    },
	
   _showDescription: function() {
   		// Through JavaScript closures, this variable allows us to reference the 
       // surrounding object from within the get(...) methods.
       var hookedTo = this;
	   
	   dojo.xhrGet({
	        // The following URL must match that used to test the server.
	        url: this.descUrl,
	        handleAs: "text",
	  
	        timeout: 5000, // Time in milliseconds
	        // The LOAD function will be called on a successful response.
	        load: function(response, ioArgs){
			    questionTooltipHtml = response;
			    dijit.showTooltip(
			    	questionTooltipHtml,
			        hookedTo.domNode
			    );
	            return response;
	        },
	        
	        // The ERROR function will be called in an error case.
	        error: function(response, ioArgs){
	            return response;
	        }
	    });
      
   },  // End of _showDescription

   _hideTip: function() {
   		dijit.hideTooltip(this.domNode);
   }

});
