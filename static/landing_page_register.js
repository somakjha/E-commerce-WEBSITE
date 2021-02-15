function checkPassAndConPass(){
    var password = document.getElementById("pass");
    var conPass = document.getElementById("conPass");

    // console.log(password.value);
    // console.log(conPass.value);
    // console.log(conPassLength);

    if(conPass.value != password.value){
        document.getElementById("message").innerHTML= "<span style='color:#fc0303'>Password and confirm password not matching</span>";
        document.getElementById("Register").disabled = true;
    }
    else
    if(conPass.value === password.value){
        document.getElementById("message").innerHTML= "<span style='color:#03fc28'>Password and confirm password matching</span>";
        document.getElementById("Register").disabled = false;
    }
}
