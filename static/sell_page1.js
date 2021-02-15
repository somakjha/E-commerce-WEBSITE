function updateSellAD(uid, parentKey, oldTitle){
    oldTitle = oldTitle.toLowerCase();
    var desc = document.getElementById("desc2");
    var price = document.getElementById("price2");
    firebase.database().ref("/sell").child(uid).child(parentKey).update({
        1:desc.value,
        4:price.value
    }).then((snap) => {
        var x = event.currentTarget;
        var alertDiv = document.createElement("div");
        alertDiv.className = "alert alert-success alert-dismissible fade show";
        alertDiv.setAttribute("role", "alert");
        var pTag = document.createElement("h6");
        pTag.innerHTML = "<strong> Changes saved successfully</strong>";
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

        window.location.reload(false);
    });
}