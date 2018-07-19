// Get the modal
var modal = document.getElementById('myModal');

var loginBtn = document.getElementById("loginSubmit");
var registerBtn = document.getElementById("registerSubmit");

modal.style.display = "block";

// When the user clicks on the button, open the modal
loginBtn.onclick = function() {
    modal.style.display = "none";
}
registerBtn.onclick = function() {
    modal.style.display = "none";
}
