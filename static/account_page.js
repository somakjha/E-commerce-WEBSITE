function changePassword(email){
    firebase.auth().sendPasswordResetEmail(
        email).then(function() {
          alert('A password reset link has been sent to your registered email!');
        })
        .catch(function(error) {
          // Error occurred. Inspect error.code.
    });
}