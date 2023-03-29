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

function sendEmail(){
    const data = new FormData(document.querySelector('#contact form'));

    fetch(`/send_message/`,{
        method: 'POST',
        header: {  
            'Content-Type': "multipart/form-data",
        }, 
        body: data,
        credentials: 'same-origin',
    }).then( (result) => {
        if (result.status == 200)
            alert('Message sent successfully, thank you for your message. I will reply as soon as possible (make sure that the email is correct, otherwise I cannot reply)')
    })

    //clear form
    document.querySelectorAll('#contact form input')[2].value = ''
    document.querySelectorAll('#contact form input')[3].value = ''
    document.querySelector('#contact form textarea').value = ''

    return false;
}