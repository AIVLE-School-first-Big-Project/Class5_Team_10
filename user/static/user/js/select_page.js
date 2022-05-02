const imgClickHandler = document.querySelectorAll(img.profile-card)

function onClickHandling(kid_id){
    sessionStorage.removeItem('kid_id')
    sessionStorage.setItem('kid_id', kid_id)
    window.location
}

imgClickHandler.addEventListener("click", onClickHandling())