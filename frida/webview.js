console.log("loading webview hooker ....");

if (Java.available) {
    Java.perform(() => {
        const webview = Java.use("android.webkit.WebView");
        //const webview = Java.use("com.miui.webkit_api.WebView");
        const Arrays = Java.use("java.util.Arrays");
        const Map = Java.use("java.util.HashMap");
        const JavascriptInterface = Java.use("android.webkit.JavascriptInterface");
        
        try {
            const QbSdk = Java.use("com.tencent.smtt.sdk.QbSdk");

            QbSdk.getIsSysWebViewForcedByOuter.implementation = function() {
                this.forceSysWebView();
                console.log("Forcing USE System Webview");
                
                var ret = this.getIsSysWebViewForcedByOuter();
                return ret;
            }
        } catch(error) {
            console.warn(error)
        }

        webview.setWebViewClient.implementation = function(client) {
            var ret = this.setWebViewClient(client);
            const name = client.getClass().getName().toString();
            //console.log("class : "+name);

            client.shouldOverrideUrlLoading.overload("android.webkit.WebView","android.webkit.WebResourceRequest").implementation = function(webview,request) {
            //client.shouldOverrideUrlLoading.overload('com.miui.webkit_api.WebView', 'com.miui.webkit_api.WebResourceRequest').implementation = function(webview,request) {
                const cls_name = this.getClass().getName().toString();
                const fromUrl = webview.getUrl();
                const targetUrl = request.getUrl().toString();
                const requestMap = request.getRequestHeaders();
                var requestHeaders = []
                try  {
                    const entries = requestMap.entrySet().iterator();
                while(entries.hasNext()) {
                    var entry = entries.next();
                    requestHeaders.push(entry.toString())
                }
                } catch(error) {
                    console.error(error)
                }
                var details = {};
                details['class_name'] = cls_name;
                details["from"] = fromUrl;
                details["to"] = targetUrl;
                details["headers"] = requestHeaders;
    
                console.log('catch overloading url : '+JSON.stringify(details,null,"\t"));
    
                const ret = this.shouldOverrideUrlLoading(webview,request);
                return ret;
            }
            return ret
        }

        webview.loadUrl.overload("java.lang.String").implementation = function(url) {
            const ret = this.loadUrl(url);
            var websettings = this.getSettings();
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
            var additionHttpHeaders = [];
            const entries = map.entrySet().iterator();
            while(entries.hasNext()) {
                var entry = entries.next();
                additionHttpHeaders.push(entry.toString());
            } 
            var websettings = this.getSettings()
            var status = {};
            status["JavaScriptEnabled"] = websettings.getJavaScriptEnabled();
            status["AllowContentAccess"] = websettings.getAllowContentAccess();
            status["AllowFileAccess"] = websettings.getAllowFileAccess();
            status["AllowFileAccessFromFileURLs"] = websettings.getAllowFileAccessFromFileURLs();
            status["AllowUniversalAccessFromFileURLs"] = websettings.getAllowUniversalAccessFromFileURLs();
            status["UserAgent"] = websettings.getUserAgentString();
            status["HttpHeaders"] = additionHttpHeaders;

            console.log("Now Loading URL : "+url);
            console.log("webview instance status : "+JSON.stringify(status,null,"\t"));

            return ret;
        }

        webview.addJavascriptInterface.implementation = function(obj,name) {
            const ret = this.addJavascriptInterface(obj,name);
            const cls_name = obj.getClass().getName();
            var interfaces = new Array();
            var details = {};
            try {
                // const cls = Java.use(cls_name);
                const method = obj.getClass().getDeclaredMethods();
                // method.forEach((s) => {
                //     var met = s.toString();
                //     met = met.replace(cls_name+".","")
                //     if(met.indexOf("$") < 0) {
                //         interfaces.push(met);
                //     }
                // })
                method.forEach((s) => {
                    if (s.isAnnotationPresent(JavascriptInterface.class)) {
                        var method_name = s.toString();
                        method_name = method_name.replace(cls_name+".","");
                        interfaces.push(method_name);
                    }
                })
            }catch (error) {
                console.log(error);
                interfaces.push("failed to get method, pls confirm manually");
            }
            details["class_name"] = cls_name;
            details["JsBridge_name"] = name;
            details["interfaces"] = interfaces
            
            console.log("catch Javascript Interface : "+JSON.stringify(details,null,"\t"));
            
            return ret;
        }
    })
}