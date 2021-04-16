console.log("loading webview hooker ....");

if (Java.available) {
    Java.perform(() => {
        const webview = Java.use("android.webkit.WebView");
        const Arrays = Java.use("java.util.Arrays");
        const webviewclient = Java.use("android.webkit.WebViewClient");

        webview.loadUrl.overload("java.lang.String").implementation = function(url) {
            const ret = this.loadUrl(url);
            var websettings = this.mProvider.value.getSettings();
            var status = {};
            status["JavaScriptEnabled"] = websettings.getJavaScriptEnabled();
            status["AllowContentAccess"] = websettings.getAllowContentAccess();
            status["AllowFileAccess"] = websettings.getAllowFileAccess();
            status["AllowFileAccessFromFileURLs"] = websettings.getAllowFileAccessFromFileURLs();
            status["AllowUniversalAccessFromFileURLs"] = websettings.getAllowUniversalAccessFromFileURLs();
            status["UserAgent"] = websettings.getUserAgentString();

            console.log("Now Loading URL : "+url);

            console.log("webview instance status : "+JSON.stringify(status,null,"\t"));
            return ret;
        }

        webview.loadUrl.overload('java.lang.String', 'java.util.Map').implementation = function (url,map) {
            const ret = this.loadUrl(url,map);
            //Arrays.toString(map.entrySet().toArray())
            const additionHttpHeaders = Arrays.toString(map.entrySet().toArray());
            var websettings = this.mProvider.value.getSettings()
            var status = {};
            status["JavaScriptEnabled"] = websettings.getJavaScriptEnabled();
            status["AllowContentAccess"] = websettings.getAllowContentAccess();
            status["AllowFileAccess"] = websettings.getAllowFileAccess();
            status["AllowFileAccessFromFileURLs"] = websettings.getAllowFileAccessFromFileURLs();
            status["AllowUniversalAccessFromFileURLs"] = websettings.getAllowUniversalAccessFromFileURLs();
            status["UserAgent"] = websettings.getUserAgentString();
            status["HttpHeaders"] = additionHttpHeaders;

            console.log("Now Loading URL : "+url);
            console.log("class instance : "+cls);

            return ret;
        }

        webview.addJavascriptInterface.implementation = function(obj,name) {
            const ret = this.addJavascriptInterface(obj,name);
            const cls_name = obj.getClass().getName();
            var interfaces = new Array();
            var details = {};
            try {
                const cls = Java.use(cls_name);
                const method = cls.class.getDeclaredMethods();
                method.forEach((s) => {
                    interfaces.push(s.toString());
                })
            }catch (error) {
                interfaces.push("failed to get method, pls confirm manually");
            }
            details["class_name"] = cls_name;
            details["JsBridge_name"] = name;
            details["interfaces"] = interfaces
            
            console.log("catch Javascript Interface : "+JSON.stringify(details,null,"\t"));
            
            return ret;
        }

        webviewclient.shouldOverrideUrlLoading.overload("android.webkit.WebView","android.webkit.WebResourceRequest").implementation = function(webview,request) {
            const fromUrl = webview.getUrl();
            const targetUrl = request.getUrl().toString();
            const requestMap = request.getRequestHeaders();
            const requestHeaders = null
            try{
                requestHeaders = Arrays.toString(requestMap.entrySet().toArray());
            } catch(error) {

            } 

            var details = {};
            details["from"] = fromUrl;
            details["to"] = targetUrl;
            details["headers"] = requestHeaders;

            console.log('catch overloading url : '+JSON.stringify(details,null,"\t"));

            const ret = this.shouldOverrideUrlLoading(webview,request);
            return ret;
        }
    })
}