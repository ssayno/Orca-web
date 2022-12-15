function toggleTagAddEL(ATag){
    ATag.addEventListener('click', function (event){
    let showConnected = ATag.parentElement.parentElement.parentElement.getElementsByClassName('origin-hide')[0];
    let status = showConnected.style.display;
    console.log(status)
    if(!status || status === "none"){
        showConnected.style.display = 'block';
    }else if (status === 'block'){
        showConnected.style.display = 'none';
    }
})}
/* upload file usage*/
function createDiv(singleJson, parent){
    let number = singleJson['number'];
    let latestTime = singleJson['latest_event']['time_iso'];
    let state = singleJson['state'];
    let events = singleJson['events'];
    // create element
    const singleDiv = document.createElement('div');
    singleDiv.setAttribute('class', 'single');
    const singleDivHeader = document.createElement('div');
    singleDivHeader.setAttribute('class', 'single-header');
    const singleDivHeaderP = document.createElement('p');
    // a tag event listener
    const spanTag= document.createElement('span');
    const toggleATag = document.createElement('a');
    toggleATag.setAttribute('href', 'javascript:void(0);');
    toggleATag.innerHTML = 'x';
    singleDivHeaderP.innerHTML = number + latestTime;
    toggleTagAddEL(toggleATag);
    const originHiddenDiv = document.createElement('div');
    originHiddenDiv.setAttribute('class', 'origin-hide');
    const ulElement = document.createElement('ul');
    for(let _event of events){
        console.log(_event, typeof _event);
        let _event_content = "";
        for(let key in _event){
            _event_content += `${key}: ${_event[key]}----`
        }
        const liElement = document.createElement('li');
        liElement.innerHTML = _event_content;
        ulElement.appendChild(liElement);
    }
    // append child
    singleDiv.appendChild(singleDivHeader);
    singleDiv.appendChild(originHiddenDiv);
    singleDivHeader.appendChild(singleDivHeaderP);
    singleDivHeader.appendChild(spanTag);
    spanTag.appendChild(toggleATag);
    originHiddenDiv.appendChild(ulElement);
    //
    parent.appendChild(singleDiv);
}
const uploadFileForm = document.getElementById('only-file');
uploadFileForm.addEventListener('change', function (event){
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange=function() {
        if (xhttp.readyState === 4 && xhttp.status === 200)
        {
            const resultJson = JSON.parse(xhttp.response);
            const contentDiv = document.getElementById('content');
            for(let singleJson of resultJson){
                createDiv(singleJson, contentDiv);
            }
        }
    }
    let formData = new FormData();
    formData.append('file', this.files[0])
    xhttp.open('post', '/upload', true);
    xhttp.send(formData);
})
