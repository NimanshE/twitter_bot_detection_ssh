var cache = {};
function loadPage(url) {
    if (cache[url]) {
        return new Promise(function (resolve) {
            resolve(cache[url]);
        });
    }

    return fetch(url, {
        method: 'GET'
    }).then(function (response) {
        cache[url] = response.text();
        return cache[url];
    });
}

var main = document.querySelector('main');

function changePage() {
    var url = window.location.href;

    loadPage(url).then(function (responseText) {
        var wrapper = document.createElement('div');
        wrapper.innerHTML = responseText;

        var oldContent = document.querySelector('.cc');
        var newContent = wrapper.querySelector('.cc');

        main.appendChild(newContent);
        animate(oldContent, newContent);
    });
}

function animate(oldContent, newContent) {
    oldContent.style.position = 'absolute';

    var fadeOut = oldContent.animate({
        opacity: [1, 0]
    }, 1000);

    var fadeIn = newContent.animate({
        opacity: [0, 1]
    }, 1000);

    fadeIn.onfinish = function () {
        oldContent.parentNode.removeChild(oldContent);
    };
}

window.addEventListener('popstate', changePage);

document.addEventListener('click', function (e) {
    var el = e.target;

    while (el && !el.href) {
        el = el.parentNode;
    }

    if (el) {
        e.preventDefault();
        history.pushState(null, null, el.href);
        changePage();

        return;
    }
});

document.getElementById("sendReq").addEventListener("click",()=>{
    req(document.getElementById("reqText").value);
});

async function req(reqText){
    const resp = await fetch(`http://localhost:5000?id=${reqText}`, {
        method: "GET",
        headers: {"Access-Control-Allow-Origin": "*"}
    })
    data = await resp.json();
    if(data.pred===1){
        alert("It is a bot");
    }else{
        alert("It is not a bot");
    }
}