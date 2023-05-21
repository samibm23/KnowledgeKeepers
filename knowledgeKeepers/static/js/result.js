function hint(){
    $('.loadingresult').css('display', 'grid');
    var data = {
          "model": "gpt-3.5-turbo","messages":
                  [{"role": "user",
                  "content": "Give me hint for this mathimatical problem without solving it , The problem is: ' "+$('h3.eng').text() +" give hint in "+language
    }]             };
    return new Promise(function(resolve, reject) {
        $.ajax({
        type: 'POST',
        url: 'https://api.openai.com/v1/chat/completions',
        headers: {
        'Content-Type': 'application/json',
        'Authorization': 'API KEY :Bearer ',
        },
        data: JSON.stringify(data),
        success: function(response) {
          resolve(response);
        },
        error: function(error) {
          reject(error);
        }
        });
        });
        }

function showresult()
{
    
    hint().then(function(response) {
            thint="yes";
            console.log(thint);
            $('#1').addClass('result_page_show');
          // Response is available here
            console.log(response.choices[0].message.content);
            $("#thehint").text(response.choices[0].message.content)
       
          
          console.log(response);
        })
        .catch(function(error) {
          console.log(error);
        });
};

function hideresult()
{
    setTimeout(function()
    {
        $('.loadingresult').removeAttr("style");
        $('.result_page').removeClass('result_page_show');
       

    },30)
};

function showpop() {         
    $.ajax({
url: '/whiteboard/',
method: 'GET',
success: function(response) {
  // Open a new window with the response from the Django function
  var popupWindow = window.open('', '_blank','width=900,height=800');
  popupWindow.document.write(response);
  window.addEventListener("message", function(event) {
    if (event.origin !== window.location.origin) {
      // Message is not from this origin
      return;
    }
    console.log(event.data);
    // Handle the message received from the pop-up window
    $("#inp").val(event.data);
  }, false);
}
});
};


function record() {

    $("#record-button").removeClass("fas fa-microphone");
    $("#record-button").addClass("fas fa-stop");
        $.ajax({
              url: '/speech_to_text/',
              type: 'POST',
              dataType: 'json',
              data: {
              },
              success: function(response) {
                // handle success response
                console.log(response);
                $("#record-button").removeClass("fas fa-stop");
                $("#record-button").addClass("fas fa-microphone");
                $("#inp").val(response.text_en);
              },
              error: function(xhr, status, error) {
                // handle error response
                console.log(error);
              }
            });
    
}

function text_to_audio(){
        console.log($('#PROB').text());
        $.ajax({
            url: '/text-to-speech/', // Replace with your Django function URL
            type: 'POST',
            data: {
      'text': $('#PROB').text(),
  },

            success: function(response) {
                // Handle successful AJAX response
                console.log('Audio played successfully!');
            },
            error: function(response) {
                // Handle AJAX errors
                console.log('Error playing audio:', response);
            }
        });
    }
function logout(){
  window.location.href = '/login/'
}
        

