var prev_link;
var root = document.querySelector(':root');
const socket = new WebSocket(`ws://${window.location.hostname}:8001/ws/chat/`);

document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#category').className += "selected-link";

    prev_link = document.querySelector(".selected-link");

    if (window.location.search.includes('basket'))
        openBasket()

    if (window.location.search.includes('order'))
        openOrder()

})

function update_basket(dish_pk, n){
    const data = new FormData();
    data.append('table_pk',table_pk)
    data.append('dish_pk',dish_pk)
    data.append('n',n)
    data.append('csrfmiddlewaretoken', document.querySelector('input[name="csrfmiddlewaretoken"]').value);

    fetch('/basket/update/',{
        method: 'POST',
        header: {  
            'Content-Type': "multipart/form-data",
        }, 
        body: data,
        credentials: 'same-origin',
    })
    .then(response => response.json())
    .then(result => {
        console.log(result['totPrice'])
        document.querySelector('span.total#price').innerHTML = result['totPrice'];
    })
}

document.querySelectorAll('.btn.circle#plus').forEach(button => {
    button.onclick = () =>{
        let n = parseInt(++button.parentElement.dataset['quantity']);

        button.parentElement.querySelector('#quantity').innerHTML = n;
        update_basket(button.parentElement.dataset['dish_pk'],n)
        let value  = `"${parseInt(getComputedStyle(root).getPropertyValue('--basket-number-items').replaceAll('"','').replaceAll(' ', '')) + 1}"`
        root.style.setProperty('--basket-number-items',value);

        const minus = button.parentElement.querySelector('.btn.circle#minus');
        minus.style.visibility = 'inherit';
        minus.style.user_select = 'inherit';
    }
})

document.querySelectorAll('.btn.circle#minus').forEach(button => {
    button.onclick = () =>{
        let n = parseInt(--button.parentElement.dataset['quantity']);
        
        if (n < 0)
            n = button.parentElement.dataset['quantity'] = 0;
        else{
            let value  = `"${parseInt(getComputedStyle(root).getPropertyValue('--basket-number-items').replaceAll('"','').replaceAll(' ', '')) - 1}"`
            root.style.setProperty('--basket-number-items',value);
        }

        button.parentElement.querySelector('#quantity').innerHTML = n;
        update_basket(button.parentElement.dataset['dish_pk'],n)

        if (n == 0){
            button.style.visibility = '';
            button.style.user_select = '';
        }
    }
})

 
document.addEventListener('scroll', () => {
    document.querySelectorAll('#dish-container .category').forEach(element => {
        var vh = window.innerHeight + 1;
        if (element.getBoundingClientRect().bottom <= 120){
            prev_link.classList.remove('selected-link');
            prev_link = document.querySelector(`#menu #category[name="${element.id}"]`);
            prev_link.className += "selected-link";
        }
    })
})

document.querySelector('#basket-container').onclick = (e) => {
    window.location.assign(`/menu/?table=${table_pk}&basket`)
}

document.querySelector('#basket-page-container').onclick = (e) => {
    if (e.target == document.querySelector('#basket-page-container'))
        closeBasket();
}

function openBasket(){
    document.querySelector('body').style.overflow = 'hidden';
    document.querySelector('#basket-page-container').style.top = "0"
}

function closeBasket(){
    location.assign(`/menu/?table=${table_pk}`)
}

document.querySelector('#completed-order-container').onclick = (e) => {
    window.location.assign(`/menu/?table=${table_pk}&order`)
}

document.querySelector('#order-page-container').onclick = (e) => {
    if (e.target == document.querySelector('#order-page-container'))
        closeBasket();
}

function openOrder(){
    document.querySelector('body').style.overflow = 'hidden';
    document.querySelector('#order-page-container').style.top = "0"
}

function closeOrder(){
    location.assign(`/menu/?table=${table_pk}`)
}

function clearBasket(pk){
    const data = new FormData;
    data.append('csrfmiddlewaretoken', document.querySelector('input[name="csrfmiddlewaretoken"]').value);
    data.append('basket_pk',pk);

    fetch('/basket/clear/',{
        method: 'POST',
        header: {  
            'Content-Type': "multipart/form-data",
        }, 
        body: data,
        credentials: 'same-origin',
    })
    .then(
        setTimeout(()=>{
            location.reload()
        },500)
    )
}

function orderBasket(pk){
    const data = new FormData;
    data.append('csrfmiddlewaretoken', document.querySelector('input[name="csrfmiddlewaretoken"]').value);
    data.append('basket_pk',pk);

    fetch('/order/',{
        method: 'POST',
        header: {  
            'Content-Type': "multipart/form-data",
        }, 
        body: data,
        credentials: 'same-origin',
    })
    .then(response => response.json())
    .then(data => {
        if (data.result == 'Error'){
            alert('Your basket is empty.');
        }else{
            socket.send(JSON.stringify({
                'order':{
                    'dishes':data.dishes,
                    'pk':data.pk,
                    'status':data.status,
                },
            }))
        }
        location.reload()
    })
}
