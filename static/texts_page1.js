var userid;
var fromid;
var combinedMessages = []
var chatWith = "";
var myName = "";
var count = 0;
var globalVar = {};
var count1 = 1;
var currid;
var t;
var prevLength;
function call(id, uid) {
    
    chatWith = "";
    myName = "";
    combinedMessages = [];
    count = 0;
    userid = uid;
    fromid = id;
    count1 = 1;
    globalVar.id = id;
    globalVar.uid = uid;
    
    var messagesBySessionUser = firebase.database().ref("/messages").child(uid).child(id);
    var messageFromClickedPerson = firebase.database().ref("/messages").child(id).child(uid);
    
    var userName = firebase.database().ref("/userId").child(id);
    var myNamefromDB = firebase.database().ref("/userId").child(uid);
    
    userName.on('value', (snapshot) =>{
        const data = snapshot.val();
        chatWith = data["fName"];
        globalVar.chatWith = chatWith;
        document.getElementById("chatperson").innerHTML = chatWith;
    });
    
    myNamefromDB.on('value', (snapshot) =>{
        const data = snapshot.val();
        myName = data["fName"];
        globalVar.myName = myName;
    });
    
    messagesBySessionUser.on('value', gotData, errData);
    messageFromClickedPerson.on('value', gotData, errData);
    
    if(currid != id){
        currid = id;
    }

    t=setInterval(function(){ 
        var check2 = firebase.database().ref("/messages").child(id).child(uid);
        var newLength = 0;
        var data2;
        var data2_keys;
        check2.on('value', (snapshot) =>{
            data2 = snapshot.val();
            data2_keys=Object.keys(data2)
            newLength = data2_keys.length;
        });

        lastKey=data2_keys[newLength - 1];
        var newMsg = data2[lastKey][0];
        console.log(newMsg);
        
        if(newLength > prevLength && currid==id){

            var x = document.getElementById("chatHistory");
            var newListItem = document.createElement("li");
            var upperDiv = document.createElement("div");
            upperDiv.className = "message-data";
            var newSpan = document.createElement("span");
            newSpan.innerHTML = String(new Date(data2[lastKey][1])).replace("GMT+0530 (India Standard Time)","") + chatWith;
            newSpan.style.color = "white";
            var newDiv = document.createElement("div");
            newListItem.appendChild(upperDiv);
            upperDiv.appendChild(newSpan);
            newDiv.className = "message my-message";
            newDiv.innerHTML = newMsg;
            newDiv.style.fontFamily = "'Lato', Arial, sans-serif";
            newListItem.appendChild(newDiv);

            x.appendChild(newListItem);
            var el = document.getElementById("scrollArea");
            el.scrollTop = 10000000000000;
            prevLength = newLength;
        }
    }, 1000);

}

function gotData(data){
    var tempData = data.val();
    console.log(tempData);
    var keys = Object.keys(tempData);
    
    for(var i = 0; i < keys.length; i++){
        var k = keys[i];
        combinedMessages.push(tempData[k]);
        
    }
    count++;
    if(count === 2){
        prevLength = 0;
        prevLength = keys.length;
        call2(combinedMessages);
    }
}

function call2(combinedMessages){
    

    combinedMessages.sort(function(a,b){
        return a[1] - b[1];
      });
    
    try{
        var start = document.getElementById("chatStart");
        start.remove();
    }
    catch(err){

    }

    var scrollArea = document.getElementById("scrollArea");

    var newX = document.createElement("ul");
    newX.setAttribute("id", "chatHistory");
    scrollArea.appendChild(newX);

    var x = document.getElementById("chatHistory");

    for(var i = 0; i < combinedMessages.length; i++){
        if(combinedMessages[i][2] === userid){
            var newListItem = document.createElement("li");
            newListItem.className = "clearfix";

            var upperDiv = document.createElement("div");
            var newSpan = document.createElement("span");
            newSpan.innerHTML = String(new Date(combinedMessages[i][1])).replace("GMT+0530 (India Standard Time)","") + ", " + myName;
            newSpan.style.color = "white";
            upperDiv.className = "message-data align-right";
            var newDiv = document.createElement("div");
            newListItem.appendChild(upperDiv);
            newDiv.className = "message other-message float-right";
            newDiv.innerHTML = combinedMessages[i][0];
            newDiv.style.fontFamily = "'Lato', Arial, sans-serif";
            upperDiv.appendChild(newSpan);
            newListItem.appendChild(newDiv);

            x.appendChild(newListItem);
        }else{
            var newListItem = document.createElement("li");
            var upperDiv = document.createElement("div");
            upperDiv.className = "message-data";
            var newSpan = document.createElement("span");
            newSpan.innerHTML = String(new Date(combinedMessages[i][1])).replace("GMT+0530 (India Standard Time)","") + ", " + chatWith;
            newSpan.style.color = "white";
            var newDiv = document.createElement("div");
            newListItem.appendChild(upperDiv);
            upperDiv.appendChild(newSpan);
            newDiv.className = "message my-message";
            newDiv.innerHTML = combinedMessages[i][0];
            newDiv.style.fontFamily = "'Lato', Arial, sans-serif";
            newListItem.appendChild(newDiv);

            x.appendChild(newListItem);
        }
    }
    
    var el = document.getElementById("scrollArea");
    el.scrollTop = 10000000000000;
}

function errData(err){
    console.log("Error");
    console.log(err);
}
