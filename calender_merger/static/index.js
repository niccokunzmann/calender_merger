
const DEFAULT_URL = "http://calender-merger.herokuapp.com";


function updateUrls() {
    updateCalenderInputs();
    updateOutputs();
}

function updateCalenderInputs() {
    var urlInputs = document.getElementsByClassName("calender-url-input");
    var calenderUrls = document.getElementById("calender-urls");
    var hasEmptyInput = false;
    for (var i = 0; i < urlInputs.length; i+= 1) {
        var urlInput = urlInputs[i];
        hasEmptyInput |= urlInput.value == "";
    }
    if (!hasEmptyInput) {
        var li = document.createElement("li");
        var input = document.createElement("input");
        input.type = "text";
        input.classList.add("calender-url-input");
        input.addEventListener("change", updateUrls);
        input.addEventListener("keyup", updateUrls);
        input.id = "calender-url-input-" + urlInputs.length;
        li.appendChild(input);
        calenderUrls.appendChild(li);
    }
}

function getUrls() {
    var urls = [];
    var urlInputs = document.getElementsByClassName("calender-url-input");
    for (var i = 0; i < urlInputs.length; i+= 1) {
        var urlInput = urlInputs[i];
        var url = urlInput.value;
        if (url) {
            urls.push(url);
        }
    }
    return urls;
}

function getMergedUrl(urls) {
    var url;
    if (document.location.protocol == "file:") {
        url = DEFAULT_URL + "/join-calenders.ics?";
    } else {
        url = document.location.protocol + "//" + document.location.host + "/join-calenders.ics?";
    }
    var arguments = urls.map(function(url){
        return encodeURIComponent(url) + "="
    });
    return url + arguments.join("&");
}

var lastMergedUrl = "";

function updateOutputs() {
    var urls = getUrls();
    console.log("urls", urls);
    var mergedUrl = getMergedUrl(urls);
    if (lastMergedUrl == mergedUrl) {
        return;
    }
    lastMergedUrl = mergedUrl;
    console.log("mergedUrl", mergedUrl);
    displayJoinedLink(mergedUrl);
    var instantcalUrl = getInstantCalFrameUrl(mergedUrl);
    console.log("instantcalUrl", instantcalUrl);
    displayCalenderLink(instantcalUrl);
    displayCalender(instantcalUrl);
    showCalenderSourceCode(instantcalUrl);
    
}

function displayJoinedLink(url) {
    var link = document.getElementById("joined-link");
    link.innerText = url;
    link.href = url;
}
function displayCalenderLink(url) {
    var link = document.getElementById("calender-link");
    link.innerText = url;
    link.href = url;
}
function getInstantCalFrameUrl(url) {
    var frameUrl = encodeURIComponent(url).replace(/%25/g, "%");
    return "http://cdn.instantcal.com/cvir.html?id=cv_nav5&file=" + frameUrl + "&theme=RE&ccolor=%23ffffc0&dims=1&gtype=cv_monthgrid&gcloseable=0&gnavigable=1&gperiod=month&itype=cv_simpleevent";
}
function displayCalender(url) {
    var link = document.getElementById("cv_if5");
    link.src = url;
}
function showCalenderSourceCode(url) {
    var link = document.getElementById("calender-code");
    link.innerText = "<iframe id='cv_if5' \nsrc='" + encodeURI(url) + "' \nallowTransparency=true scrolling='no' frameborder=0 height=600 width=800></iframe>";
}




window.addEventListener("load", function(){
    updateCalenderInputs();
});



