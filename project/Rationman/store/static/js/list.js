var update = document.getElementsByClassName('update-list');

for(var i = 0; i<update.length; i++){
    update[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log(productId);
        console.log(action);

        if (user == 'AnonymousUser') {
            console.log("User not logged in");
        }else {
            updateUserList(productId, action)        
        }
    })

}

function updateUserList(productId, action){
    console.log("User is logged in Sending data in...");
    var url = '/update_list/'
    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        }, 
        body:JSON.stringify({'productId':productId, 'action':action})
    })
    .then((response) => {
       return response.json();
    })
    .then((data) => {
        console.log('data: ',data);
        location.reload()
    });

}
