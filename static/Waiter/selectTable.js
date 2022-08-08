let table_pk;

document.querySelector('.btn#next').onclick = (e) => {
    window.location.assign(`/menu?table=${table_pk}`)
}

document.querySelectorAll('#table-container div').forEach((elem) => {
    elem.onclick = () => {
        if (table_pk != undefined){
            const prev = document.querySelector(`#table-${table_pk}`);
            prev.style.background = "",
            prev.style.color = "";
        }
        table_pk = elem.id.substring(6);
        elem.style.background = "gray";
        elem.style.color = "white";
    }
})