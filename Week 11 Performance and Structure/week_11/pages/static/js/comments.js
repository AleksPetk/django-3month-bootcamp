document.addEventListener("DOMContentLoaded", () => {
    console.log("comments.js loaded v2");

    const forms = document.querySelectorAll(".comment-form");

    forms.forEach((form) => {
        form.addEventListener("submit", async (event) => {
            event.preventDefault();

            const postId = form.dataset.postId;
            const url = form.dataset.url;
            const formData = new FormData(form);

            const response = await fetch(url, {
                method: "POST",
                body: formData,
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                },
            });

            if (!response.ok) {
                alert("Could not add comment.");
                return;
            }

            const data = await response.json();

            addCommentToPage(postId, data);
            form.reset();
        });
    });
});

function addCommentToPage(postId, data) {
    const commentsList = document.querySelector(`#comments-list-${postId}`);
    const noComments = document.querySelector(`#no-comments-${postId}`);

    if (!commentsList) {
        return;
    }

    if (noComments) {
        noComments.remove();
    }

    const commentCard = document.createElement("div");
    commentCard.classList.add("comment-card");
    commentCard.id = `comment-card-${data.comment_id}`;

    const author = document.createElement("strong");
    author.textContent = data.author;

    const createdAt = document.createElement("span");
    createdAt.textContent = data.created_at;

    const content = document.createElement("p");
    content.textContent = data.content;

    commentCard.append(author, createdAt, content);

    if (data.can_edit) {
        const editButton = document.createElement("button");
        editButton.type = "button";
        editButton.classList.add("comment-edit-btn");
        editButton.dataset.url = data.edit_url;
        editButton.textContent = "Edit";
        commentCard.append(editButton);
    }

    if (data.can_delete) {
        const deleteButton = document.createElement("button");
        deleteButton.type = "button";
        deleteButton.classList.add("comment-delete-btn");
        deleteButton.dataset.url = data.delete_url;
        deleteButton.dataset.commentId = data.comment_id;
        deleteButton.textContent = "Delete";
        commentCard.append(deleteButton);
    }

    commentsList.prepend(commentCard);
}

// DELETE COMMENT

document.addEventListener("click", async (event) => {
    const button = event.target.closest(".comment-delete-btn");

    if (!button) {
        return;
    }

    event.preventDefault();

    const commentCard = button.closest(".comment-card");
    const url = button.dataset.url;

    if (!url) {
        alert("Delete URL is missing. Please refresh the page.");
        return;
    }

    const response = await fetch(url, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "X-Requested-With": "XMLHttpRequest",
        },
    });

    if (!response.ok) {
        alert("Could not delete comment.");
        return;
    }

    const data = await response.json();

    if (data.success) {
        commentCard.remove();
    }
});
function getCookie(name) {
    let cookieValue = null;

    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");

        for (let cookie of cookies) {
            cookie = cookie.trim();

            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                );
                break;
            }
        }
    }

    return cookieValue;
}

// EDIT COMMENT

document.addEventListener("click", (event) => {
    const button = event.target.closest(".comment-edit-btn");

    if (!button) {
        return;
    }

    event.preventDefault();

    const commentCard = button.closest(".comment-card");
    const commentText = commentCard.querySelector("p");
    const url = button.dataset.url;

    if (!url) {
        alert("Edit URL is missing. Please refresh the page.");
        return;
    }

    const oldContent = commentText.textContent.trim();

    const textarea = document.createElement("textarea");
    textarea.classList.add("comment-edit-textarea");
    textarea.value = oldContent;

    const saveBtn = document.createElement("button");
    saveBtn.type = "button";
    saveBtn.classList.add("comment-save-btn");
    saveBtn.textContent = "Save";

    const cancelBtn = document.createElement("button");
    cancelBtn.type = "button";
    cancelBtn.classList.add("comment-cancel-btn");
    cancelBtn.textContent = "Cancel";

    commentText.replaceChildren(textarea, saveBtn, cancelBtn);

    cancelBtn.addEventListener("click", () => {
        commentText.textContent = oldContent;
    });

    saveBtn.addEventListener("click", async () => {
        const formData = new FormData();
        formData.append("content", textarea.value);

        const response = await fetch(url, {
            method: "POST",
            body: formData,
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
                "X-Requested-With": "XMLHttpRequest",
            },
        });

        if (!response.ok) {
            alert("Could not edit comment.");
            return;
        }

        const data = await response.json();

        if (data.success) {
            commentText.textContent = data.content;
        }
    });
});
