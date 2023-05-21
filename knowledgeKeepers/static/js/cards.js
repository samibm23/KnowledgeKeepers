function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

function onLoad(){
  var cards = document.querySelectorAll('.card');
  document.getElementById("focused").focus();
  cards.forEach(function(card) {
  card.addEventListener('click', function() {
  var tabindex = this.getAttribute('tabindex');
  let avatarImg = document.getElementById("photo");
  let miniphoto = document.getElementById("mini-photo");
  
  
    const data = {
      id:tabindex,
    };
    $.ajax({
      type: "POST",
      url: "/avatar_collection/",
      data: data,
      beforeSend: function(xhr, settings) {
          xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
      },
      success: function(response) {
          console.log(response);
          const blob = new Blob([response.svg], { type: 'image/svg+xml' });
          const url = URL.createObjectURL(blob);
           avatarImg.src = url
           miniphoto.src = url
      },
      error: function(xhr, status, error) {
          console.log(error);
      }
  });
      });});}

      function showPopup() {
        if (document.getElementById("currency").value<5){
        
        document.getElementById("popup").style.display = "block";
      }else{
        window.location.href = '/avatar/';
      }
      }
      
      function hidePopup() {
        document.getElementById("popup").style.display = "none";
      }
      
      
      
      