var telemetry = (function() {

    var queue = [];
    var _backendURL = '';
    var httpRequest = new XMLHttpRequest();

    var _isQueing = false;
	var _sessionURL;
	var _isSessionSet = false;

    var getTimestamp = function() {
        return new Date().toLocaleString();
    };

    var _makeRequest = function() {
        if(httpRequest.readyState === XMLHttpRequest.DONE) {
            if(httpRequest.status === 200) {
                queue = [];
            } else {
                console.log('Error processing request');
            }
        }
    };

    var transmitDataToBackend = function() {
        if(!httpRequest) {
            console.log('Could not create XMLHTTP instance');
            return false;
        }
        httpRequest.onreadystatechange = _makeRequest;
        httpRequest.open('POST', _backendURL);
        var data = {
            telemetry: queue
        };
        httpRequest.send(JSON.stringify(data));
    };

	var _sessionSet = function() {
		if(httpRequest.readyState === XMLHttpRequest.DONE) {
			if(httpRequest.status === 200) {
				_isSessionSet = true;
			}
		}
	};

	var _setSession = function() {
		if(!httpRequest) {
			console.log('Could not create XMLHTTP instance');
			return false;
		}
		httpRequest.onreadystatechange = _sessionSet;
		httpRequest.withCredentials = true;
		httpRequest.open('POST', _sessionURL);
		httpRequest.setRequestHeader('Access-Control-Allow-Origin', _sessionURL);
		httpRequest.send(null);
	};

    var handleEvent = function(evt) {
        // evt.preventDefault();
        event.stopPropagation();
        var os = navigator.platform;
        var userAgent = navigator.userAgent;
        var timestamp = getTimestamp();
        if(_isQueing) {
            if(queue.length < 10) {
                queue.push({
                    type: evt.type,
                    os: os,
                    userAgent: userAgent,
                    timestamp: timestamp,
                    element: evt.toElement.dataset.telemetryId,
                    location: window.location.pathname
                });
            } else {
                //Flush the queue
				if(_isSessionSet) {
					transmitDataToBackend();
				} else {
					var waitTillSessionSet = setInterval(function(){
						if(_isSessionSet) {
							clearInterval(waitTillSessionSet);
							transmitDataToBackend();
						}
					}, 500);
				}
            }
        } else {
            queue.push({
                type: evt.type,
                os: os,
                userAgent: userAgent,
                timestamp: timestamp,
                element: evt.toElement.dataset.telemetryId,
                location: window.location.pathname
            });
			if(_isSessionSet) {
				transmitDataToBackend();
			} else {
				var waitTillSessionSet = setInterval(function(){
					if(_isSessionSet) {
						clearInterval(waitTillSessionSet);
						transmitDataToBackend();
					}
				}, 500);
			}
        }
    };

    var handleScrollEvent = function(evt) {
        evt.stopPropagation();
        var os = navigator.platform;
        var userAgent = navigator.userAgent;
        var timestamp = getTimestamp();
        if(_isQueing) {
            if(queue.length < 10) {
                queue.push({
                    type: 'scrollend',
                    os: os,
                    userAgent: userAgent,
                    timestamp: timestamp,
                    element: evt.srcElement.dataset.telemetryId,
                    location: window.location.pathname
                });
            } else {
                //Flush the queue
				if(_isSessionSet) {
					transmitDataToBackend();
				} else {
					var waitTillSessionSet = setInterval(function(){
						if(_isSessionSet) {
							clearInterval(waitTillSessionSet);
							transmitDataToBackend();
						}
					}, 500);
				}
            }
        } else {
            queue.push({
                type: 'scrollend',
                os: os,
                userAgent: userAgent,
                timestamp: timestamp,
                element: evt.srcElement.dataset.telemetryId,
                location: window.location.pathname
            });
			if(_isSessionSet) {
				transmitDataToBackend();
			} else {
				var waitTillSessionSet = setInterval(function(){
					if(_isSessionSet) {
						clearInterval(waitTillSessionSet);
						transmitDataToBackend();
					}
				}, 500);
			}
        }
    };

    var bootstrapTelemetry = function(params) {
        if(params) {
            if(params.isQueueing && params.isQueueing === true) {
                _isQueing = true;
            }
            if(params.backendURL && typeof params.backendURL === 'string') {
                _backendURL = params.backendURL;
            } else {
                throw 'Backend URL not specified';
            }
            if(params.sessionURL && typeof params.sessionURL === 'string') {
                _sessionURL = params.sessionURL;
            } else {
                throw 'Session URL not specified';
            }
        } else {
            throw 'No Backend URL and Session URL specified';
        }
		// Manage Session
        _setSession();
        // Get all elements with telemetry attribute
        var telemetryElements = document.querySelectorAll('[data-telemetry-id]');
        if(telemetryElements.length === 0) {
            return;
        }
        // For element, attach an event handler
        telemetryElements.forEach(function(element) {
            // Don't attach the click event for <a/> tags which are not self referentials
            if(element.tagName === 'A' && !element.href.startsWith('#')) {
                return;
            }
            element.onclick = handleEvent;
            // if input element, attach a keypress event
            if(element.tagName === 'input') {
                element.keypress = handleEvent;
                element.onfocus = handleEvent;
                element.onblur = handleEvent;
            }
            element.onscroll = function(evt) {
                console.log('scrolling');
                if(element.attributes.timeout) {
                    clearTimeout(element.attributes.timeout);
                }
                element.attributes.timeout = setTimeout(function(){
                    console.log('scrolling stopped');
                    handleScrollEvent(evt);
                }, 250);
            };
        });

        // Handle DOM change events
        // Remove event handlers for removed DOM nodes
        // Add event handlers for added DOM nodes
        var observer = new MutationObserver(function(mutations){
            mutations.forEach(function(mutation) {
                var addedNodes = mutation.addedNodes;
                var removedNodes = mutation.removedNodes;

                addedNodes.forEach(function(node) {
                    if(node.nodeType == 3) {
                        return;
                    }
                    if(node.hasAttribute('data-telemetry-id')) {
                        node.onclick = handleEvent;
                        node.onscroll = function(evt) {
                            console.log('scrolling');
                            if(node.attributes.timeout) {
                                clearTimeout(node.attributes.timeout);
                            }
                            node.attributes.timeout = setTimeout(function(){
                                console.log('scrolling stopped');
                                handleScrollEvent(evt);
                            }, 250);
                        };
                        if(node.tagName === 'input') {
                            node.onkeypress = handleEvent;
                        }
                    }
                });

                removedNodes.forEach(function(node) {
                    if(node.hasAttribute('data-telemetry-id')) {
                        node.removeEventListener('click', handleEvent);
                        node.removeEventListener('keypress', handleEvent);
                    }
                });
            });
        });

        var observerConfig = {
        	attributes: true,
        	childList: true,
        	characterData: true,
            subtree: true
        };

        observer.observe(document.body, observerConfig);

        window.onbeforeunload = function(evt) {
            // form object
            var os = navigator.platform;
            var userAgent = navigator.userAgent;
            var timestamp = getTimestamp();
            var telemetryObject = {
                type: 'navigation',
                os: os,
                userAgent: userAgent,
                timestamp: timestamp,
                location: window.location.pathname,
                newLocation: document.activeElement.pathname,
                element: document.activeElement.attributes[0].value
            };
            // console.log(telemetryObject);
            queue.push(telemetryObject);
            if(_isSessionSet) {
				transmitDataToBackend();
			} else {
				var waitTillSessionSet = setInterval(function(){
					if(_isSessionSet) {
						clearInterval(waitTillSessionSet);
						transmitDataToBackend();
					}
				}, 500);
			}
        };

    };

    return {
        bootstrapTelemetry: bootstrapTelemetry
    };

})();
