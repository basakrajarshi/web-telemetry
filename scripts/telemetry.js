var telemetry = (function() {

    var queue = [];
    var _backendURL = '';
    var httpRequest = new XMLHttpRequest();

    var setBackendURL = function(url) {
        _backendURL = url;
    }

    var getTimestamp = function() {
        return new Date().toLocaleString();
    };

    var _makeRequest = function() {
        if(httpRequest.readyState === XMLHttpRequest.DONE) {
            if(httpRequest.status === 200) {
                queue = [];
            }
        } else {
            console.log('Error processing request');
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
            telemetry: queue;
        };
        httpRequest.send(JSON.stringify(data));
    };

    var handleEvent = function(evt) {
        var os = navigator.platform;
        var userAgent = navigator.userAgent;
        var timestamp = getTimestamp();
        if(queue.length < 10) {
            queue.push({
                type: evt.type,
                os: os,
                userAgent: userAgent,
                timestamp: timestamp,
                element: evt.toElement.dataset.telemetryId
            });
        } else {
            //Flush the queue
            transmitDataToBackend();
        }
        console.log(evt);
    };

    var bootstrapTelemetry = function() {
        // Get all elements with telemetry attribute
        var telemetryElements = document.querySelectorAll('[data-telemetry-id]');
        if(telemetryElements.length === 0) {
            return;
        }
        // For element, attach an event handler
        telemetryElements.forEach(function(element) {
            element.onclick = handleEvent;
            // if input element, attach a keypress event
            if(element.tagName === 'input') {
                element.keypress = handleEvent;
            }
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
    };

    bootstrapTelemetry();

    return {
        setBackendURL: setBackendURL
    };

})();
