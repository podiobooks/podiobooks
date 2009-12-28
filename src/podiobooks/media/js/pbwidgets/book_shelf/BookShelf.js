dojo.provide("pbwidgets.book_shelf.BookShelf");
dojo.provide("pbwidgets.book_shelf._StackButton");

dojo.require("dijit._Widget");
dojo.require("dijit._Templated");
dojo.require("dijit._Contained");
dojo.require("dijit.layout.StackContainer");
dojo.require("dojo.fx.easing");

dojo.declare("pbwidgets.book_shelf.BookShelf", [dijit.layout.StackContainer, dijit._Templated], {
    // duration: Integer
    //	used for Fade and Slide RadioGroup's, the duration to run the transition animation. does not affect anything
    //	in default RadioGroup
    duration: 750,
    
    // templateString: String
    //	the template for our container
    templateString: '<div dojoAttachPoint="containerNode"></div>',
    
    startup: function(){
        this.inherited(arguments);
        this._size = dojo.coords(this.containerNode);
    },
    
    _setupChild: function(/* dijit._Widget */child){
        dojo.style(child.domNode, "position", "absolute");
        child.domNode.style.display = "none";
    },
    
    _transition: function(/*dijit._Widget*/newWidget, /*dijit._Widget*/ oldWidget){
        // summary: called when StackContainer receives a selectChild call, used to transition the panes.
        this._showChild(newWidget);
        if (oldWidget) {
            this._hideChild(oldWidget);
        }
        // Size the new widget, in case this is the first time it's being shown,
        // or I have been resized since the last time it was shown.
        // page must be visible for resizing to work
        if (this.doLayout && newWidget.resize) {
            newWidget.resize(this._containerContentBox || this._contentBox);
        }
    },
    
    _showChild: function(/*dijit._Widget*/page){
        // summary: show the selected child widget
        var children = this.getChildren();
        page.isFirstChild = (page == children[0]);
        page.isLastChild = (page == children[children.length - 1]);
        page.selected = true;
        
        page.domNode.style.display = "";
        
        if (page._onShow) {
            page._onShow(); // trigger load in ContentPane
        }
        else 
            if (page.onShow) {
                page.onShow();
            }
    },
    
    _hideChild: function(/*dijit._Widget*/page){
        // summary: hide the specified child widget
        page.selected = false;
        page.domNode.style.display = "none";
        if (page.onHide) {
            page.onHide();
        }
    }
    
});

dojo.declare("pbwidgets.book_shelf.BookShelfFade", pbwidgets.book_shelf.BookShelf, {
    // summary: An extension on a stock RadioGroup, that fades the panes.
    
    _hideChild: function(page){
        // summary: hide the specified child widget
        dojo.fadeOut({
            node: page.domNode,
            duration: this.duration,
            onEnd: dojo.hitch(this, "inherited", arguments, arguments)
        }).play();
    },
    
    _showChild: function(page){
        // summary: show the specified child widget
        this.inherited(arguments);
        dojo.style(page.domNode, "opacity", 0);
        dojo.fadeIn({
            node: page.domNode,
            duration: this.duration
        }).play();
    }
});

dojo.declare("pbwidgets.book_shelf.BookShelfSlide", pbwidgets.book_shelf.BookShelf, {
    // summary: A Sliding Radio Group
    // description: 
    //		An extension on a stock RadioGroup widget, sliding the pane
    //		into view from being hidden. The entry direction is randomized 
    //		on each view
    //		
    
    // easing: Function
    //	A hook to override the default easing of the pane slides.
    easing: "dojo.fx.easing.backOut",
    
    // zTop: Integer
    //		A z-index to apply to the incoming pane
    zTop: 99,
    
    constructor: function(){
        if (dojo.isString(this.easing)) {
            this.easing = dojo.getObject(this.easing);
        }
    },
    
    _positionChild: function(page){
        // summary: set the child out of view immediately after being hidden
        
        if (!this._size) {
            return;
        } // FIXME: is there a real "size" floating around always?
        // there should be a contest: obfuscate this function as best you can. 
        var rA = true, rB = true;
        switch (page.slideFrom) {
            case "bottom":
                rB = !rB;
                break;
            case "right":
                rA = !rA;
                rB = !rB;
                break;
            case "top":
                break;
            case "left":
                rA = !rA;
                break;
            default:
                rA = Math.round(Math.random());
                rB = Math.round(Math.random());
                break;
        }
        var prop = rA ? "top" : "left", val = (rB ? "-" : "") + (this._size[rA ? "h" : "w"] + 20) + "px";
        
        dojo.style(page.domNode, prop, val);
        
    },
    
    _showChild: function(page){
        // summary: Slide in the selected child widget
        
        var children = this.getChildren();
        page.isFirstChild = (page == children[0]);
        page.isLastChild = (page == children[children.length - 1]);
        page.selected = true;
        
        dojo.style(page.domNode, {
            zIndex: this.zTop,
            display: ""
        })
        
        if (this._anim && this._anim.status() == "playing") {
            this._anim.gotoPercent(100, true);
        }
        
        this._anim = dojo.animateProperty({
            node: page.domNode,
            properties: {
                left: 0,
                top: 0
            },
            duration: this.duration,
            easing: this.easing,
            onEnd: dojo.hitch(page, function(){
                if (this.onShow) {
                    this.onShow();
                }
                if (this._onShow) {
                    this._onShow();
                }
            }),
            beforeBegin: dojo.hitch(this, "_positionChild", page)
        });
        this._anim.play();
    },
    
    _hideChild: function(page){
        // summary: reset the position of the hidden pane out of sight
        
        page.selected = false;
        dojo.style(page.domNode, {
            zIndex: this.zTop - 1,
            display: "none"
        });
        if (page.onHide) {
            page.onHide();
        }
        
    }
    
});

dojo.extend(dijit._Widget, {
    // slideFrom: String
    //		A parameter needed by RadioGroupSlide only. An optional paramter to force
    //		the ContentPane to slide in from a set direction. Defaults
    //		to "random", or specify one of "top", "left", "right", "bottom"
    //		to slideFrom top, left, right, or bottom.
    slideFrom: "random"
});

dojo.declare("pbwidgets.book_shelf._StackButton", dijit.form.ToggleButton, {
    // summary:
    //		Internal widget used by StackContainer.
    // description:
    //		The button-like or tab-like object you click to select or delete a page
    // tags:
    //		private
    
    // Override _FormWidget.tabIndex.
    // StackContainer buttons are not in the tab order by default.
    // Probably we should be calling this.startupKeyNavChildren() instead.
    tabIndex: "-1",
    
    postCreate: function(/*Event*/evt){
        dijit.setWaiRole((this.focusNode || this.domNode), "tab");
        this.inherited(arguments);
    },
	
	_clicked: function(/*Event*/ evt){
		//this.attr('checked', !this.checked);
	},
    
    onClick: function(/*Event*/evt){
        // summary:
        //		This is for TabContainer where the tabs are <span> rather than button,
        //		so need to set focus explicitly (on some browsers)
        //		Note that you shouldn't override this method, but you can connect to it.
        dijit.focus(this.focusNode);
        
        // ... now let StackController catch the event and tell me what to do
    },
    
    onClickCloseButton: function(/*Event*/evt){
        // summary:
        //		StackContainer connects to this function; if your widget contains a close button
        //		then clicking it should call this function.
        //		Note that you shouldn't override this method, but you can connect to it.
        evt.stopPropagation();
    }
});

