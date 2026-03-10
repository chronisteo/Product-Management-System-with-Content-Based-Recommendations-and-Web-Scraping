const api = "http://127.0.0.1:5000";

window.onload = () => {
    // BEGIN CODE HERE
    const getSearchButton = document.getElementById("searchButton");
    getSearchButton.onclick = searchButtonOnClick;
    const postSaveButton = document.getElementById("saveButton");
    postSaveButton.onclick = productFormOnSubmit;
    // END CODE HERE
}

searchButtonOnClick = () => {
    // BEGIN CODE HERE
  
    const getName = document.getElementById("productName");
    const res = new XMLHttpRequest();
   
    res.open("GET", `${api}/search?name=${getName.value}`);
    
    res.onreadystatechange = () => {
        if (res.readyState == 4) {
            if (res.status == 200) {

                //alert(res.responseText); 
                const resultsDiv = document.getElementById("results");
                resultsDiv.innerHTML = "";

                 for (let i = 0; i < res.responseText.length; i++) {

                    
                    const resText = JSON.parse(res.responseText)[i];
                    
                    
                    //const oidValue = resText._id;
                    const oidValue = resText._id.substr(18);
                    const product = document.createElement("div");
                
                 
                    product.innerHTML =  ` <div class="Flexbox2">
                            <span class="Id">${oidValue}</span>
                            <span class="Name">${resText.name}</span>
                            <span class="Production">${resText.production_year}</span>
                            <span class="Price">${resText.price}</span>
                            <span class="Color">${resText.color}</span>
                            <span class="Size">${resText.size}</span>
                        </div>  ` ; 
            
                    resultsDiv.appendChild(product);
                }
                

            }
        }
    };

    res.send();
    // END CODE HERE
}

productFormOnSubmit = (event) => {
    // BEGIN CODE HERE

    const res = new XMLHttpRequest();
    res.open("POST", `${api}/add-product`);
    res.onreadystatechange = () => {
        if (res.readyState == 4) {
            if (res.status == 200) {
                alert(res.responseText);
            }
        }
    };

    const getName = document.getElementById("name");
    const getProductionYear = document.getElementById("productionYear");
    const getPrice = document.getElementById("price");
    const getColor = document.getElementById("color");
    const getSize = document.getElementById("size");

    const name = getName.value.trim();
    const productionYear = parseInt(getProductionYear.value);
    const price = parseInt(getPrice.value);
    const color = parseInt(getColor.value);
    const size = parseInt(getSize.value);

    if (!name || !productionYear || !price || !color || !size) {
        alert("Please fill in all fields properly!");
        return;
    }

    res.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

    res.send(
        JSON.stringify({
            "name": name,
            "production_year": productionYear,
            "price": price,
            "color": color,
            "size": size
        })
    );

    getName.value = "";
    getProductionYear.value = "";
    getPrice.value = "";
    getColor.value = "";
    getSize.value = "";

    // END CODE HERE
}