function check_pw()
{
    var pw1 = document.getElementById('pw2')
    var pw2 = document.getElementById('pw2')

    var message = document.getElementById('message')
    if(pw1==pw2)
    {
        pw1.setCustomValidity('cool');
        
    }
    else{
        pw1.setCustomValidity('Passwords do not match');
        
    }
    message.innerHTML=Passwords;
}
