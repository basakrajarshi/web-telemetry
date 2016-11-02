(function() {

    var stack = [];

    var getDOMPath = function(domPath) {
        // traverse the array in reverse
        // for(var i = domPath.length - 1; i >= 0; i--) {
        // }
        return '';
    };

    var getTimestamp = function() {
        return Date();
    };

    var handleEvent = function(evt) {
        var os = navigator.platform;
        var userAgent = navigator.userAgent;
        var timestamp = getTimestamp();
        var domPath = getDOMPath(evt.path);
        if(stack.length < 10) {
            stack.push({
                type: evt.type,
                os: os,
                userAgent: userAgent,
                timestamp: timestamp,
                domPath: domPath
            });
        } else {
            //Flush the stack
            stack = [];
        }
        console.log(evt);
    };

    var bootstrapTelemetry = function() {
        // Get all elements with telemetry attribute
        var telemetryElements = document.querySelectorAll('[data-telemetry]');
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
                    node.onclick = handleEvent;
                    if(node.tagName === 'input') {
                        node.onkeypress = handleEvent;
                    }
                });

                removedNodes.forEach(function(node) {
                    node.onclick = null;
                    node.keypress = null;
                });
            });
        });

        var observerConfig = {
        	attributes: true,
        	childList: true,
        	characterData: true
        };

        observer.observe(document.body, observerConfig);
    };

    bootstrapTelemetry();

    // document.onclick = handleEvent;
    // document.onkeypress = handleEvent;

})();
