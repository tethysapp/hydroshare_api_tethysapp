mapboxgl.accessToken = 'pk.eyJ1IjoiYWJoaXNoZWthbWFsMTgiLCJhIjoiY2s1eTVxNGExMmQ5MDNubjExaWY5MjdvbSJ9.3nmdjWZmUCDNyRdlPo5gbg';
var map = new mapboxgl.Map({
container: 'mapid',
style: 'mapbox://styles/abhishekamal18/ckd7nht1p04hn1ipcddzbndkd', // stylesheet location
center: [-74.5, 40], // starting position [lng, lat]
zoom: 9 // starting zoom
});



let resourceslist = []


let button = document.getElementById('fetchfile')
const fileSelector = document.querySelector('#title_input')
button.addEventListener('click', async function () {
    const username = document.getElementById('username')
    const password = document.getElementById('password')
    const viewr = document.getElementById('viewr')
    const csrfToken = document.querySelector('input[name=csrfmiddlewaretoken]')

    const formData = new FormData();
    formData.append('username', username.value);
    formData.append('password', password.value);
    formData.append('viewr', viewr.value);
    formData.append('csrfmiddlewaretoken', csrfToken.value);

    const response = await fetch('/apps/hydroshare-python/mapview/', {
        method: 'post',
        body: formData
    });

    const responseData = await response.json()
    resourceslist = responseData

    var child = fileSelector.lastElementChild;
    while (child) {
        fileSelector.removeChild(child);
        child = fileSelector.lastElementChild;
    }
    // Default option
    const option = document.createElement('option');
    option.textContent = "Select a Resource";
    fileSelector.append(option)

    // File name options
    responseData.filter(resource=>{
        
        if(!resource.coverages || resource.coverages.length==0){
            return false
        }
        console.log(resource)
        const box = resource.coverages.find(coveragesItem=>coveragesItem.type=="box")
        if (box){return true}
        return false
    }).forEach(result => {
        const option = document.createElement('option');
        option.value = result.resource_id;
        option.textContent = result.resource_title;
        fileSelector.append(option)
    })
})
fileSelector.addEventListener('change', function(event){
    const selected = document.querySelector('#selected_resource')
    selected.textContent = event.target.value
})

const viewbutton = document.querySelector('[name=add-button]')
viewbutton.addEventListener('click', function(event){
    event.preventDefault()
    const selectedid = fileSelector.value
    const resource = resourceslist.find(resource=>resource.resource_id==selectedid)
    if(resource){
        console.log("Map works")
        const box = resource.coverages.find(coveragesItem=>coveragesItem.type=="box")
        var bounds = [[box.value.northlimit, box.value.westlimit], [box.value.southlimit, box.value.eastlimit]];
// create an orange rectangle
        L.rectangle(bounds, {color: "#ff7800", weight: 3}).addTo(mymap);
// zoom the map to the rectangle bounds
        mymap.fitBounds(bounds);
    }
})


