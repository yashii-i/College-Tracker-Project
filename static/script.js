const userInput = document.getElementById('name');
const sendButton = document.getElementById('send-btn');
const chatbot = document.getElementById('chat-box');


sendButton.addEventListener('click',function() {
let messageText = userInput.value;
console.log("This user wants to know about: ", messageText);
fetch('/chat', {
    method:'POST',
    headers: {  'Content-Type': 'application/json'},
    body: JSON.stringify({message: messageText})
})
.then((response => response.json()))
.then(serverData => {
    console.log("The dictionary returned from Python!!: ", serverData.data);
    const reply = document.createElement('p');
    reply.textContent = JSON.stringify(serverData.data);
    chatbot.appendChild(reply);
});
});




