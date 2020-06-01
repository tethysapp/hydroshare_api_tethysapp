// var mymap = L.map('mapid').setView([51.505, -0.09], 13);

// L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
//     attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
//     maxZoom: 18,
//     id: 'mapbox/streets-v11',
//     tileSize: 512,
//     zoomOffset: -1,
//     accessToken: 'your.mapbox.access.token'
//     }).addTo(mymap);

const clickevent = (event) => {
    var r = confirm("Are you sure ?")
    if (r==false){
        event.preventDefault()
    }
}

var addbutton = document.querySelector("[name=add-button]")
addbutton.addEventListener('click', clickevent);

var createbutton = document.querySelector("[name=create-button]")
createbutton.addEventListener('click', clickevent);

let button = document.getElementById('fetchfile')
button.addEventListener('click', async function () {
    const username = document.getElementById('username')
    const password = document.getElementById('password')
    const resourceid = document.getElementById('resourcein')
    const csrfToken = document.querySelector('input[name=csrfmiddlewaretoken]')
    const fileSelector = document.getElementById('title_input')

    const formData = new FormData();
    formData.append('username', username.value);
    formData.append('password', password.value);
    formData.append('resourcein', resourceid.value);
    formData.append('csrfmiddlewaretoken', csrfToken.value);

    const response = await fetch('/apps/hydroshare-python/filev/', {
        method: 'post',
        body: formData
    });

    const responseData = await response.json()


    var child = fileSelector.lastElementChild;
    while (child) {
        fileSelector.removeChild(child);
        child = fileSelector.lastElementChild;
    }
    // Default option
    const option = document.createElement('option');
    option.textContent = "Select a file";
    fileSelector.append(option)

    // File name options
    responseData.results.forEach(result => {
        const option = document.createElement('option');
        option.value = result.file_name;
        option.textContent = result.file_name;
        fileSelector.append(option)
    })
})

