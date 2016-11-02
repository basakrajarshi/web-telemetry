(function() {

    var stack = [];

    var getDOMPath = function(domPath) {
        // traverse the array in reverse
        for(var i = domPath.length - 1; i >= 0; i--) {
        }
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
    };

    document.onclick = handleEvent;
    document.onkeypress = handleEvent;

})();
