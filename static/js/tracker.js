/* connect websocket*/
const socket = io();
socket.on('connect', function(message) {
    console.log(message);
    socket.send("Webbrower connect");
    console.log("Websocket connect successfully");

});
/* update package info*/
socket.on('packerUpdate', function(message) {
    console.log(message);
    console.log("Get your message");
});
const showATags = document.getElementsByClassName('toggle-sh');
console.log(showATags);
for(let showATag of showATags){
    showATag.addEventListener('click', function (event){
    let showConnected = showATag.parentElement.parentElement.parentElement.getElementsByClassName('origin-hide')[0];
    let status = showConnected.style.display;
    console.log(status)
    if(!status || status === "none"){
        showConnected.style.display = 'block';
    }else if (status === 'block'){
        showConnected.style.display = 'none';
    }
})}
/* upload file usage*/
const uploadFileForm = document.getElementById('only-file');
console.log(uploadFileForm);
uploadFileForm.addEventListener('change', function (event){
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange=function() {
        if (xhttp.readyState === 4 && xhttp.status === 200)
        {
            console.log(xhttp.response);
            console.log("Upload file successfully");
        }
    }
    let formData = new FormData();
    formData.append('file', this.files[0])
    xhttp.open('post', '/upload', true);
    xhttp.send(formData);
})
