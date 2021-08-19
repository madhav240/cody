var viewpy;
var app = document.getElementById('app')
var file;
var htmls;
var searchBar = document.getElementById("search-input")
var loader = document.getElementById("loader")
var view = document.getElementById('view')
var analyze = document.getElementById('analyze')
var dochtmls = {}
var s_sugg = []
document.getElementById('upload-file').addEventListener('change', function() {
    file = this.files[0]
    var req = new XMLHttpRequest();
    req.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            htmls = JSON.parse(this.responseText);
            loader.style.display = "none"
            view.style.display = ""
            analyze.style.display = ""
        } else {
            loader.style.display = "flex"
        }
    }
    req.open('POST', '/', true);
    req.setRequestHeader("Content-Type", "application/octet-stream");
    req.setRequestHeader("X-File-Name", file.name);
    req.setRequestHeader("X-File-Type", file.type);
    req.send(file);
})

function changeHTML(html) {
    app.innerHTML = html
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
    hljs.highlightAll()
}
view.onclick = function() {
    changeHTML(htmls['viewHTML'])
}
analyze.onclick = function() {
    changeHTML(htmls["analyzeHTML"])
}

function changeLoc() {
    window.location.href = "#" + searchBar.value
}

function search() {
    let sv = searchBar.value.trim()
    searchBar.value = sv
    if (sv != "") {
        var links = []
        let l = document.getElementsByTagName('dt')
        for (var i = 0; i < l.length; i++) {
            links.push(l[i].id);
        }
        if (links.includes(sv)) {
            changeLoc()
        } else if (dochtmls[sv] != undefined) {
            changeHTML(dochtmls[sv])
        } else {
            var req = new XMLHttpRequest();
            req.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                    sl = this.responseText
                    dochtmls[sv] = this.responseText
                    let sidx = 0;
                    let eidx = 4
                    if (sl.slice(sidx, eidx) != "$##$") {
                        changeHTML(this.responseText)
                        l = document.getElementsByTagName('dt')
                        for (var i = 0; i < l.length; i++) {
                            s_sugg.push({
                                label: l[i].id
                            });
                        }
                    } else {
                        changeHTML(sl.substr(0, sidx) + sl.substr(eidx))
                        changeLoc()
                    }
                    loader.style.display = "none"
                } else if (this.readyState == 4 && this.status == 500) {
                    loader.style.display = "none"
                    Toastify({
                        text: "No Docs Found",
                        duration: 2000,
                        gravity: "bottom",
                    }).showToast();
                } else {
                    loader.style.display = "flex"
                }
            }
            req.open('POST', '/', true);
            req.send(sv)
        }
    }
}
document.getElementById('FileMenu').onclick = function() {
    let User_Dropdown = document.getElementsByClassName("User-Dropdown")[0]
    if (User_Dropdown.classList.contains("U-open")) {
        User_Dropdown.classList.remove("U-open");
    } else {
        User_Dropdown.classList.add("U-open");
    }
};
searchBar.addEventListener("keyup", function(event) {
    if (event.keyCode === 13) {
        event.preventDefault();
        search();
    }
});