webpackJsonp([25],{334:function(t,e,r){"use strict";function n(t){r(779)}Object.defineProperty(e,"__esModule",{value:!0});var o=r(647),i=r.n(o);for(var a in o)"default"!==a&&function(t){r.d(e,t,function(){return o[t]})}(a);var s=r(781),u=r(53),c=n,d=u(i.a,s.a,!1,c,"data-v-6dd2987f",null);e.default=d.exports},363:function(t,e,r){"use strict";function n(t){return"[object Array]"===j.call(t)}function o(t){return"[object ArrayBuffer]"===j.call(t)}function i(t){return"undefined"!=typeof FormData&&t instanceof FormData}function a(t){return"undefined"!=typeof ArrayBuffer&&ArrayBuffer.isView?ArrayBuffer.isView(t):t&&t.buffer&&t.buffer instanceof ArrayBuffer}function s(t){return"string"==typeof t}function u(t){return"number"==typeof t}function c(t){return void 0===t}function d(t){return null!==t&&"object"==typeof t}function p(t){return"[object Date]"===j.call(t)}function f(t){return"[object File]"===j.call(t)}function l(t){return"[object Blob]"===j.call(t)}function m(t){return"[object Function]"===j.call(t)}function h(t){return d(t)&&m(t.pipe)}function g(t){return"undefined"!=typeof URLSearchParams&&t instanceof URLSearchParams}function v(t){return t.replace(/^\s*/,"").replace(/\s*$/,"")}function b(){return("undefined"==typeof navigator||"ReactNative"!==navigator.product)&&("undefined"!=typeof window&&"undefined"!=typeof document)}function y(t,e){if(null!==t&&void 0!==t)if("object"!=typeof t&&(t=[t]),n(t))for(var r=0,o=t.length;r<o;r++)e.call(null,t[r],r,t);else for(var i in t)Object.prototype.hasOwnProperty.call(t,i)&&e.call(null,t[i],i,t)}function F(){function t(t,r){"object"==typeof e[r]&&"object"==typeof t?e[r]=F(e[r],t):e[r]=t}for(var e={},r=0,n=arguments.length;r<n;r++)y(arguments[r],t);return e}function _(t,e,r){return y(e,function(e,n){t[n]=r&&"function"==typeof e?G(e,r):e}),t}var G=r(367),w=r(376),j=Object.prototype.toString;t.exports={isArray:n,isArrayBuffer:o,isBuffer:w,isFormData:i,isArrayBufferView:a,isString:s,isNumber:u,isObject:d,isUndefined:c,isDate:p,isFile:f,isBlob:l,isFunction:m,isStream:h,isURLSearchParams:g,isStandardBrowserEnv:b,forEach:y,merge:F,extend:_,trim:v}},365:function(t,e,r){"use strict";(function(e){function n(t,e){!o.isUndefined(t)&&o.isUndefined(t["Content-Type"])&&(t["Content-Type"]=e)}var o=r(363),i=r(379),a={"Content-Type":"application/x-www-form-urlencoded"},s={adapter:function(){var t;return"undefined"!=typeof XMLHttpRequest?t=r(368):void 0!==e&&(t=r(368)),t}(),transformRequest:[function(t,e){return i(e,"Content-Type"),o.isFormData(t)||o.isArrayBuffer(t)||o.isBuffer(t)||o.isStream(t)||o.isFile(t)||o.isBlob(t)?t:o.isArrayBufferView(t)?t.buffer:o.isURLSearchParams(t)?(n(e,"application/x-www-form-urlencoded;charset=utf-8"),t.toString()):o.isObject(t)?(n(e,"application/json;charset=utf-8"),JSON.stringify(t)):t}],transformResponse:[function(t){if("string"==typeof t)try{t=JSON.parse(t)}catch(t){}return t}],timeout:0,xsrfCookieName:"XSRF-TOKEN",xsrfHeaderName:"X-XSRF-TOKEN",maxContentLength:-1,validateStatus:function(t){return t>=200&&t<300}};s.headers={common:{Accept:"application/json, text/plain, */*"}},o.forEach(["delete","get","head"],function(t){s.headers[t]={}}),o.forEach(["post","put","patch"],function(t){s.headers[t]=o.merge(a)}),t.exports=s}).call(e,r(378))},367:function(t,e,r){"use strict";t.exports=function(t,e){return function(){for(var r=new Array(arguments.length),n=0;n<r.length;n++)r[n]=arguments[n];return t.apply(e,r)}}},368:function(t,e,r){"use strict";var n=r(363),o=r(380),i=r(382),a=r(383),s=r(384),u=r(369);t.exports=function(t){return new Promise(function(e,c){var d=t.data,p=t.headers;n.isFormData(d)&&delete p["Content-Type"];var f=new XMLHttpRequest;if(t.auth){var l=t.auth.username||"",m=t.auth.password||"";p.Authorization="Basic "+btoa(l+":"+m)}if(f.open(t.method.toUpperCase(),i(t.url,t.params,t.paramsSerializer),!0),f.timeout=t.timeout,f.onreadystatechange=function(){if(f&&4===f.readyState&&(0!==f.status||f.responseURL&&0===f.responseURL.indexOf("file:"))){var r="getAllResponseHeaders"in f?a(f.getAllResponseHeaders()):null,n=t.responseType&&"text"!==t.responseType?f.response:f.responseText,i={data:n,status:f.status,statusText:f.statusText,headers:r,config:t,request:f};o(e,c,i),f=null}},f.onerror=function(){c(u("Network Error",t,null,f)),f=null},f.ontimeout=function(){c(u("timeout of "+t.timeout+"ms exceeded",t,"ECONNABORTED",f)),f=null},n.isStandardBrowserEnv()){var h=r(385),g=(t.withCredentials||s(t.url))&&t.xsrfCookieName?h.read(t.xsrfCookieName):void 0;g&&(p[t.xsrfHeaderName]=g)}if("setRequestHeader"in f&&n.forEach(p,function(t,e){void 0===d&&"content-type"===e.toLowerCase()?delete p[e]:f.setRequestHeader(e,t)}),t.withCredentials&&(f.withCredentials=!0),t.responseType)try{f.responseType=t.responseType}catch(e){if("json"!==t.responseType)throw e}"function"==typeof t.onDownloadProgress&&f.addEventListener("progress",t.onDownloadProgress),"function"==typeof t.onUploadProgress&&f.upload&&f.upload.addEventListener("progress",t.onUploadProgress),t.cancelToken&&t.cancelToken.promise.then(function(t){f&&(f.abort(),c(t),f=null)}),void 0===d&&(d=null),f.send(d)})}},369:function(t,e,r){"use strict";var n=r(381);t.exports=function(t,e,r,o,i){var a=new Error(t);return n(a,e,r,o,i)}},370:function(t,e,r){"use strict";t.exports=function(t){return!(!t||!t.__CANCEL__)}},371:function(t,e,r){"use strict";function n(t){this.message=t}n.prototype.toString=function(){return"Cancel"+(this.message?": "+this.message:"")},n.prototype.__CANCEL__=!0,t.exports=n},373:function(t,e,r){t.exports=r(375)},374:function(t,e,r){"use strict";Object.defineProperty(e,"__esModule",{value:!0}),e.globalCustom=e.testConnection=e.delDataBase=e.upDataBase=e.getDataBase=e.addDataBase=e.get_api_list=e.get_parameter=e.getLoginList=e.addLoginToken=e.getTimedTask=e.delApiGroup=e.updateApiGroup=e.addApiGroup=e.getApiGroupList=e.addApiDetail=e.getTestTenResult=e.getTestTenTime=e.getTestResultList=e.addEmailConfig=e.delEmailConfig=e.getEmailConfigDetail=e.getProjectMemberList=e.getProjectDynamicList=e.addHost=e.updateHost=e.enableHost=e.disableHost=e.delHost=e.getHost=e.getProjectDetail=e.addProject=e.updateProject=e.enableProject=e.disableProject=e.delProject=e.getProject=e.recordVisitor=e.requestLogin=e.dingLogin=e.dingConfig=e.test=void 0;var n=r(373),o=function(t){return t&&t.__esModule?t:{default:t}}(n),i=e.test="http://wxweapp-api-test2.shenlanbao.com";e.dingConfig=function(t){return o.default.get(i+"/api/user/dingConfig",t).then(function(t){return t.data})},e.dingLogin=function(t){return o.default.post(i+"/api/user/dingConfig",t).then(function(t){return t.data})},e.requestLogin=function(t){return o.default.post(i+"/api/user/login",t).then(function(t){return t.data})},e.recordVisitor=function(t){return o.default.post(i+"/api/user/VisitorRecord",t).then(function(t){return t.data})},e.getProject=function(t,e){return o.default.get(i+"/api/project/project_list",{params:e,headers:t}).then(function(t){return t.data})},e.delProject=function(t,e){return o.default.post(i+"/api/project/del_project",e,{headers:t}).then(function(t){return t.data})},e.disableProject=function(t,e){return o.default.post(i+"/api/project/disable_project",e,{headers:t}).then(function(t){return t.data})},e.enableProject=function(t,e){return o.default.post(i+"/api/project/enable_project",e,{headers:t}).then(function(t){return t.data})},e.updateProject=function(t,e){return o.default.post(i+"/api/project/update_project",e,{headers:t}).then(function(t){return t.data})},e.addProject=function(t,e){return o.default.post(i+"/api/project/add_project",e,{headers:t}).then(function(t){return t.data})},e.getProjectDetail=function(t,e){return o.default.get(i+"/api/title/project_info",{params:e,headers:t}).then(function(t){return t.data})},e.getHost=function(t,e){return o.default.get(i+"/api/global/host_total",{params:e,headers:t}).then(function(t){return t.data})},e.delHost=function(t,e){return o.default.post(i+"/api/global/del_host",e,{headers:t}).then(function(t){return t.data})},e.disableHost=function(t,e){return o.default.post(i+"/api/global/disable_host",e,{headers:t}).then(function(t){return t.data})},e.enableHost=function(t,e){return o.default.post(i+"/api/global/enable_host",e,{headers:t}).then(function(t){return t.data})},e.updateHost=function(t,e){return o.default.post(i+"/api/global/update_host",e,{headers:t}).then(function(t){return t.data})},e.addHost=function(t,e){return o.default.post(i+"/api/global/add_host",e,{headers:t}).then(function(t){return t.data})},e.getProjectDynamicList=function(t,e){return o.default.get(i+"/api/dynamic/dynamic",{params:e,headers:t}).then(function(t){return t.data})},e.getProjectMemberList=function(t,e){return o.default.get(i+"/api/member/project_member",{params:e,headers:t}).then(function(t){return t.data})},e.getEmailConfigDetail=function(t,e){return o.default.get(i+"/api/member/get_email",{params:e,headers:t}).then(function(t){return t.data})},e.delEmailConfig=function(t,e){return o.default.post(i+"/api/member/del_email",e,{headers:t}).then(function(t){return t.data})},e.addEmailConfig=function(t,e){return o.default.post(i+"/api/member/email_config",e,{headers:t}).then(function(t){return t.data})},e.getTestResultList=function(t,e){return o.default.get(i+"/api/report/auto_test_report",{params:e,headers:t}).then(function(t){return t.data})},e.getTestTenTime=function(t,e){return o.default.get(i+"/api/report/test_time",{params:e,headers:t}).then(function(t){return t.data})},e.getTestTenResult=function(t,e){return o.default.get(i+"/api/report/lately_ten",{params:e,headers:t}).then(function(t){return t.data})},e.addApiDetail=function(t,e){return o.default.post(i+"/api/api/add_api",e,{headers:t}).then(function(t){return t.data})},e.getApiGroupList=function(t,e){return o.default.get(i+"/api/api/group",{params:e,headers:t}).then(function(t){return t.data})},e.addApiGroup=function(t,e){return o.default.post(i+"/api/api/add_group",e,{headers:t}).then(function(t){return t.data})},e.updateApiGroup=function(t,e){return o.default.post(i+"/api/api/update_name_group",e,{headers:t}).then(function(t){return t.data})},e.delApiGroup=function(t,e){return o.default.post(i+"/api/api/del_group",e,{headers:t}).then(function(t){return t.data})},e.getTimedTask=function(t,e){return o.default.get(i+"/api/task/timing_list",{params:e,headers:t}).then(function(t){return t})},e.addLoginToken=function(t,e){return o.default.post(i+"/api/token/LoginToken",e,{headers:t}).then(function(t){return t.data})},e.getLoginList=function(t,e){return o.default.get(i+"/api/token/listToken",{params:e,headers:t}).then(function(t){return t.data})},e.get_parameter=function(t,e){return o.default.get(i+"/api/data/get_parameter",{params:e,headers:t}).then(function(t){return t.data})},e.get_api_list=function(t,e){return o.default.get(i+"/api/automation/api_list",{params:e,headers:t}).then(function(t){return t.data})},e.addDataBase=function(t,e){return o.default.post(i+"/api/database/addData",e,{headers:t}).then(function(t){return t.data})},e.getDataBase=function(t,e){return o.default.get(i+"/api/database/getData",{params:e,headers:t}).then(function(t){return t.data})},e.upDataBase=function(t,e){return o.default.post(i+"/api/database/updateData",e,{headers:t}).then(function(t){return t.data})},e.delDataBase=function(t,e){return o.default.post(i+"/api/database/delDataBase",e,{headers:t}).then(function(t){return t.data})},e.testConnection=function(t,e){return o.default.get(i+"/api/database/testConnection",{params:e,headers:t}).then(function(t){return t.data})},e.globalCustom=function(t,e){return o.default.get(i+"/api/custom/GetPublicVariable",{params:e,headers:t}).then(function(t){return t.data})}},375:function(t,e,r){"use strict";function n(t){var e=new a(t),r=i(a.prototype.request,e);return o.extend(r,a.prototype,e),o.extend(r,e),r}var o=r(363),i=r(367),a=r(377),s=r(365),u=n(s);u.Axios=a,u.create=function(t){return n(o.merge(s,t))},u.Cancel=r(371),u.CancelToken=r(391),u.isCancel=r(370),u.all=function(t){return Promise.all(t)},u.spread=r(392),t.exports=u,t.exports.default=u},376:function(t,e){/*!
 * Determine if an object is a Buffer
 *
 * @author   Feross Aboukhadijeh <https://feross.org>
 * @license  MIT
 */
t.exports=function(t){return null!=t&&null!=t.constructor&&"function"==typeof t.constructor.isBuffer&&t.constructor.isBuffer(t)}},377:function(t,e,r){"use strict";function n(t){this.defaults=t,this.interceptors={request:new a,response:new a}}var o=r(365),i=r(363),a=r(386),s=r(387);n.prototype.request=function(t){"string"==typeof t&&(t=i.merge({url:arguments[0]},arguments[1])),t=i.merge(o,{method:"get"},this.defaults,t),t.method=t.method.toLowerCase();var e=[s,void 0],r=Promise.resolve(t);for(this.interceptors.request.forEach(function(t){e.unshift(t.fulfilled,t.rejected)}),this.interceptors.response.forEach(function(t){e.push(t.fulfilled,t.rejected)});e.length;)r=r.then(e.shift(),e.shift());return r},i.forEach(["delete","get","head","options"],function(t){n.prototype[t]=function(e,r){return this.request(i.merge(r||{},{method:t,url:e}))}}),i.forEach(["post","put","patch"],function(t){n.prototype[t]=function(e,r,n){return this.request(i.merge(n||{},{method:t,url:e,data:r}))}}),t.exports=n},378:function(t,e){function r(){throw new Error("setTimeout has not been defined")}function n(){throw new Error("clearTimeout has not been defined")}function o(t){if(d===setTimeout)return setTimeout(t,0);if((d===r||!d)&&setTimeout)return d=setTimeout,setTimeout(t,0);try{return d(t,0)}catch(e){try{return d.call(null,t,0)}catch(e){return d.call(this,t,0)}}}function i(t){if(p===clearTimeout)return clearTimeout(t);if((p===n||!p)&&clearTimeout)return p=clearTimeout,clearTimeout(t);try{return p(t)}catch(e){try{return p.call(null,t)}catch(e){return p.call(this,t)}}}function a(){h&&l&&(h=!1,l.length?m=l.concat(m):g=-1,m.length&&s())}function s(){if(!h){var t=o(a);h=!0;for(var e=m.length;e;){for(l=m,m=[];++g<e;)l&&l[g].run();g=-1,e=m.length}l=null,h=!1,i(t)}}function u(t,e){this.fun=t,this.array=e}function c(){}var d,p,f=t.exports={};!function(){try{d="function"==typeof setTimeout?setTimeout:r}catch(t){d=r}try{p="function"==typeof clearTimeout?clearTimeout:n}catch(t){p=n}}();var l,m=[],h=!1,g=-1;f.nextTick=function(t){var e=new Array(arguments.length-1);if(arguments.length>1)for(var r=1;r<arguments.length;r++)e[r-1]=arguments[r];m.push(new u(t,e)),1!==m.length||h||o(s)},u.prototype.run=function(){this.fun.apply(null,this.array)},f.title="browser",f.browser=!0,f.env={},f.argv=[],f.version="",f.versions={},f.on=c,f.addListener=c,f.once=c,f.off=c,f.removeListener=c,f.removeAllListeners=c,f.emit=c,f.prependListener=c,f.prependOnceListener=c,f.listeners=function(t){return[]},f.binding=function(t){throw new Error("process.binding is not supported")},f.cwd=function(){return"/"},f.chdir=function(t){throw new Error("process.chdir is not supported")},f.umask=function(){return 0}},379:function(t,e,r){"use strict";var n=r(363);t.exports=function(t,e){n.forEach(t,function(r,n){n!==e&&n.toUpperCase()===e.toUpperCase()&&(t[e]=r,delete t[n])})}},380:function(t,e,r){"use strict";var n=r(369);t.exports=function(t,e,r){var o=r.config.validateStatus;r.status&&o&&!o(r.status)?e(n("Request failed with status code "+r.status,r.config,null,r.request,r)):t(r)}},381:function(t,e,r){"use strict";t.exports=function(t,e,r,n,o){return t.config=e,r&&(t.code=r),t.request=n,t.response=o,t}},382:function(t,e,r){"use strict";function n(t){return encodeURIComponent(t).replace(/%40/gi,"@").replace(/%3A/gi,":").replace(/%24/g,"$").replace(/%2C/gi,",").replace(/%20/g,"+").replace(/%5B/gi,"[").replace(/%5D/gi,"]")}var o=r(363);t.exports=function(t,e,r){if(!e)return t;var i;if(r)i=r(e);else if(o.isURLSearchParams(e))i=e.toString();else{var a=[];o.forEach(e,function(t,e){null!==t&&void 0!==t&&(o.isArray(t)?e+="[]":t=[t],o.forEach(t,function(t){o.isDate(t)?t=t.toISOString():o.isObject(t)&&(t=JSON.stringify(t)),a.push(n(e)+"="+n(t))}))}),i=a.join("&")}return i&&(t+=(-1===t.indexOf("?")?"?":"&")+i),t}},383:function(t,e,r){"use strict";var n=r(363),o=["age","authorization","content-length","content-type","etag","expires","from","host","if-modified-since","if-unmodified-since","last-modified","location","max-forwards","proxy-authorization","referer","retry-after","user-agent"];t.exports=function(t){var e,r,i,a={};return t?(n.forEach(t.split("\n"),function(t){if(i=t.indexOf(":"),e=n.trim(t.substr(0,i)).toLowerCase(),r=n.trim(t.substr(i+1)),e){if(a[e]&&o.indexOf(e)>=0)return;a[e]="set-cookie"===e?(a[e]?a[e]:[]).concat([r]):a[e]?a[e]+", "+r:r}}),a):a}},384:function(t,e,r){"use strict";var n=r(363);t.exports=n.isStandardBrowserEnv()?function(){function t(t){var e=t;return r&&(o.setAttribute("href",e),e=o.href),o.setAttribute("href",e),{href:o.href,protocol:o.protocol?o.protocol.replace(/:$/,""):"",host:o.host,search:o.search?o.search.replace(/^\?/,""):"",hash:o.hash?o.hash.replace(/^#/,""):"",hostname:o.hostname,port:o.port,pathname:"/"===o.pathname.charAt(0)?o.pathname:"/"+o.pathname}}var e,r=/(msie|trident)/i.test(navigator.userAgent),o=document.createElement("a");return e=t(window.location.href),function(r){var o=n.isString(r)?t(r):r;return o.protocol===e.protocol&&o.host===e.host}}():function(){return function(){return!0}}()},385:function(t,e,r){"use strict";var n=r(363);t.exports=n.isStandardBrowserEnv()?function(){return{write:function(t,e,r,o,i,a){var s=[];s.push(t+"="+encodeURIComponent(e)),n.isNumber(r)&&s.push("expires="+new Date(r).toGMTString()),n.isString(o)&&s.push("path="+o),n.isString(i)&&s.push("domain="+i),!0===a&&s.push("secure"),document.cookie=s.join("; ")},read:function(t){var e=document.cookie.match(new RegExp("(^|;\\s*)("+t+")=([^;]*)"));return e?decodeURIComponent(e[3]):null},remove:function(t){this.write(t,"",Date.now()-864e5)}}}():function(){return{write:function(){},read:function(){return null},remove:function(){}}}()},386:function(t,e,r){"use strict";function n(){this.handlers=[]}var o=r(363);n.prototype.use=function(t,e){return this.handlers.push({fulfilled:t,rejected:e}),this.handlers.length-1},n.prototype.eject=function(t){this.handlers[t]&&(this.handlers[t]=null)},n.prototype.forEach=function(t){o.forEach(this.handlers,function(e){null!==e&&t(e)})},t.exports=n},387:function(t,e,r){"use strict";function n(t){t.cancelToken&&t.cancelToken.throwIfRequested()}var o=r(363),i=r(388),a=r(370),s=r(365),u=r(389),c=r(390);t.exports=function(t){return n(t),t.baseURL&&!u(t.url)&&(t.url=c(t.baseURL,t.url)),t.headers=t.headers||{},t.data=i(t.data,t.headers,t.transformRequest),t.headers=o.merge(t.headers.common||{},t.headers[t.method]||{},t.headers||{}),o.forEach(["delete","get","head","post","put","patch","common"],function(e){delete t.headers[e]}),(t.adapter||s.adapter)(t).then(function(e){return n(t),e.data=i(e.data,e.headers,t.transformResponse),e},function(e){return a(e)||(n(t),e&&e.response&&(e.response.data=i(e.response.data,e.response.headers,t.transformResponse))),Promise.reject(e)})}},388:function(t,e,r){"use strict";var n=r(363);t.exports=function(t,e,r){return n.forEach(r,function(r){t=r(t,e)}),t}},389:function(t,e,r){"use strict";t.exports=function(t){return/^([a-z][a-z\d\+\-\.]*:)?\/\//i.test(t)}},390:function(t,e,r){"use strict";t.exports=function(t,e){return e?t.replace(/\/+$/,"")+"/"+e.replace(/^\/+/,""):t}},391:function(t,e,r){"use strict";function n(t){if("function"!=typeof t)throw new TypeError("executor must be a function.");var e;this.promise=new Promise(function(t){e=t});var r=this;t(function(t){r.reason||(r.reason=new o(t),e(r.reason))})}var o=r(371);n.prototype.throwIfRequested=function(){if(this.reason)throw this.reason},n.source=function(){var t;return{token:new n(function(e){t=e}),cancel:t}},t.exports=n},392:function(t,e,r){"use strict";t.exports=function(t){return function(e){return t.apply(null,e)}}},647:function(t,e,r){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var n=r(374);e.default={data:function(){return{project:"",groupData:[],addGroupFormVisible:!1,addGroupLoading:!1,addFormVisible:!1,addGroupFormRules:{firstgroup:[{required:!0,message:"请输入子分组名称",trigger:"blur"}]},addGroupForm:{firstgroup:""},editFirstGroupFormVisible:!1,editFirstGroupLoading:!1,editFirstFormVisible:!1,editFirstGroupFormRules:{secondFirstGroup:[{required:!0,message:"请输入分组名称",trigger:"blur"}]},editFirstGroupForm:{firstgroup:"",second_id:""},filters:{name:""},api:[],total:0,page:1,listLoading:!1,sels:[],apiView:!0}},methods:{init:function(){this.addGroupForm.firstgroup=""},getApiGroup:function(){var t=this,e={project_id:this.$route.params.project_id},r={"Content-Type":"application/json",Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};(0,n.getApiGroupList)(r,e).then(function(e){var r=e.msg,n=e.code,o=e.data;"999999"===n?(t.groupData=o,t.init()):t.$message.error({message:r,center:!0})})},handleAddGroup:function(){this.addGroupFormVisible=!0},handleEditFirstGroup:function(t,e){this.editFirstGroupFormVisible=!0,this.editFirstGroupForm.second_id=t,this.editFirstGroupForm.secondFirstGroup=e},addGroupSubmit:function(){var t=this;this.$refs.addGroupForm.validate(function(e){if(e){var r=t;t.$confirm("确认提交吗？","提示",{}).then(function(){r.addGroupLoading=!0;var e={project_id:Number(t.$route.params.project_id),name:r.addGroupForm.firstgroup},o={"Content-Type":"application/json",Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};(0,n.addApiGroup)(o,e).then(function(t){var e=t.msg,n=t.code;t.data;r.addGroupLoading=!1,"999999"===n?(r.$message({message:"添加成功",center:!0,type:"success"}),r.$refs.addGroupForm.resetFields(),r.addGroupFormVisible=!1,r.getApiGroup(),r.init()):"999997"===n?r.$message.error({message:e,center:!0}):(r.$message.error({message:e,center:!0}),r.$refs.addGroupForm.resetFields(),r.addGroupFormVisible=!1,r.getApiGroup(),r.init())})})}})},editFirstGroupSubmit:function(){var t=this;this.$refs.editFirstGroupForm.validate(function(e){if(e){var r=t;t.$confirm("确认提交吗？","提示",{}).then(function(){r.editFirstGroupLoading=!0;var e={project_id:Number(t.$route.params.project_id),name:r.editFirstGroupForm.secondFirstGroup,id:r.editFirstGroupForm.second_id},o={"Content-Type":"application/json",Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};(0,n.updateApiGroup)(o,e).then(function(t){var e=t.msg,n=t.code;t.data;r.editFirstGroupLoading=!1,"999999"===n?(r.$message({message:"修改成功",center:!0,type:"success"}),r.$refs.editFirstGroupForm.resetFields(),r.editFirstGroupFormVisible=!1,r.getApiGroup(),r.init()):"999997"===n?r.$message.error({message:e,center:!0}):(r.$message.error({message:e,center:!0}),r.$refs.editFirstGroupForm.resetFields(),r.editFirstGroupFormVisible=!1,r.getApiGroup(),r.init())})})}})},handleDelFirst:function(t){var e=this;this.$confirm("确认删除该记录吗?","提示",{type:"warning"}).then(function(){var r=e,o={id:Number(t),project_id:Number(e.$route.params.project_id)},i={"Content-Type":"application/json",Authorization:"Token "+JSON.parse(sessionStorage.getItem("token"))};(0,n.delApiGroup)(i,o).then(function(t){var e=t.msg,n=t.code;t.data;"999999"===n?r.$message({message:"删除成功",center:!0,type:"success"}):r.$message.error({message:e,center:!0}),r.getApiGroup()})})}},mounted:function(){this.getApiGroup(),this.project=this.$route.params.project_id}}},779:function(t,e,r){var n=r(780);"string"==typeof n&&(n=[[t.i,n,""]]),n.locals&&(t.exports=n.locals);r(326)("52e4a48c",n,!0,{})},780:function(t,e,r){e=t.exports=r(325)(!1),e.push([t.i,".api-title[data-v-6dd2987f]{padding:15px;margin:0;text-align:center;border-radius:5px;font-size:15px;color:#f0f8ff;background-color:#20a0ff;font-family:PingFang SC}.group .editGroup[data-v-6dd2987f]{float:right}.row-title[data-v-6dd2987f]{margin:35px}.addGroup[data-v-6dd2987f]{margin-top:0;margin-bottom:10px;border-radius:25px}",""])},781:function(t,e,r){"use strict";var n=function(){var t=this,e=t.$createElement,r=t._self._c||e;return r("section",[r("el-row",{staticClass:"row-title",attrs:{span:24}},[r("el-col",{attrs:{span:4}},[r("el-button",{staticClass:"addGroup",on:{click:t.handleAddGroup}},[t._v("新增分组")]),t._v(" "),r("router-link",{staticStyle:{"text-decoration":"none",color:"aliceblue"},attrs:{to:{name:"快速测试",params:{project_id:this.$route.params.project_id}}}},[r("el-button",{staticClass:"addGroup"},[t._v("快速测试")])],1),t._v(" "),r("div",{staticClass:"api-title"},[r("strong",[t._v("接口分组")])]),t._v(" "),r("div",{staticClass:"api-title",staticStyle:{cursor:"pointer"}},[r("router-link",{staticStyle:{"text-decoration":"none",color:"aliceblue"},attrs:{to:{name:"接口列表",params:{project_id:this.$route.params.project_id}}}},[t._v("\n                    所有接口\n                ")])],1),t._v(" "),r("aside",[r("el-menu",{staticClass:"el-menu-vertical-demo",attrs:{"default-active":"2","active-text-color":"rgb(32, 160, 255)","unique-opened":!0}},[t._l(t.groupData,function(e,n){return[r("router-link",{staticStyle:{"text-decoration":"none"},attrs:{to:{name:"分组接口列表",params:{project_id:t.project,firstGroup:e.id}}}},[r("el-menu-item",{key:e.id,staticClass:"group",attrs:{index:n+""}},[r("template",{slot:"title"},[t._v(t._s(e.name)+"\n                                    "),r("el-dropdown",{staticClass:"editGroup",staticStyle:{"margin-right":"10%"},attrs:{trigger:"hover"}},[r("i",{staticClass:"el-icon-more"}),t._v(" "),r("el-dropdown-menu",{attrs:{slot:"dropdown"},slot:"dropdown"},[r("el-dropdown-item",{nativeOn:{click:function(r){return t.handleDelFirst(e.id)}}},[t._v("删除")]),t._v(" "),r("el-dropdown-item",{nativeOn:{click:function(r){return t.handleEditFirstGroup(e.id,e.name)}}},[t._v("修改")])],1)],1)],1)],2)],1)]})],2)],1)],1),t._v(" "),r("el-dialog",{staticStyle:{width:"60%",left:"20%"},attrs:{title:"新增分组",visible:t.addGroupFormVisible,"close-on-click-modal":!1},on:{"update:visible":function(e){t.addGroupFormVisible=e}}},[r("el-form",{ref:"addGroupForm",attrs:{model:t.addGroupForm,"label-width":"80px",rules:t.addGroupFormRules}},[r("el-form-item",{attrs:{label:"分组名称",prop:"firstgroup"}},[r("el-input",{staticStyle:{width:"90%"},attrs:{"auto-complete":"off"},model:{value:t.addGroupForm.firstgroup,callback:function(e){t.$set(t.addGroupForm,"firstgroup","string"==typeof e?e.trim():e)},expression:"addGroupForm.firstgroup"}})],1)],1),t._v(" "),r("div",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[r("el-button",{nativeOn:{click:function(e){t.addGroupFormVisible=!1}}},[t._v("取消")]),t._v(" "),r("el-button",{attrs:{type:"primary",loading:t.addGroupLoading},nativeOn:{click:function(e){return t.addGroupSubmit(e)}}},[t._v("提交")])],1)],1),t._v(" "),r("el-dialog",{staticStyle:{width:"60%",left:"20%"},attrs:{title:"编辑分组",visible:t.editFirstGroupFormVisible,"close-on-click-modal":!1},on:{"update:visible":function(e){t.editFirstGroupFormVisible=e}}},[r("el-form",{ref:"editFirstGroupForm",attrs:{model:t.editFirstGroupForm,"label-width":"80px",rules:t.editFirstGroupFormRules}},[r("el-form-item",{attrs:{label:"分组名称",prop:"secondFirstGroup"}},[r("el-input",{attrs:{"auto-complete":"off"},model:{value:t.editFirstGroupForm.secondFirstGroup,callback:function(e){t.$set(t.editFirstGroupForm,"secondFirstGroup","string"==typeof e?e.trim():e)},expression:"editFirstGroupForm.secondFirstGroup"}})],1)],1),t._v(" "),r("div",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[r("el-button",{nativeOn:{click:function(e){t.editFirstGroupFormVisible=!1}}},[t._v("取消")]),t._v(" "),r("el-button",{attrs:{type:"primary",loading:t.editFirstGroupLoading},nativeOn:{click:function(e){return t.editFirstGroupSubmit(e)}}},[t._v("提交")])],1)],1),t._v(" "),r("el-col",{attrs:{span:20}},[r("div",{staticStyle:{"margin-left":"10px","margin-right":"20px"}},[r("router-view")],1)])],1)],1)},o=[],i={render:n,staticRenderFns:o};e.a=i}});