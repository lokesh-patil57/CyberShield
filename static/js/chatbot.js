document.addEventListener('DOMContentLoaded', function() {
    const toggleChat = document.getElementById('toggle-chat');
    const chatBody = document.querySelector('.chatbot-body');
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendMessage = document.getElementById('send-message');

    toggleChat.addEventListener('click', function() {
        chatBody.style.display = chatBody.style.display === 'none' ? 'flex' : 'none';
    });

    function addMessage(message, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `chat-message ${isUser ? 'user-message' : 'bot-message'}`;
        messageDiv.style.margin = '5px';
        messageDiv.style.padding = '10px';
        messageDiv.style.borderRadius = '10px';
        messageDiv.style.backgroundColor = isUser ? '#007bff' : '#f1f1f1';
        messageDiv.style.color = isUser ? 'white' : 'black';
        messageDiv.style.alignSelf = isUser ? 'flex-end' : 'flex-start';
        messageDiv.style.maxWidth = '80%';
        messageDiv.textContent = message;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    async function sendToBot(message) {
        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: message })
            });
            const data = await response.json();
            return data.response;
        } catch (error) {
            console.error('Error:', error);
            return 'Sorry, I encountered an error. Please try again.';
        }
    }

    sendMessage.addEventListener('click', async function() {
        const message = userInput.value.trim();
        if (message) {
            addMessage(message, true);
            userInput.value = '';
            userInput.disabled = true;
            sendMessage.disabled = true;
            
            const response = await sendToBot(message);
            addMessage(response);
            
            userInput.disabled = false;
            sendMessage.disabled = false;
        }
    });

    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage.click();
        }
    });

    // Initial greeting
    addMessage('Hello! I'm your cybersecurity assistant. How can I help you today?');
});
