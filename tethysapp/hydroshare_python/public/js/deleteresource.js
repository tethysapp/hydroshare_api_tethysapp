
const clickevent = (event) => {
    var r = confirm("Are you sure ?")
    if (r==false){
        event.preventDefault()
    }
}

var deletebutton = document.querySelector("[name=delete-button]")
deletebutton.addEventListener('click', clickevent);