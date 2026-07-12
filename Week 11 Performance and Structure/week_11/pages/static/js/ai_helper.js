document.addEventListener("DOMContentLoaded", () => {
    const toggleButton = document.querySelector("#ai-helper-toggle");
    const closeButton = document.querySelector("#ai-helper-close");
    const panel = document.querySelector("#ai-helper-panel");
    const form = document.querySelector("#ai-helper-form");
    const input = document.querySelector("#ai-helper-input");
    const messages = document.querySelector("#ai-helper-messages");

    if (!toggleButton || !closeButton || !panel || !form || !input || !messages) {
        return;
    }

    toggleButton.addEventListener("click", () => {
        panel.classList.add("is-open");
        input.focus();
    });

    closeButton.addEventListener("click", () => {
        panel.classList.remove("is-open");
    });

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const message = input.value.trim();

        if (!message) {
            return;
        }

        addMessage(message, "user");
        input.value = "";

        const thinkingMessage = addMessage("Thinking...", "bot");

        try {
            const response = await fetch(form.dataset.url, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCsrfToken(),
                    "X-Requested-With": "XMLHttpRequest",
                },
                body: JSON.stringify({ message: message }),
            });

            const data = await response.json();

            if (!response.ok || !data.success) {
                thinkingMessage.textContent = data.error || "Sorry, I could not answer that.";
                return;
            }

            thinkingMessage.textContent = data.answer;
        } catch (error) {
            thinkingMessage.textContent = "Sorry, something went wrong. Please try again.";
        }
    });

    function addMessage(text, sender) {
        const messageElement = document.createElement("div");
        messageElement.classList.add("ai-helper-message");
        messageElement.classList.add(`ai-helper-message-${sender}`);
        messageElement.textContent = text;

        messages.append(messageElement);
        messages.scrollTop = messages.scrollHeight;

        return messageElement;
    }

    function getCsrfToken() {
        const csrfInput = form.querySelector("[name=csrfmiddlewaretoken]");

        if (csrfInput) {
            return csrfInput.value;
        }

        return getCookie("csrftoken");
    }

    function getCookie(name) {
        let cookieValue = null;

        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");

            for (let cookie of cookies) {
                cookie = cookie.trim();

                if (cookie.startsWith(name + "=")) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }

        return cookieValue;
    }
});
