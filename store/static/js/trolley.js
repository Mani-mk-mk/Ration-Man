// converting the 0 price to --N/A--
var len = document.getElementsByClassName("shopprice").length
var price = document.querySelectorAll(".shopprice");

for (let index = 0; index < len; index++) {
    prices = price[index].innerText;
    console.log(prices)
    if (prices === "₹ 0"){
        price[index].innerHTML = "--N/A--";
    }
}

//counting how many products are --N/A--
var count_flipkart = 0;
var count_amazon = 0;
var count_bigb = 0;

var total_flipkart = 0;
var total_amazon = 0;
var total_bigb = 0;

var lenf = document.getElementsByClassName("flipkart").length
var pricef = document.querySelectorAll(".flipkart");
for (let index = 0; index < lenf; index++) {
    pricesf = pricef[index].innerText;
    if (pricesf == "--N/A--"){
        count_flipkart = count_flipkart + 1;
    }
    else{
        pricesf = pricesf.replace("₹ ","");
        pricesf = parseFloat(pricesf);
        total_flipkart += pricesf;
    }
}

var lena = document.getElementsByClassName("amazon").length
var pricea = document.querySelectorAll(".amazon");
for (let index = 0; index < lena; index++) {
    pricesa = pricea[index].innerText;
    if (pricesa == "--N/A--"){
        count_amazon = count_amazon + 1;
    }
    else{
        pricesa = pricesa.replace("₹ ","");
        pricesa = parseFloat(pricesa);
        total_amazon += pricesa;
    }
}

var lenb = document.getElementsByClassName("bigb").length
var priceb = document.querySelectorAll(".bigb");
for (let index = 0; index < lenb; index++) {
    pricesb = priceb[index].innerText;
    if (pricesb == "--N/A--"){
        count_bigb = count_bigb + 1;
    }
    else{
        pricesb = pricesb.replace("₹ ","");
        pricesb = parseFloat(pricesb);
        total_bigb += pricesb;
    }
}

console.log("count_flipkart: "+count_flipkart);
console.log("count_amazon: "+count_amazon);
console.log("count_bigb: "+count_bigb);

console.log("total_flipkart: "+total_flipkart);
console.log("total_amazon: "+total_amazon);
console.log("total_bigb: "+total_bigb);

var total_f = document.querySelector(".total-f");
console.log(total_f);
total_f.innerHTML = "<td class='total-shop total-f'> ₹ " + total_flipkart + "</td>";

var total_a = document.querySelector(".total-a");
total_a.innerHTML = "<td class='total-shop total-a'> ₹ " + total_amazon + "</td>";

var total_b = document.querySelector(".total-b");
total_b.innerHTML = "<td class='total-shop total-a'> ₹ " + total_bigb + "</td>";

//shows where you can get most of products best buy and best price 
var offer = document.querySelector(".offer");
var best_buy = document.querySelector(".bestbuy");
var checkout = document.querySelector("#checkout");
console.log(offer);
if (count_flipkart < count_amazon && count_flipkart < count_bigb){
    offer.innerHTML = "<h5>Offered By: <strong> Flipkart </strong> </h5>";
    best_buy.innerHTML = "<h5>Best price: <strong>₹ " + total_flipkart + "</strong></h5>"; 

}
else if (count_amazon < count_bigb){
    offer.innerHTML = "<h5>Offered By: <strong> Amazon </strong> </h5>";
    best_buy.innerHTML = "<h5>Best price: <strong>₹ " + total_amazon + "</strong></h5>";
}
else if (count_amazon === count_bigb && count_amazon === count_flipkart){
    if (total_flipkart < total_amazon && total_flipkart < total_bigb){
        offer.innerHTML = "<h5>Offered By: <strong> Flipkart </strong> </h5>";
        best_buy.innerHTML = "<h5>Best price: <strong>₹ " + total_flipkart + "</strong></h5>";  
    }
    else if (total_amazon < total_bigb){
        offer.innerHTML = "<h5>Offered By: <strong> Amazon </strong> </h5>";
        best_buy.innerHTML = "<h5>Best price: <strong>₹ " + total_amazon + "</strong></h5>";
    }
    else{
        offer.innerHTML = "<h5>Offered By: <strong> Big Basket </strong> </h5>";
        best_buy.innerHTML = "<h5>Best price: <strong>₹ " + total_bigb + "</strong></h5>";
    }
}
else if (count_amazon === count_bigb && count_flipkart > 0){
    if (total_amazon < total_bigb){
        offer.innerHTML = "<h5>Offered By: <strong> Amazon </strong> </h5>";
        best_buy.innerHTML = "<h5>Best price: <strong>₹ " + total_amazon + "</strong></h5>";
    }
    else{
        offer.innerHTML = "<h5>Offered By: <strong> Big Basket </strong> </h5>";
        best_buy.innerHTML = "<h5>Best price: <strong>₹ " + total_bigb + "</strong></h5>";
    }
}
else if (count_amazon === count_flipkart && count_bigb > 0){
    if (total_amazon < total_flipkart){
        offer.innerHTML = "<h5>Offered By: <strong> Amazon </strong> </h5>";
        best_buy.innerHTML = "<h5>Best price: <strong>₹ " + total_amazon + "</strong></h5>";
    }
    else{
        offer.innerHTML = "<h5>Offered By: <strong> Flipkart </strong> </h5>";
        best_buy.innerHTML = "<h5>Best price: <strong>₹ " + total_flipkart + "</strong></h5>";
    }
}
else if (count_flipkart === count_bigb && count_amazon > 0){
    if (total_flipkart < total_bigb){
        offer.innerHTML = "<h5>Offered By: <strong> Flipkart </strong> </h5>";
        best_buy.innerHTML = "<h5>Best price: <strong>₹ " + total_flipkart + "</strong></h5>";
    }
    else{
        offer.innerHTML = "<h5>Offered By: <strong> Big Basket </strong> </h5>";
        best_buy.innerHTML = "<h5>Best price: <strong>₹ " + total_bigb + "</strong></h5>";
    }
}
else{
    offer.innerHTML = "<h5>Offered By: <strong> Big Basket </strong> </h5>";
    best_buy.innerHTML = "<h5>Best price: <strong>₹ " + total_bigb + "</strong></h5>";
}