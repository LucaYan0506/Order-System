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

document.querySelector('form').onsubmit = () =>{
    return validation(document.querySelector('form'));
}

function validation(form){
    const data = new FormData(form);
    fetch(`/send_message/`,{
        method: 'POST',
        header: {  
            'Content-Type': "multipart/form-data",
        }, 
        body: data,
        credentials: 'same-origin',
    })
    alert('Message submited')
    return false;
}