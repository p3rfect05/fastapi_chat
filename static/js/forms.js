function clearFields(event){
    let input_fields = document.querySelectorAll('input, textarea');
    for(let i = 0; i < input_fields.length;i++){
        input_fields[i].value = '';
    }
}
function validatePassword(password){
    let isAlpha = function(ch){
      return typeof ch === "string" && ch.length === 1
             && (ch >= "a" && ch <= "z" || ch >= "A" && ch <= "Z");
    }
    console.log(password, password.length);
    if(password.length < 8)
        return false;
    for(let i = 0;i < password.length;i++){
        if(!(isAlpha(password[i]) || (password[i] >= '0' && password[i] <= '9')))
            return false

    }
    return true;
}
function createError(error_class, error_message) {
    let div = document.createElement('div');
    div.innerText = error_message;
    div.style.color = 'red';
    div.style.margin = '10px';
    div.classList = error_class;
    div.style.fontSize = '20px';
    div.style.textAlign = 'center';
    div.style.fontWeight = '600'
    let buttons = document.querySelector('.form_buttons');
    buttons.before(div);
}
async function registerUser(event) {
    event.preventDefault()
    let user_email = document.getElementById('user_email');
    let user_password = document.getElementById('user_reg_password');
    const validateEmail = (email) => {
  return email.match(
    /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
  );
};
    if(!validateEmail(user_email.value)) {
        if (!document.querySelector('.invalid_email'))
            createError('invalid_email', 'Invalid email')
        return;
    }
    if(!validatePassword(user_password.value)) {
        if (!document.querySelector('.invalid_password'))
            createError('invalid_password', 'Wrong password format')
        return;
    }

    await fetch('http://localhost:7777/auth/register', {
        method: 'POST',
        body: JSON.stringify({'email' : user_email.value, 'password' : user_password.value}),
        headers: {
            'Content-Type' : 'application/json'
        }
    }
    ).then(response => {
        console.log(response.status)
        if(response.status === 200){
            window.location.replace('/chat/profile')
        }
        else if (response.status === 422) {
            if(!document.querySelector('.submit_input_error'))
                createError('submit_input_error', 'Invalid email');
        }
        else if (response.status === 403) {
            if(!document.querySelector('.submit_input_error'))
                createError('already_exists_input_error', 'User already exists');
        }
        else {
            if(!document.querySelector('.server_input_error'))
                createError('server_input_error', 'Server error');
        }
    })
}

async function loginUser(event) {
    event.preventDefault()
    let user_email = document.getElementById('user_email');
    let user_password = document.getElementById('user_reg_password')
    await fetch('http://localhost:7777/auth/login', {
        method: 'POST',
        body: JSON.stringify({'email' : user_email.value, 'password' : user_password.value}),
        headers: {
            'Content-Type' : 'application/json'
        }
    }
    ).then(response => {

        if(response.status === 200){
            window.location.replace('/chat/profile')
        }
        else if (response.status === 401) {
            if(!document.querySelector('.invalid_credentials'))
                createError('invalid_credentials', 'Incorrect email or password');
        }
        else if (response.status === 422) {
            if(!document.querySelector('.submit_input_error'))
                createError('submit_input_error', 'Invalid email');
        }
        else {
            if(!document.querySelector('.server_input_error'))
                createError('server_input_error', 'Server error');
        }
    })
}
