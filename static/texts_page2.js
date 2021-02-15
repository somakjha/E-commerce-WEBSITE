function send(){
    var message = document.getElementById("messageToSend").value;
    var id = globalVar.id;
    var uid = globalVar.uid;
    var noofMsg = firebase.database().ref("/messages").child(uid).child(id);
    var size;
    noofMsg.on('value', (snapshot) =>{
        const data = snapshot.val();
        size = Object.keys(data).length;
    });

    size = size + 1;
    firebase.database().ref("/messages").child(uid).child(id).push({
        0 : message,
        1 : Date.now(),
        2 : uid
    });

    var x = document.getElementById("chatHistory");
    console.log(x);
    var newListItem = document.createElement("li");
    newListItem.className = "clearfix";

    var upperDiv = document.createElement("div");
    var newSpan = document.createElement("span");
    newSpan.innerHTML = String(new Date()).replace("GMT+0530 (India Standard Time)","") + ", " + globalVar.myName;
    newSpan.style.color = "white";
    upperDiv.className = "message-data align-right";
    var newDiv = document.createElement("div");
    newListItem.appendChild(upperDiv);
    newDiv.className = "message other-message float-right";
    newDiv.innerHTML = message;
    newDiv.style.fontFamily = "'Lato', Arial, sans-serif";
    upperDiv.appendChild(newSpan);
    newListItem.appendChild(newDiv);

    x.append(newListItem);

    document.getElementById("messageToSend").value = "";
    var el = document.getElementById("scrollArea");
    el.scrollTop = 10000000000000;
    
}