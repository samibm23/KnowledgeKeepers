var selectedemail = "";
function showmail(parentmail) {
  console.log(parentmail);
  selectedemail= parentmail;
  console.log(selectedemail);

  // Send a GET request to retrieve the email interface HTML
  fetch('/student_email/', {
    method: 'GET',
  })
    .then(response => response.text())
    .then(html => {
      // Open a new window with the email interface HTML
      var popupWindow = window.open('', '_blank','width=900,height=800');
      popupWindow.document.write(html);
      popupWindow.myValue = selectedemail;

      // Listen for the "message" event from the pop-up window
      window.addEventListener("message", function(event) {

        if (event.origin !== window.location.origin) {
          // Message is not from this origin
          return;
        }
      
        if (event.data == "done") {
          // Handle the "done" message
          // Show a success message or perform any other action
          alert("Email sent successfully!");
        } else if (event.data === "cancel") {
          // Handle the "cancel" message
          // Show a message or perform any other action
          alert("Email sending cancelled.");
        }
      }, false);
    })
    .catch(error => {
      // Handle any errors that occur during the request
      console.error(error);
      // Show an error message or perform any other action
    });
}
