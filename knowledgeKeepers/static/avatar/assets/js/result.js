function showresult()
{
    $('.loadingresult').css('display', 'grid');

    setTimeout(function()
    {
        $('.result_page').addClass('result_page_show');

    },1000)
};

        
        
//correct answers
var correct_answers = ['Hong Kong','All of the above','Zoroastrianism','Gen. K.M. Cariappa', 'Zinc'];

// user answers
let correct = 0;

var steps = $('section').length;



console.log(steps);
function countresult(resultnumber)
{
    $('#step'+resultnumber+' .radio-field input').each(function()
    {
        for(var i = 0; i<=correct_answers.length; i++)
        {
            if($(this).is(':checked'))
        {
            if($(this).val() == correct_answers[i])
            {
                
    
                correct++;

                break;
    
            }
        }
        }
    
    })

    var correctprcnt = correct / steps * 100;

    $('.u_prcnt').html(correctprcnt + '%');
    $('.u_result span').html(correctprcnt + ' Points');

    if(correctprcnt >=80)
    {
        $('.pass_check').html('<i class="fa-solid fa-check"></i> You Passed!');
        $('.result_msg').html('You passed the test!');
    }
}
