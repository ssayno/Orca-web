const socketio = io();

socketio.on('connect', function (message) {
    console.log("show I'm connected");
})
socketio.on('update', function (resultJson) {
    const contentTag = document.getElementById('content');
    const parsedResultJson = JSON.parse(resultJson);
    //
    const type_ = parsedResultJson['type'];
    const jsonData = JSON.parse(parsedResultJson['data']);
    const packages_count = parsedResultJson['count'];
    const spanPrefix = document.getElementById('prefix');
    const spanPostfix = document.getElementById('postfix');
    if (type_ === "init") {
        console.log("clear");
        contentTag.querySelectorAll('div.single').forEach(
            function (node, index) {
                node.remove();
            }
        )
        spanPrefix.innerHTML = 0;
        spanPostfix.innerHTML = packages_count;
    } else if (type_ === "add") {
        console.log("add");
        spanPrefix.innerHTML = parseInt(spanPrefix.innerHTML) + packages_count
        console.log("get", jsonData);
        for (let singleJson of jsonData) {
            createDiv(singleJson, contentTag);
        }
        socketio.emit(
            'update', "fin"
        )
    }
})

function popAdd(message) {
    layui.use('layer', function () {
        const layer = layui.layer;
        layer.open({
            type: 1,
            title: '详细信息',
            area: ['800px', '1000px'],
            content: message
        });
    });
}

function toggleTagAddEL(ATag) {
    ATag.addEventListener('click', function (event) {
        let showConnected = ATag.parentElement.parentElement.parentElement.getElementsByClassName('origin-hide')[0];
        let status = showConnected.style.display;
        if (!status || status === "none") {
            showConnected.style.display = 'inline-block';
        } else if (status === 'inline-block') {
            showConnected.style.display = 'none';
        }
    })
}

/* upload file usage*/
function createDiv(singleJson, parent) {
    console.log("start create");
    console.log(singleJson);
    let number = singleJson['number'];
    let latestTime = singleJson['latest_event']['time_iso'];
    let state = singleJson['state'];
    let events = singleJson['events'];
    // create element
    const singleDiv = document.createElement('div');
    singleDiv.setAttribute('class', 'single');
    const singleDivHeader = document.createElement('div');
    singleDivHeader.setAttribute('class', 'single-header');
    // a tag event listener
    const otherDiv = document.createElement('div');
    otherDiv.setAttribute('class', 'others');
    const moreButton = document.createElement('button');
    moreButton.setAttribute('class', 'show-more');
    moreButton.innerHTML = 'More';
    singleDivHeader.innerHTML = `<p>${number}</p><p>${latestTime}</p>`;
    // toggleTagAddEL(toggleATag);
    const ulElement = document.createElement('ul');
    let _event_content = "";
    for (let _event of events) {
        for (let key in _event) {
            _event_content += `${key}: ${_event[key]}----`
        }
        const liElement = document.createElement('li');
        liElement.innerHTML = _event_content;
        ulElement.appendChild(liElement);
    }
    // add event listener
    moreButton.addEventListener('click', () => {
        popAdd(ulElement.outerHTML)
    })
    // append child
    singleDiv.appendChild(singleDivHeader);
    singleDiv.appendChild(otherDiv);
    otherDiv.appendChild(moreButton);
    //
    parent.appendChild(singleDiv);
}

const uploadFileForm = document.getElementById('only-file');
uploadFileForm.addEventListener('change', function (event) {
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (xhttp.readyState === 4 && xhttp.status === 200) {
            console.log("Load finished");
        }
    }
    let formData = new FormData();
    formData.append('file', this.files[0])
    xhttp.open('post', '/upload', true);
    xhttp.send(formData);
})
