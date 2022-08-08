  
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
            inner.style.maxHeight = '220px';
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
    
            document.querySelector('body').append(div);
        });
    })
})

function startOrder(button){
    button.innerText = "In progress";
    button.className = 'btn';
    button.style.background = '#0053ff';
    button.onclick = () => {
        if (confirm('Is this order completed?'))
            completeOrder(button);
    }
}

function completeOrder(button){
    button.innerText = "Complete";
    button.className = 'btn';
    button.style.background = 'green';
}