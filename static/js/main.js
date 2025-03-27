// Chat functionality
const chatForm = document.getElementById('chat-form');
const chatMessages = document.getElementById('chat-messages');
const loadingSpinner = document.querySelector('.loading-spinner');

function scrollToBottom() {
    if (chatMessages) {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
}

// Add hover animation to cards
document.querySelectorAll('.card').forEach(card => {
    card.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-5px)';
    });

    card.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0)';
    });
});

// Handle chat form submission if it exists
if (chatForm) {
    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const messageInput = chatForm.querySelector('input[type="text"]');
        const message = messageInput.value.trim();

        if (message) {
            if (loadingSpinner) loadingSpinner.style.display = 'block';
            messageInput.value = '';

            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ message })
                });

                const data = await response.json();
                if (chatMessages) {
                    chatMessages.innerHTML += `
                        <div class="message user-message">${message}</div>
                        <div class="message bot-message">${data.response}</div>
                    `;
                    scrollToBottom();
                }
            } catch (error) {
                console.error('Error:', error);
            } finally {
                if (loadingSpinner) loadingSpinner.style.display = 'none';
            }
        }
    });
}

// Add smooth scroll animation to all internal links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});