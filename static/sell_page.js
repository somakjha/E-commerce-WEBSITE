function upload(uid,full_name){
    var title=document.getElementById("title")
    var description=document.getElementById("description")
    var price=document.getElementById("price")
    const ref=firebase.storage().ref();
    const file=document.getElementById("customFile").files[0];
    console.log(file)
    const name=new Date()+'-'+file.name;
    const metaData={
        contentType:file.type
    }
    const task=ref.child(name).put(file,metaData);
    task
    .then(snapshot => snapshot.ref.getDownloadURL())
    .then(url => {

        firebase.database().ref("/images").push({
            0:url,
            1:title.value
        });
        firebase.database().ref("/sell").child(uid).push({
            0:title.value,
            1:description.value,
            2:full_name,
            3:url,
            4:price.value,
            5:0
        })
        .then((snap) => {
            const key = snap.key 
            console.log(key);
            firebase.database().ref("/titles").child(document.getElementById("title").value.toLowerCase()).push({
                0:uid,
                1:key
            });
        window.location.reload(false);
         });
    });
}