(() => {
    "use strict";

    const assistant = document.querySelector("[data-website-assistant]");
    if (!assistant) {
        return;
    }

    const panel = assistant.querySelector("#website-assistant-panel");
    const toggle = assistant.querySelector("[data-assistant-toggle]");
    const closeButton = assistant.querySelector("[data-assistant-close]");
    const form = assistant.querySelector("[data-assistant-form]");
    const input = assistant.querySelector("[data-assistant-input]");
    const submitButton = assistant.querySelector("[data-assistant-submit]");
    const messages = assistant.querySelector("[data-assistant-messages]");
    const csrfToken = form.querySelector("[name=csrfmiddlewaretoken]").value;
    const endpoint = assistant.dataset.endpoint;
    const clientTimeoutMilliseconds = 15000;
    const conversation = [];

    const setPanelOpen = (isOpen) => {
        panel.hidden = !isOpen;
        panel.setAttribute("aria-hidden", String(!isOpen));
        toggle.setAttribute("aria-expanded", String(isOpen));
        assistant.classList.toggle("website-assistant--open", isOpen);

        if (isOpen) {
            window.setTimeout(() => input.focus(), 50);
        } else {
            toggle.focus();
        }
    };

    const addMessage = (text, type) => {
        const message = document.createElement("div");
        message.className = `website-assistant__message website-assistant__message--${type}`;
        message.textContent = text;
        messages.appendChild(message);
        messages.scrollTop = messages.scrollHeight;
        return message;
    };

    toggle.addEventListener("click", () => {
        setPanelOpen(panel.hidden);
    });

    closeButton.addEventListener("click", () => setPanelOpen(false));

    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape" && !panel.hidden) {
            setPanelOpen(false);
        }
    });

    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        const question = input.value.trim();
        if (!question || submitButton.disabled) {
            return;
        }

        addMessage(question, "user");
        const recentHistory = conversation.slice(-4);
        conversation.push({role: "user", content: question});
        input.value = "";
        input.disabled = true;
        submitButton.disabled = true;
        const waitingMessage = addMessage("Thinking...", "waiting");
        const controller = new AbortController();
        const timeout = window.setTimeout(
            () => controller.abort(),
            clientTimeoutMilliseconds,
        );

        try {
            const response = await fetch(endpoint, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken,
                },
                body: JSON.stringify({question, history: recentHistory}),
                signal: controller.signal,
            });
            const data = await response.json();
            waitingMessage.remove();

            if (!response.ok) {
                addMessage(data.error || "The helper could not answer right now.", "error");
            } else {
                addMessage(data.answer, "helper");
                conversation.push({role: "assistant", content: data.answer});
            }
        } catch (error) {
            waitingMessage.remove();
            const message = error.name === "AbortError"
                ? "The helper took too long to answer. Please try again."
                : "The helper could not connect. Please try again later.";
            addMessage(message, "error");
        } finally {
            window.clearTimeout(timeout);
            input.disabled = false;
            submitButton.disabled = false;
            input.focus();
        }
    });
})();
