function changeStatus(evt, status, uid, parentKey,toFromId,productId,sell_lease_key,title_key,title) {
    console.log(evt.currentTarget);
    var x = evt.currentTarget.parentElement;
    console.log(x);
    var y=x.parentElement;
    y.parentElement.remove();


    if (status=="shipped") {

        firebase.database().ref("/confirmations_shipped").child(uid).child(parentKey).update({
            0:1
        });

        var sell_lease=0;
        if (sell_lease_key==='Lessor :') {
            sell_lease=1;
        }
        firebase.database().ref("/confirmations_received").child(toFromId).child(parentKey).set({
            0:0,
            1:productId,
            2:uid,
            3:sell_lease,
            4:title_key
        });
        
        
    }
    else if (status=="not_shipped") {

        firebase.database().ref("/confirmations_shipped").child(uid).child(parentKey).update({
            0:-1
        });

        var sell_lease=0;
        if (sell_lease_key==='Lessor :') {
            sell_lease=1;
        }
        firebase.database().ref("/confirmations_received").child(toFromId).child(parentKey).set({
            0:-1,
            1:productId,
            2:uid,
            3:sell_lease,
            4:title_key
        });

    }
    else if (status=="received") {

        firebase.database().ref("/confirmations_received").child(uid).child(parentKey).update({
            0:1
        });

        if(sell_lease_key == "Seller :"){
            firebase.database().ref("/sell").child(toFromId).child(productId).update({
                5:1
            });
        } 
        else{  
            firebase.database().ref("/lease").child(toFromId).child(productId).update({
                5:1
            });
        }

        
        currentTime=String(new Date()).replace(" GMT+0530 (India Standard Time)","");
        console.log(currentTime)

        var buy_sell_rent_lease=1;
        if (sell_lease_key==='Lessor :') {
            buy_sell_rent_lease=3;
        }
        firebase.database().ref("/all_transactions").child(uid).push({
            0:currentTime,
            1:productId,
            2:toFromId,
            3:buy_sell_rent_lease
        });
        firebase.database().ref("/all_transactions").child(toFromId).push({
            0:currentTime,
            1:productId,
            2:uid,
            3:buy_sell_rent_lease+1
        });

        var low_title=title.toLowerCase()
        console.log(low_title)
        if(buy_sell_rent_lease==1){
            console.log("buy_sale working")
            console.log(title_key)
            firebase.database().ref("/titles").child(low_title).child(title_key).remove()
        }
        else{
            console.log("rent_lease working")
            firebase.database().ref("/lease_titles").child(low_title).child(title_key).remove()
        }
        
    }
    else {

        firebase.database().ref("/confirmations_received").child(uid).child(parentKey).update({
            0:-1
        });

        firebase.database().ref("/confirmations_shipped").child(toFromId).child(parentKey).update({
            0:-1,
        });
    }

}