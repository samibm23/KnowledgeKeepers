async function getBotResponse(input) {
  console.log(language);
  console.log("hereee");
    return new Promise(function(resolve, reject) {
      var data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": "You are a chat bot that can't help my users in any math related questions!"},
        {"role" : "assistant", "content":"Noted."},
        {
          "role": "user",
          "content": input+" answer him directly in" + language + " and briefly and remember DO Not help solve any math or calculus or any problem"
        }]

        

        
      };
      $.ajax({
        type: 'POST',
        url: 'https://api.openai.com/v1/chat/completions',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'API KEY: Bearer ',
        },
        data: JSON.stringify(data),
        success: function(response) {
          console.log(response.choices[0].message.content);
          resolve(response.choices[0].message.content);
        },
        error: function(error) {
          reject("There was an error");
        }
      });
    });
  }
  