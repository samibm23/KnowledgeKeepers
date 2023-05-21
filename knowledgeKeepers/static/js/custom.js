// next prev
var now = 0; // currently shown div
var thint;
var numOfMistakes = 0;
var res = "top"
var sol = "Your Solution";
function GenerateImage() {
    $("#btn1").remove();
    $("#loader").show();
    $("#loading_doodle").show();
    var prompt = $('h3.eng').text();
    var data = {
  "prompt":prompt ,
  "n": 1,
  "size": "512x512"
};
    $.ajax({
      type: 'POST',
      url: 'https://api.openai.com/v1/images/generations',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'API KEY:Bearer',
      },
      data: JSON.stringify(data),
      success: function(response) {
        if (typeof response === 'string') {
            // Parse the JSON string to an object
            response = JSON.parse(response);
        }
        console.log(response);
        var firstUrl = response.data[0].url;
        $("#loading_doodle").hide();
        $("#loader").css("background-image",'url('+firstUrl+')');
        
      },
      error: function(error) {
        console.log(error);
      }
    });
  }
function GenerateStable() {
    $("#btn2").remove();
    $("#loader2").show();
    $("#loading_doodle2").show();
    var pmpt = $('h3.eng').text();
    var url = '/test/';
    const data = {
      prompt:'ultra realistic close up of ' + pmpt + ', symmetrical balance, in-frame, 8K',
    };
    $.ajax({
      type: "POST",
      url: "/test/",
      data: data,
      beforeSend: function(xhr, settings) {
          xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
      },
      success: function(response) {
        console.log('Response:', data);
        if (typeof response === 'string') {
          // Parse the JSON string to an object
          response = JSON.parse(response);
      }
      console.log(response);
      var firstUrl = response.output[0];
      $("#loading_doodle2").hide();
      $("#loader2").css("background-image",'url('+firstUrl+')');
        // Handle the response here
      },
      error: function(xhr, status, error) {
          console.log(error);
      }});
  }



  function chatCompletions(data) {
    $('.loadingresult').css('display', 'grid');
    prmpt = document.getElementById('inp').value;
    console.log(prmpt);
  var data = {
    "model": "gpt-3.5-turbo","messages":
    [    { role: "user", content: "You will tell if a student's answer to a mathematical problem is right or wrong given the problem and the 2 answers (the real one) and the user given one" },
    { role: "assistant", content: "Okay" },
    { role: "user", content: "the problem : Kara bought 32 tickets for a movie for $ 7200. What is the cost of each ticket? The student's answer to it : 225 , The real answer is :$ 225" },
    { role: "assistant", content: "Yes the student was correct , To solve this problem we need to divide the 7200$ by the 32 tickets she bought and the result will be $7200/32 = $225" },
    { role: "user", content: "the problem : Kara bought 32 tickets for a movie for $ 7200. What is the cost of each ticket? The student's answer to it : 7200/32 = 225, The real answer is :$ 225" },
    { role: "assistant", content: "Yes the student was correct , To solve this problem we need to divide the 7200$ by the 32 tickets she bought and the result will be $7200/32 = $225" },
    { role: "user", content: "the problem : Kara bought 32 tickets for a movie for $ 7200. What is the cost of each ticket? The student's answer to it : 220, The real answer is :$ 225" },
    { role: "assistant", content: "No the student was not correct , To solve this problem we need to divide the 7200$ by the 32 tickets she bought and the result will be $7200/32 = $225" },
  {"role": "user",
                "content":"the problem :"+$("#gett").text()+" The student's answer to it :" +prmpt + " The real answer is :'"+document.getElementById('Answer').value
 }]};

 console.log("the request : "+ "the problem :"+$("#gett").text()+" The student's answer to it :" +prmpt + " The real answer is :'"+document.getElementById('Answer').value);
 return new Promise(function(resolve, reject) {
$.ajax({
type: 'POST',
url: 'https://api.openai.com/v1/chat/completions',
headers: {
'Content-Type': 'application/json',
'Authorization': 'API KEY:Bearer ',
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

function validate() {
  if(document.getElementById('inp').value===""){
    document.getElementById('inp').setCustomValidity("Please enter a value");
    document.getElementById('inp').reportValidity();
    return;
  }else{
    chatCompletions()
    .then(function(response) {
        $('#2').addClass('result_page_show');
      // Response is available here
      if (response.choices[0].message.content.toLowerCase().includes("is correct")||response.choices[0].message.content.toLowerCase().startsWith("yes")||response.choices[0].message.content.toLowerCase().startsWith("yes")) {
        console.log("Input string starts with 'yes'");
        if (language=="arabic"){
          $("#thefb").text("صحيح");
        }else{
        $("#thefb").text("Correct !");
      }
        const files = ["giphy (1).gif", "giphy (4).gif", "giphy.gif"]
        const randomIndex = Math.floor(Math.random() * files.length);
        const randomFile = files[randomIndex];
        const imagePath = STATIC_URL + "yes/" + randomFile;
        $("#res").attr("src", imagePath);
        fetch('/addpoints/')
        .then(response => response.json())
        .then(data =>{var h3Element = document.getElementById("currency_test");

        // Change the text content of the H3 element
        h3Element.textContent = data.new_val+ " ∯";
        // Get the input element
        var inputElement = document.getElementById("currency");
        
        // Change the value of the input element
        inputElement.value = data.new_val;
        console.log(data);
        sendHistory();
        $("#back").hide();
        $("#next").show();
        $("#Similar").show();
        numOfMistakes=0;
      
      
      } )
        .catch(error => console.error(error));
        //increase the Math currency
      } else {
        numOfMistakes+=1;
        if (language=="arabic"){
          $("#numOfMistakes").text((numOfMistakes+1)+"/3 : عدد المحاولات");
        }else if (language=="french"){
          $("#numOfMistakes").text("Nombre de tentatives : "+(numOfMistakes+1)+"/3")
        }
        else{
          $("#numOfMistakes").text("Number of tries : "+(numOfMistakes+1)+"/3")
      }
        
        $("#next").hide();
        $("#Similar").hide();
        if(numOfMistakes>2){
          res = "bad"
          
          $("#next").toggle();
          $("#Similar").toggle();
          $("#back").hide();
          const text = response.choices[0].message.content;
          const toIndex = text.indexOf("To");
          const result = text.substring(toIndex);
          console.log(result);
          var tt ="";
          if (language=="arabic"){
            tt = "عذرًا، خطأ";
          }else if (language=="french"){
            tt = "Désolé, erreur";
          }
          else{
            tt = "Sorry Wrong";
        }
          $("#thefb").html("<p>"+ tt +"</p><p>" + result + "</p>");
          console.log(result);
          sol = result
          sendHistory();
          $("#res").remove();
          numOfMistakes=0;
        }else{
          console.log("Input string does not start with 'yes'");
          if (language=="arabic"){
            $("#thefb").text("عذرًا، خطأ")
          }else if (language=="french"){
            $("#thefb").text("Désolé, erreur")
          }
          else{
            $("#thefb").text("Sorry Wrong")
        }
          
          
          const files = ["giphy (1).gif", "giphy (2).gif", "giphy.gif", "giphy (3).gif"]
          const randomIndex = Math.floor(Math.random() * files.length);
          const randomFile = files[randomIndex];
          const imagePath = STATIC_URL + "no/" + randomFile;
          console.log(imagePath);
          $("#res").attr("src", imagePath);
        }
        
        
      }
      console.log(response);
    })
    .catch(function(error) {
      console.log(error);
    });
         
  }
 
  }
//show active step
function showActiveStep()
{
    if ($('#step1').is(':visible'))
    {
        $(".step-bar .bar .fill").eq(now).addClass('w-100');
        $("#activeStep").html('1');
    }
    else if ($('#step2').is(':visible'))
    {
        $(".step-bar .bar .fill").eq(now).addClass('w-100');
        $("#activeStep").html('2');
    }
    else if ($('#step3').is(':visible'))
    {
        $(".step-bar .bar .fill").eq(now).addClass('w-100');
        $("#activeStep").html('3');
    }
    else if ($('#step4').is(':visible'))
    {
        $(".step-bar .bar .fill").eq(now).addClass('w-100');
        $("#activeStep").html('4');
    }
    else if ($('#step5').is(':visible'))
    {
        $(".step-bar .bar .fill").eq(now).addClass('w-100');
        $("#activeStep").html('5');
    }
    else
    {
    console.log("error");
    }
}


function next()
{
    divs.eq(now).hide();
    now = (now + 1 < divs.length) ? now + 1 : 0;
    divs.eq(now).show(); // show next
    console.log(now);

    showActiveStep();
}


function sendHistory(){
  if (!(thint==="yes")){
    thint="no";
  }
  const data = { // the data you want to send in the request body
    solution: sol,
    answer: document.getElementById('inp').value,
    result: res,
    num: numOfMistakes,
    hint: thint
    
  }
  
  
  fetch('/history/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken'),
    },
    body: JSON.stringify(data) // convert data to JSON string
  })
  .then(response => {
    if (response.ok) {
      return response.json(); // convert response to JSON format
    } else {
      throw new Error('Network response was not ok.');
    }
  })
  .then(data => {
    console.log(data); // handle the response data
  })
  .catch(error => {
    console.error('There was a problem with the fetch operation:', error);
  });
}