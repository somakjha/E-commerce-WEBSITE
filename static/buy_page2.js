function show_interest(evt,uid,seller_id,item_id,title_key) {
    console.log(uid)
    console.log(seller_id)
    console.log(item_id)
    firebase.database().ref('/interests_shown').child(uid).push({
        0:0,
        1:item_id,
        2:seller_id,
        3:0,
        4:title_key
    })
    .then((snap) => {
        const key = snap.key 
        console.log(key);
        firebase.database().ref("/interests_received").child(seller_id).child(key).set({
            0:0,
            1:item_id,
            2:uid,
            3:0,
            4:title_key
        });
        var alertDiv = document.createElement("div");
        alertDiv.className = "alert alert-success alert-dismissible fade show";
        alertDiv.setAttribute("role", "alert");
        var pTag = document.createElement("h6");
        pTag.innerHTML = "<strong>Congrats! Interest showed Successfully</strong>";
        alertDiv.appendChild(pTag);
        var closeButton = document.createElement("button");
        closeButton.setAttribute("type", "button");
        closeButton.id = "closeButton";
        closeButton.className = "close";
        closeButton.setAttribute("data-dismiss", "alert");
        closeButton.setAttribute("aria-label", "Close");
        closeButton.onclick= function() {
            const myNode = document.getElementById("showAlert");
            while (myNode.firstChild) {
              myNode.removeChild(myNode.lastChild);
            }
        }
        var spanArea = document.createElement("span");
        spanArea.setAttribute("aria-hidden", "true");
        spanArea.innerHTML = "&times;";
        closeButton.appendChild(spanArea);
        alertDiv.appendChild(closeButton);

        var showAlert = document.getElementById("showAlert");
        showAlert.appendChild(alertDiv);
    });
}