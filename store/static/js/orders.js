var company_id = document.querySelectorAll(".companyname")

for (let index = 0; index < company_id.length; index++) {
    var id = company_id[index].innerText
    if (id === "3"){
        company_id[index].innerHTML = "Bigbasket";
        console.log("Bigbasket");
    }
    else if (id === "2"){
        company_id[index].innerHTML = "Amazon";
        console.log("Amazon");
    }
    else if (id === "1"){
        company_id[index].innerHTML = "Flipkart";
        console.log("Flipkart")
    }
}