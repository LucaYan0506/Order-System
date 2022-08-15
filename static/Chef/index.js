  
const socket = new WebSocket(`ws://${window.location.hostname}:8001/ws/chat/`);
socket.onmessage = (event) => {
    var data = JSON.parse(event.data);
    const div = document.createElement('div');
    div.style.height = '300px';
    div.style.width = '200px';
    div.className = 'container'

    const inner = document.createElement('div');
    inner.innerHTML = data['order']['dishes'];
    inner.style.height = '260px';
    inner.style.overflowY = 'auto';
    div.append(inner);

    const button = document.createElement('button')
    button.innerText = "Start";
    button.className = 'btn';
    button.style.background = 'red';
    button.style.color = 'white';
    button.dataset['pk'] = data['order']['pk'];
    button.onclick = () => {
        startOrder(button);
    }
    div.append(button);

    document.querySelector('#order-container').append(div);

    //change to in progress if need
    if (data['order']['status'] == 'in progress')
        button.click();
}

document.addEventListener('DOMContentLoaded',()=>{
    const editor = CKEDITOR.instances['id_dishes']

    fetch(`/chef/order_info/`)
    .then(response => response.json())
    .then(result => {
        result.orders.forEach(order => {
            const div = document.createElement('div');
            div.style.height = '300px';
            div.style.width = '200px';
            div.className = 'container'
    
            const inner = document.createElement('div');
            inner.innerHTML = order.dishes;
            inner.style.height = '260px';
            inner.style.overflowY = 'auto';
            div.append(inner);
            
            const button = document.createElement('button')
            button.innerText = "Start";
            button.className = 'btn';
            button.style.background = 'red';
            button.style.color = 'white';
            button.dataset['pk'] = order.pk;
            button.onclick = () => {
                startOrder(button);
            }
            div.append(button);
    
            document.querySelector('#order-container').append(div);

            //change to in progress if need
            if (order.status == 'in progress')
                button.click();
        });
    })
})

function startOrder(button){
    button.innerText = "In progress";
    button.className = 'btn';
    button.style.background = '#0053ff';

    const data = new FormData;
    data.append('csrfmiddlewaretoken', document.querySelector('input[name="csrfmiddlewaretoken"]').value);
    data.append('pk',button.dataset['pk']);

    fetch(`/chef/order_in_progress/`,{
        method: 'POST',
        header: {  
            'Content-Type': "multipart/form-data",
        }, 
        body: data,
        credentials: 'same-origin',
    })

    button.onclick = () => {
        if (confirm('Is this order completed?'))
            completeOrder(button);
    }
}

function completeOrder(button){
    const data = new FormData;
    data.append('csrfmiddlewaretoken', document.querySelector('input[name="csrfmiddlewaretoken"]').value);
    data.append('pk',button.dataset['pk']);
    
    fetch(`/chef/order_done/`,{
        method: 'POST',
        header: {  
            'Content-Type': "multipart/form-data",
        }, 
        body: data,
        credentials: 'same-origin',
    })

    button.innerText = "Complete";
    button.className = 'btn';
    button.style.background = 'green';

    const order = button.parentElement;

    setTimeout(() => {
        order.parentElement.removeChild(order);
    }, 500);
}