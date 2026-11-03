const chatForm = document.getElementById("chatForm");
const messageInput = document.getElementById("messageInput");
const chatArea = document.getElementById("chatArea");
const sendButton = document.getElementById("sendButton");

function addMessage(message, sender) {
    const wrapper = document.createElement("div");
    wrapper.className = `message ${sender}-message`;

    if (sender === "assistant") {
        const avatar = document.createElement("div");
        avatar.className = "message-avatar";
        avatar.textContent = "✧";
        wrapper.appendChild(avatar);
    }

    const content = document.createElement("div");
    content.className = "message-content";

    const author = document.createElement("span");
    author.className = "message-author";
    author.textContent = sender === "assistant" ? "ExpenseFlow AI" : "You";

    const paragraph = document.createElement("p");
    paragraph.textContent = message;

    content.append(author, paragraph);
    wrapper.appendChild(content);

    chatArea.appendChild(wrapper);
    chatArea.scrollTop = chatArea.scrollHeight;

    return wrapper;
}

async function sendMessage(message) {
    const cleanMessage = message.trim();

    if (!cleanMessage || sendButton.disabled) return;

    addMessage(cleanMessage, "user");
    messageInput.value = "";
    sendButton.disabled = true;
    sendButton.textContent = "Thinking...";

    const loading = document.createElement("div");
    loading.className = "typing";
    loading.textContent = "ExpenseFlow AI is analysing your request...";
    chatArea.appendChild(loading);
    chatArea.scrollTop = chatArea.scrollHeight;

    try {
        const response = await fetch("/api/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: cleanMessage })
        });

        const result = await response.json();

        loading.remove();

        if (!response.ok) {
            throw new Error(result.error || "The request could not be completed.");
        }

        addMessage(
            result.response || "The assistant returned an empty response.",
            "assistant"
        );
    } catch (error) {
        loading.remove();
        addMessage(
            error.message || "Something went wrong. Please try again.",
            "assistant"
        );
    } finally {
        sendButton.disabled = false;
        sendButton.innerHTML = 'Send <span>↑</span>';
        messageInput.focus();
    }
}

chatForm.addEventListener("submit", function(event) {
    event.preventDefault();
    sendMessage(messageInput.value);
});

document.querySelectorAll(".suggestion").forEach(button => {
    button.addEventListener("click", () => {
        sendMessage(button.dataset.message);
    });
});
