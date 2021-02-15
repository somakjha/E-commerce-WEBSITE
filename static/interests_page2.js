function changeStatus(evt, status, uid, parentKey,showerId,productId,sell_lease_key,title_key) {
    console.log(evt.currentTarget);
    var x = evt.currentTarget.parentElement;
    console.log(x);
    var y=x.parentElement;
    x.remove();
    var newspanItem = document.createElement("span");
    newspanItem.className="response101";

    console.log(parentKey)
    var received_interestToChange=firebase.database().ref("/interests_received").child(uid).child(parentKey);
    var shown_interestToChange=firebase.database().ref("/interests_shown").child(showerId).child(parentKey);
    //var add_msg_Received=firebase.database().ref("/messages");
    if (status=="accepted") 
    {
        newspanItem.innerHTML="Interest Accepted";
        received_interestToChange.update({
            0:1,
        });
        
        shown_interestToChange.update({
            0:1,
        });
        console.log(typeof uid)
        console.log(uid)
        firebase.database().ref("/messages").child(uid).child(showerId).push({
            0:"You can chat with me now (This is an auto generated message)",
            1:Date.now(),
            2:uid
        });

        firebase.database().ref("/messages").child(showerId).child(uid).push({
            0:"You can chat with me now (This is an auto generated message)",
            1:Date.now(),
            2:showerId
        });

        var sell_lease=0;
        if (sell_lease_key==='Lessor :') {
            sell_lease=1;
        }
        firebase.database().ref("/confirmations_shipped").child(uid).push({
            0:0,
            1:productId,
            2:showerId,
            3:sell_lease,
            4:title_key
        });



    }
    else {

        newspanItem.innerHTML="Interest Rejected";
        received_interestToChange.update({
            0:-1
        })

        shown_interestToChange.update({
            0:-1,
        });
    }
    y.appendChild(newspanItem);
}