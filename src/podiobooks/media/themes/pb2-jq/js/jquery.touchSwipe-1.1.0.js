(function($) 
{
	$.fn.swipe = function(options) 
	{
		if (!this) return false;
		
		// Default thresholds & swipe functions
		var defaults = {
			fingers 		: 1,								// int - The number of fingers to trigger the swipe, 1 or 2. Default is 1.
			threshold 		: 75,								// int - The number of pixels that the user must move their finger by before it is considered a swipe. Default is 75.
			
			swipe 			: null,		// Function - A catch all handler that is triggered for all swipe directions. Accepts 2 arguments, the original event object and the direction of the swipe : "left", "right", "up", "down".
			swipeLeft		: null,		// Function - A handler that is triggered for "left" swipes. Accepts 3 arguments, the original event object, the direction of the swipe : "left", "right", "up", "down" and the distance of the swipe.
			swipeRight		: null,		// Function - A handler that is triggered for "right" swipes. Accepts 3 arguments, the original event object, the direction of the swipe : "left", "right", "up", "down" and the distance of the swipe.
			swipeUp			: null,		// Function - A handler that is triggered for "up" swipes. Accepts 3 arguments, the original event object, the direction of the swipe : "left", "right", "up", "down" and the distance of the swipe.
			swipeDown		: null,		// Function - A handler that is triggered for "down" swipes. Accepts 3 arguments, the original event object, the direction of the swipe : "left", "right", "up", "down" and the distance of the swipe.
			swipeStatus		: null,		// Function - A handler triggered for every phase of the swipe. Handler is passed 4 arguments: event : The original event object, phase:The current swipe face, either "start, "move, "end or "cancel. direction : The swipe direction, either "up, "down, "left " or "right.distance : The distance of the swipe.
			
			triggerOnTouchEnd : true,	// Boolean, if true, the swipe events are triggered when the touch end event is received (user releases finger).  If false, it will be triggered on reaching the threshold, and then cancel the touch event automatically.
			allowPageScroll : "auto" 	/* How the browser handles page scrolls when the user is swiping on a touchSwipe object. 
											"auto" : all undefined swipes will cause the page to scroll in that direction.
 											"none" : the page will not scroll when user swipes.
 											"horizontal" : will force page to scroll on horizontal swipes.
 											"vertical" : will force page to scroll on vertical swipes.
										*/
		};
		
		
		
		var LEFT = "left";
		var RIGHT = "right";
		var UP = "up";
		var DOWN = "down";
		var NONE = "none";
		var HORIZONTAL = "horizontal";
		var VERTICAL = "vertical";
		var AUTO = "auto";
		
		var phase="start";
		
		var PHASE_START="start";
		var PHASE_MOVE="move";
		var PHASE_END="end";
		var PHASE_CANCEL="cancel";
		
		
		
		if (options.allowPageScroll==undefined && (options.swipe!=undefined || options.swipeStatus!=undefined))
			options.allowPageScroll=NONE;
		
		var options = $.extend(defaults, options);
		
		if (options.debug)
			options.swipe = function(event, direction )	{ console.log("swiped " + direction );	};
		
		
		
		return this.each(function() 
		{
			var triggerElementID = null; 	// this variable is used to identity the triggering element
			var fingerCount = 0;			// the current number of fingers being used.	
			
			//track mouse points / delta
			var start={x:0, y:0};
			var end={x:0, y:0};
			var delta={x:0, y:0};
			
			/**
			* Event handler for a touch start event. 
			* Stops the default click event from triggering and stores where we touched
			*/
			function touchStart(event) 
			{
				phase = PHASE_START;
				// disable the standard ability to select the touched object
		//		event.preventDefault();
				// get the total number of fingers touching the screen
				fingerCount = event.touches.length;
				
				// check the number of fingers is what we are looking for
				if ( fingerCount == defaults.fingers ) 
				{
					// get the coordinates of the touch
					start.x = event.touches[0].pageX;
					start.y = event.touches[0].pageY;
					
					if (defaults.swipeStatus)
						triggerHandler(event, phase);
				} 
				else 
				{
					//touch with more/less than the fingers we are looking for
					touchCancel(event);
				}
			}

			/**
			* Event handler for a touch move event. 
			* If we change fingers during move, then cancel the event
			*/
			function touchMove(event) 
			{
				if (phase == PHASE_END || phase == PHASE_CANCEL)
					return;
					
				phase = PHASE_MOVE;
				
				end.x = event.touches[0].pageX;
				end.y = event.touches[0].pageY;
					
				direction = caluculateDirection();
				
				//Check if we need to prevent default evnet (page scroll) or not
				validateDefaultEvent(event, direction);
		
				if ( event.touches.length == defaults.fingers ) 
				{
					var distance = null;
					
					if (defaults.swipeStatus)
					{
						distance = caluculateDistance();
						triggerHandler(event, phase, direction, distance);
					}
					
					//If we trigger whilst dragging, not on touch end, then calculate now...
					if (!defaults.triggerOnTouchEnd)
					{
						 
						if (!distance)
							distance = caluculateDistance();
							
						// if the user swiped more than the minimum length, perform the appropriate action
						if ( distance >= defaults.threshold ) 
						{
							phase = PHASE_END;
							triggerHandler(event, phase, direction, distance);
							touchCancel(event); // reset the variables
						}
					}
				} 
				else 
				{
					phase = PHASE_CANCEL;
					triggerHandler(event, phase); 
					touchCancel(event);
				}
			}
			
			/**
			* Event handler for a touch end event. 
			* Calculate the direction and trigger events
			*/
			function touchEnd(event) 
			{
				
				event.preventDefault();
				
				if (defaults.triggerOnTouchEnd)
				{
					phase = PHASE_END;
					// check to see if more than one finger was used and that there is an ending coordinate
					if ( fingerCount == defaults.fingers && end.x != 0 ) 
					{
						var distance = caluculateDistance(); 
						direction = caluculateDirection();
						// if the user swiped more than the minimum length, perform the appropriate action
						if ( distance >= defaults.threshold ) 
						{
							triggerHandler(event, phase, direction, distance);
							touchCancel(event); // reset the variables
						} 
						else 
						{
							phase = PHASE_CANCEL;
							triggerHandler(event, phase, direction, distance); 
							touchCancel(event);
						}	
					} 
					else 
					{
						phase = PHASE_CANCEL;
						triggerHandler(event, phase); 
						touchCancel(event);
					}
				}
				else if (phase == PHASE_MOVE)
				{
					phase = PHASE_CANCEL;
					triggerHandler(event, phase); 
					touchCancel(event);
				}
				
				
			}
			
			/**
			* Event handler for a touch cancel event. 
			* Clears current vars
			*/
			function touchCancel(event) 
			{
				// reset the variables back to default values
				fingerCount = 0;
				
				start.x = 0;
				start.y = 0;
				end.x = 0;
				end.y = 0;
				delta.x = 0;
				delta.y = 0;
			}
			
			
			
			
			
			/**
			* Calcualte the length / distance of the swipe
			*/
			function caluculateDistance()
			{
				return Math.round(Math.sqrt(Math.pow(end.x - start.x,2) + Math.pow(end.y - start.y,2)));
			}
			
			/**
			* Calcualte the angle of the swipe
			*/
			function caluculateAngle() 
			{
				var X = start.x-end.x;
				var Y = end.y-start.y;
				var r = Math.atan2(Y,X); //radians
				var angle = Math.round(r*180/Math.PI); //degrees
				
				//ensure value is positive
				if (angle < 0) 
					angle = 360 - Math.abs(angle);
					
				return angle;
			}
			
			
			/**
			* Calcualte the direction of the swipe
			* This will also call caluculateAngle to get the latest angle of swipe
			*/
			function caluculateDirection() 
			{
				var angle = caluculateAngle();
				
				if ( (angle <= 45) && (angle >= 0) ) 
					return LEFT;
				
				else if ( (angle <= 360) && (angle >= 315) )
					return LEFT;
				
				else if ( (angle >= 135) && (angle <= 225) )
					return RIGHT;
				
				else if ( (angle > 45) && (angle < 135) )
					return DOWN;
				
				else
					return UP;
			}
			
			

			
			
			/**
			* Trigger the relevant event handler
			* The handlers are passed the original event, the element that was swiped, and in the case of the catch all handler, the direction that was swiped, "left", "right", "up", or "down"
			*/
			function triggerHandler(event, phase, direction, distance) 
			{
				//update status
				if (defaults.swipeStatus)
					defaults.swipeStatus(event, phase, direction || null, distance || 0);
				
				
				if (phase == PHASE_END)
				{
					//trigger catch all event handler
					if (defaults.swipe)
						defaults.swipe(event, direction, distance);
					
					//trigger direction specific event handlers	
					switch(direction)
					{
						case LEFT :
							if (defaults.swipeLeft)
								defaults.swipeLeft(event, direction, distance);
							break;
						
						case RIGHT :
							if (defaults.swipeRight)
								defaults.swipeRight(event, direction, distance);
							break;

						case UP :
							if (defaults.swipeUp)
								defaults.swipeUp(event, direction, distance);
							break;
						
						case DOWN :	
							if (defaults.swipeDown)
								defaults.swipeDown(event, direction, distance);
							break;
					}
				}
			}
			
			
			/**
			 * Checks direction of the swipe and the value allowPageScroll to see if we should allow or prevent the default behaviour from occurring.
			 * This will essentially allow page scrolling or not when the user is swiping on a touchSwipe object.
			 */
			function validateDefaultEvent(event, direction)
			{
				if( defaults.allowPageScroll==NONE )
				{
					event.preventDefault();
				}
				else 
				{
					var auto=defaults.allowPageScroll==AUTO;
					
					switch(direction)
					{
						case LEFT :
							if ( (defaults.swipeLeft && auto) || (!auto && defaults.allowPageScroll!=HORIZONTAL))
								event.preventDefault();
							break;
						
						case RIGHT :
							if ( (defaults.swipeRight && auto) || (!auto && defaults.allowPageScroll!=HORIZONTAL))
								event.preventDefault();
							break;

						case UP :
							if ( (defaults.swipeUp && auto) || (!auto && defaults.allowPageScroll!=VERTICAL))
								event.preventDefault();
							break;
						
						case DOWN :	
							if ( (defaults.swipeDown && auto) || (!auto && defaults.allowPageScroll!=VERTICAL))
								event.preventDefault();
							break;
					}
				}
				
			}
			
			// Add gestures to all swipable areas
			this.addEventListener("touchstart", touchStart, false);
			this.addEventListener("touchmove", touchMove, false);
			this.addEventListener("touchend", touchEnd, false);
			this.addEventListener("touchcancel", touchCancel, false);
				
		});
	};
	
	
	
	
})(jQuery);