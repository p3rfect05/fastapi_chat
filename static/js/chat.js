async function sendMessage(event) {
    event.preventDefault()
    var input = document.getElementById("messageText")
    let chat_id = window.location.pathname.split('/')[2];
    ws.send(JSON.stringify({'client_id' : client_id, 'chat_id': chat_id, 'text' : input.value}))
    

    console.log(input.value)

         input.value = ''
    
}




var ws = new WebSocket(`ws://localhost:8000/chat/ws/${client_id}`);

 ws.onmessage = function(event) {
    console.log('ws message', JSON.parse(event.data));
    let data = JSON.parse(event.data);

    let message_div = document.createElement('div');
    //message_div.classList = ['message align-items-center row justify-content-end'];

    let text_message = document.createElement('div');  
    text_message.classList = ['text_message col-3'];

    let avatar_div = document.createElement('div');
    avatar_div.classList = ['message_avatar col-1'];

    let avatar_img = document.createElement('img');
    avatar_img.src = '../static/img/4242-kapibara-4.jpg';
    avatar_div.appendChild(avatar_img);

    let message_author = document.createElement('span');
    message_author.classList.add('message_author');
    message_author.innerText = data['email'];

    let message_content = document.createElement('span');
    message_content.classList.add('message_content');
    message_content.innerText = data['text'];

    let message_date = document.createElement('span');
    message_date.classList.add('message_date');
    message_date.innerText = data['time_created'];
    console.log(client_id, data.time_created)
    if(client_id === data['user_id']){
        text_message.classList.add('text_me');
        text_message.appendChild(message_author);
        text_message.appendChild(message_content);
        text_message.appendChild(message_date);
        message_div.appendChild(text_message);
        message_div.appendChild(avatar_div);
        message_div.classList = ['message align-items-center row justify-content-end'];
    }
    else {
        text_message.classList.add('text_friend');
        message_div.appendChild(avatar_div);
        text_message.appendChild(message_author);
        text_message.appendChild(message_content);
        text_message.appendChild(message_date);
        message_div.appendChild(text_message);
        message_div.classList = ['message align-items-center row justify-content-start'];
        
    };

    let message_window = document.querySelector('.message_window');
    message_window.appendChild(message_div);

    
 };


