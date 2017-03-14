var telemetry = (function() {

    var _backendURL = '';
    var _backendWebSocketURL = '';
    var httpRequest = new XMLHttpRequest();
    var _fallback = false;
	var _sessionURL;
	var _isSessionSet = false;
    var _ws = null;
    var _captureKeys = false;
    var _debug = false;

    var _getWebSocketUrl = function(urlParams) {
        var protocol = 'wss';
        var port = '8080';
        if(urlParams.protocol) {
            protocol = urlParams.protocol;
        }
        if(urlParams.port) {
            port = urlParams.port
        }
        return _formURL(protocol, port, urlParams);
    };

    var _getHTTPURL = function(urlParams) {
        var protocol = 'http';
        var port = '8080';
        if(urlParams.protocol) {
            protocol = urlParams.protocol;
        }
        if(urlParams.port) {
            port = urlParams.port
        }
        return _formURL(protocol, port, urlParams);
    };

    var _formURL = function(protocol, port, urlParams) {

        if(!urlParams.host) {
            throw 'No Host specified';
        }
        if(!urlParams.prefix) {
            throw 'No Session URL specified';
        }
        return `${protocol}://${urlParams.host}:${port}${urlParams.prefix}`;
    }

    var getTimestamp = function() {
        return new Date().toLocaleString();
    };

    var _makeRequest = function() {
        if(httpRequest.readyState === XMLHttpRequest.DONE) {
            if(httpRequest.status !== 200) {
                console.log('Error processing request');
            }
        }
    };

    var sendTelemetryEvent = function(data) {
        if(!_ws) {
            // create a websocket connection
            _ws = new WebSocket(_backendWebSocketURL);
            _ws.onopen = function() {
                _ws.send(JSON.stringify(data));
            }
            if(_debug) {
                _ws.onmessage = function(evt) {
                    console.log(evt.data);
                }
            }
        } else {
            _ws.send(JSON.stringify(data));
        }
    };

    var transmitDataToBackend = function(data) {
        if(!httpRequest) {
            console.log('Could not create XMLHTTP instance');
            return false;
        }
        httpRequest.onreadystatechange = _makeRequest;
        httpRequest.open('POST', _backendURL);
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
		httpRequest.open('GET', _sessionURL);
        httpRequest.withCredentials = true;
		httpRequest.setRequestHeader('Access-Control-Allow-Origin', window.location.origin);
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

        if(evt.type === 'keypress' && _captureKeys) {
            data.telemetryItem.keyCode = evt.keyCode;
        }

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
        var transmit;
        if(_fallback) {
            transmit = transmitDataToBackend;
        } else {
            transmit = sendTelemetryEvent;
        }
        if(_isSessionSet) {
            transmit(data);
        } else {
            var waitTillSessionSet = setInterval(function(){
                if(_isSessionSet) {
                    clearInterval(waitTillSessionSet);
                    transmit(data);
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
            if(params.sessionURL && typeof params.sessionURL === 'object') {
                _sessionURL = _getHTTPURL(params.sessionURL);
            } else {
                throw 'Session URL not specified';
            }
            if(params.captureKeys) {
                _captureKeys = true;
            }
            if(params.debug) {
                _debug = true;
            }
            if(window.WebSocket) {
                // Websocket supported
                if(params.backendWebSocketURL && typeof params.backendWebSocketURL === 'object') {
                    _backendWebSocketURL = _getWebSocketUrl(params.backendWebSocketURL);
                } else {
                    throw 'Web Socket handler URL not specified';
                }
            } else {
                // No support for websockets
                // Fallback to AJAX
                _fallback = true;
                if(params.backendURL && typeof params.backendURL === 'object') {
                    _backendURL = _getHTTPURL(params.backendURL);
                } else {
                    throw 'No Backend URL specified';
                }
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
                if(element.attributes.timeout) {
                    clearTimeout(element.attributes.timeout);
                }
                element.attributes.timeout = setTimeout(function(){
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
                            if(node.attributes.timeout) {
                                clearTimeout(node.attributes.timeout);
                            }
                            node.attributes.timeout = setTimeout(function(){
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
            _transmitData(telemetryObject);
            _deleteSession();
        };

    };

    var deleteSession = function() {
        if(!httpRequest) {
            console.log('Could not create XMLHttpRequest');
            return false;
        }
        httpRequest.onreadystatechange = _makeRequest;
        httpRequest.open('DELETE', _sessionURL);
        httpRequest.send();
    };

    return {
        bootstrapTelemetry: bootstrapTelemetry
    };

})();
