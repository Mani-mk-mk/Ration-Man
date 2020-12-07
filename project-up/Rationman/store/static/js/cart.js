var updateBtns = document.getElementsByClassName('update-cart');

for(var i=0;i<updateBtns.length;i++) {
    updateBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action

        if (user == 'AnonymousUser') {
            console.log("User not logged in");
        }else {
            updateUserOrder(productId, action)
        }
    })
}

function updateUserOrder(productId, action){
    console.log("User is logged in Sending data in...");
    var url = '/update_item/'
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

//USERLIST


/*var price_f = document.getElementsByClassName("flipkart");
var price_a = document.getElementsByClassName("amazon");
var price_b = document.getElementsByClassName("bigb");
console.log(price_f);
for (var i = 0;i<price_f.length; i++) {
    var sum = 0;
    sum = sum+price_f;
    console.log(sum);
}

*/