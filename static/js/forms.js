function clearFields(event){
    let input_fields = document.querySelectorAll('input, textarea');
    for(let i = 0; i < input_fields.length;i++){
        input_fields[i].value = '';
    }
}

async function registerUser(event) {
    event.preventDefault()
    let user_email = document.getElementById('user_email');
    let user_password = document.getElementById('user_reg_password')
    await fetch('http://127.0.0.1:8000/auth/register', {
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
    })
}

async function loginUser(event) {
    event.preventDefault()
    let user_email = document.getElementById('user_email');
    let user_password = document.getElementById('user_reg_password')
    await fetch('http://127.0.0.1:8000/auth/login', {
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
        else {

        }
    })
}
