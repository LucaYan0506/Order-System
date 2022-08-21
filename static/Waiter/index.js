function show_mobile_nav(){
    document.querySelector('#mobile-navbar').style.display ="block";
}

function hide_mobile_nav(){
    document.querySelector('#mobile-navbar').style.display="";
}

document.querySelectorAll('#mobile-navbar li').forEach( el => {
    el.onclick = () => {
        hide_mobile_nav();
    }
})