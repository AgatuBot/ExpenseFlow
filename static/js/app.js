const chatForm = document.getElementById("chatForm");
const messageInput = document.getElementById("messageInput");
const chatArea = document.getElementById("chatArea");
const sendButton = document.getElementById("sendButton");

function showView(viewName) {
    const validViews = ["overview", "assistant", "policy"];
    const target = validViews.includes(viewName) ? viewName : "overview";

    document.querySelectorAll(".view").forEach(view => {
        const isActive = view.id === target;
        view.classList.toggle("active", isActive);
        view.hidden = !isActive;
    });

    document.querySelectorAll(".nav-item").forEach(link => {
        const isActive = link.dataset.view === target;
        link.classList.toggle("active", isActive);
        if (isActive) {
            link.setAttribute("aria-current", "page");
        } else {
            link.removeAttribute("aria-current");
        }
    });

    const title = document.getElementById(target).dataset.pageTitle;
    document.getElementById("pageTitle").textContent = title;
    const breadcrumb = document.getElementById("breadcrumbCurrent");
    if (breadcrumb) breadcrumb.textContent = title;
    window.scrollTo({ top: 0, behavior: "smooth" });

    if (target === "assistant") {
        setTimeout(() => messageInput.focus(), 150);
    }
}

document.querySelectorAll("[data-view]").forEach(link => {
    link.addEventListener("click", event => {
        event.preventDefault();
        const view = link.dataset.view;
        history.replaceState(null, "", `#${view}`);
        showView(view);
    });
});

document.querySelectorAll("[data-go]").forEach(button => {
    button.addEventListener("click", () => {
        const view = button.dataset.go;
        history.replaceState(null, "", `#${view}`);
        showView(view);
    });
});

window.addEventListener("hashchange", () => {
    showView(window.location.hash.replace("#", ""));
});

function addMessage(message, sender) {
    const wrapper = document.createElement("div");
    wrapper.className = `message ${sender}-message`;

    if (sender === "assistant") {
        const avatar = document.createElement("img");
        avatar.className = "message-avatar";
        avatar.src = "/static/images/agatubot-logo.jpg";
        avatar.alt = "AgatuBot";
        wrapper.appendChild(avatar);
    }

    const content = document.createElement("div");
    content.className = "message-content";

    const author = document.createElement("span");
    author.className = "message-author";
    author.textContent = sender === "assistant" ? "ExpenseFlow Assistant" : "You";

    const body = document.createElement("div");
    body.className = "message-body";

    if (sender === "assistant") {
        if (window.marked && window.DOMPurify) {
            body.innerHTML = DOMPurify.sanitize(marked.parse(message));
        } else {
            body.textContent = message;
        }
    } else {
        const paragraph = document.createElement("p");
        paragraph.textContent = message;
        body.appendChild(paragraph);
    }

    content.append(author, body);
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
    loading.textContent = "ExpenseFlow is preparing a response...";
    chatArea.appendChild(loading);
    chatArea.scrollTop = chatArea.scrollHeight;

    try {
        const response = await fetch("/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: cleanMessage })
        });

        const result = await response.json();
        loading.remove();

        if (!response.ok) {
            throw new Error(result.error || "The request could not be completed.");
        }

        addMessage(result.response || "The assistant returned an empty response.", "assistant");
    } catch (error) {
        loading.remove();
        addMessage(error.message || "Something went wrong. Please try again.", "assistant");
    } finally {
        sendButton.disabled = false;
        sendButton.innerHTML = 'Send <span>↑</span>';
        messageInput.focus();
    }
}

chatForm.addEventListener("submit", event => {
    event.preventDefault();
    sendMessage(messageInput.value);
});

document.querySelectorAll(".suggestion").forEach(button => {
    button.addEventListener("click", () => sendMessage(button.dataset.message));
});

showView(window.location.hash.replace("#", "") || "overview");
