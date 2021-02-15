function updateLeaseAD(uid, parentKey, oldTitle){
    oldTitle = oldTitle.toLowerCase();
    var desc = document.getElementById("desc2");
    var price = document.getElementById("price2");
    firebase.database().ref("/lease").child(uid).child(parentKey).update({
        1:desc.value,
        4:price.value
    })
    .then((snap) => {
        window.location.reload(false);
    });
}