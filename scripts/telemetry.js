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
		httpRequest.open('POST', _sessionURL);
        httpRequest.withCredentials = true;
		httpRequest.setRequestHeader('Access-Control-Allow-Origin', _sessionURL);
		httpRequest.send(null);
	};

    var handleEvent = function(evt) {
        // evt.preventDefault();
        event.stopPropagation();
        var os = navigator.platform;
        var userAgent = navigator.userAgent;
        var timestamp = getTimestamp();
        // If the element has it's own data-telemetry-id, use it
        if(evt.toElement.hasAttribute('data-telemetry-id')) {
            element = evt.toElement.dataset.telemetryId;
        } else {
            // Find the closest parent which has a data-telemetry-id
            // This element would cause the event
            element = evt.toElement.closest('[data-telemetry-id]').attributes['data-telemetry-id'].value;
        }

        var data = {
            type: evt.type,
            os: os,
            userAgent: userAgent,
            timestamp: timestamp,
            element: element,
            location: window.location.pathname
        };

        _transmitData(data);

    };

    var handleScrollEvent = function(evt) {
        evt.stopPropagation();
        var os = navigator.platform;
        var userAgent = navigator.userAgent;
        var timestamp = getTimestamp();
        var element = null;
        // If the element has it's own data-telemetry-id, use it
        if(evt.srcElement.hasAttribute('data-telemetry-id')) {
            element = evt.srcElement.dataset.telemetryId;
        } else {
            // Find the closest parent which has a data-telemetry-id
            // This element would cause the event
            element = evt.toElement.closest('[data-telemetry-id]').attributes['data-telemetry-id'].value;
        }

        var data = {
            type: 'scrollend',
            os: os,
            userAgent: userAgent,
            timestamp: timestamp,
            element: element,
            location: window.location.pathname
        };

        _transmitData(data);

    };

    var _transmitData = function(data) {
        if(_isQueing) {
            if(queue.length < 10) {
                queue.push(data);
            } else {
                _transmitIfSessionIsSet();
            }
        } else {
            queue.push(data);
            _transmitIfSessionIsSet();
        }
    };

    var _transmitIfSessionIsSet = function() {
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

    var handleErrors = function(message, source, lineNo, colNo, error) {
        var os = navigator.platform;
        var userAgent = navigator.userAgent;
        var timestamp = getTimestamp();
        var element = source;

        var data = {
            type: 'error',
            os: os,
            userAgent: userAgent,
            element: element,
            lineNo: lineNo,
            timestamp: timestamp,
            location: window.location.pathname,
            errorMessage: error.toString()
        };

        _transmitData(data);

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
        window.onerror = handleErrors;
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
                    if(node.nodeType === 1 && node.hasAttribute('data-telemetry-id')) {
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
                    if(node.nodeType === 1 && node.hasAttribute('data-telemetry-id')) {
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
            _transmitIfSessionIsSet();
        };

    };

    return {
        bootstrapTelemetry: bootstrapTelemetry
    };

})();
