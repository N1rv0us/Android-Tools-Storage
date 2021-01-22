console.log("running script...")

if (Java.available) {
    Java.perform(function() {
        var webviewclient = Java.use("android.webkit.WebViewClient")
        var webview = Java.use("android.webkit.WebView")

        function stacktrace() {
            var thread = Java.use('java.lang.Thread');
            var instance = thread.$new();
            var stack = instance.currentThread().getStackTrace();
            var at = "";
        
            for (var i = 0;i < stack.length ; i++) {
                at += stack[i].toString()+"\n";
            }
        
            return at;
        }

        webviewclient.shouldOverrideUrlLoading.overload('android.webkit.WebView','android.webkit.WebResourceRequest').implementation = function(webview,request) {
            var ret = this.shouldOverrideUrlLoading(webview,request)
            console.log("Overload URL : "+request.getUrl().toString())
            return ret
        }

        webview.addJavascriptInterface.implementation = function(obj,name) {
            var ret = this.addJavascriptInterface(obj,name)
            console.log("Catch Javascript Interface: ")
            console.log("|___load class name : "+obj.getClass().getName())
            console.log("|___JSBridge name : "+name)
            return ret
        }

        webview.loadUrl.overload("java.lang.String").implementation = function(target) {
            var ret = this.loadUrl(target)
            console.log("Loading URL : "+target)
            var stack = stacktrace()
            console.warn(stack)
            return ret
        }
    })
}
