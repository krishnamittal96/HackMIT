chrome.contextMenus.create({title: "Add %s to beaker", 
                             contexts:["selection"], 
                              onclick: function(info, tab){ 
                               $.ajax({
                                    type: "POST",
                                    url: "http://40.121.54.11:80/generate/graphs",
                                    data: info.selectionText,
                                    success: function(resultData) {
                                        resultData = JSON.parse(resultData);
                                        console.log(resultData);
                                        chrome.tabs.create({url: resultData['url']}); 
                                    },
                                    dataType: "text"
                                });
                                console.log("TEST");
                                console.log(info.selectionText); 
                              }
});
/*
console.log("SOMETHING");
chrome.extension.onRequest.addListener(
        $.ajax({
            type: "POST",
            url: "http://40.121.54.11:80/generate/all",
            data: request.content,
            success: function(resultData) { console.log(resultData); },
            dataType: "text"
    });
});
*/

chrome.browserAction.onClicked.addListener(function(tab) {
    console.log("SELECTED");
    console.log(tab);
    chrome.tabs.executeScript(null, { file: "jquery.js" }, function() {
        chrome.tabs.executeScript(null,{
          code : `
function textNodesUnder(el) {
    var n, a=[], walk=el.createTreeWalker(el,NodeFilter.SHOW_TEXT,null,false);
    while(n=walk.nextNode()) {
        console.log(n, n.parentNode);
        /*
        if (['SCRIPT', 'STYLE'].indexOf(n.parentNode.tagName) >= 0) {
            continue;
        }
        */
        if (['P', 'SPAN', 'H1', 'H2'].indexOf(n.parentNode.tagName) >= 0) {
            a.push(n);
        }
    }
    return a;
}
textnodes=textNodesUnder(document);
text = new Array(textnodes.length);
for (var i = 0; i < textnodes.length; ++i) {
    text[i] = textnodes[i].data;
}
requestStr = text.join(' ');
//requestStr = 'nasdaq facebook google tesla';
console.log(requestStr);
//chrome.extension.sendRequest({content: requestStr}, function(response) {console.log('aaaaa'); console.log(response); });
$.ajax({
    type: "POST",
    url: "http://40.121.54.11:80/generate/all",
    data: requestStr,
    success: function(resultData) {
        resultData = JSON.parse(resultData);
        console.log(resultData);
        console.log(textNodesUnder(document));
        for (var key in resultData) {
            console.log(key, resultData[key]);
            for (var i = 0; i < textnodes.length; ++i) {
                if (text[i].indexOf(key) >= 0) {
                    //var updown = resultData[key].pricechange[0];
                    //var stockLink = document.createTextNode(textnodes[i].data);
                    arr = textnodes[i].data.split(key);
                    textnodes[i].data = "";
                    for (var j = 0; j < arr.length - 1; j++){
                        textnodes[i].data += arr[j] + key + " (" + resultData[key].pricechange + ", " + resultData[key].price + ")";
                    }
                    textnodes[i].data += arr[arr.length - 1]
                    //textnodes[i].parentNode.insertAfter(stockLink, textnodes[i]);
                }
            }
        }
    },
    dataType: "text"
});
`
        }, function() { console.log('done'); });
    });
});
