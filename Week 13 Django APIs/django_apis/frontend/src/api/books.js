const API_BASE_URL = import.meta.env.VITE_API_URL;

export async function getBooks() {
    const response = await fetch(`${API_BASE_URL}/api/books/`);

    if (!response.ok) {
        throw new Error("Could not load books.");
    }

    return response.json();
}

export async function getBook(bookId) {
    const response = await fetch(
        `${API_BASE_URL}/api/books/${bookId}/`
    );

    if (!response.ok) {
        throw new Error("Could not load this book.");
    }

    return response.json();
}

export async function createBook(bookData) {
    const response = await fetch(
        `${API_BASE_URL}/api/books/create/`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(bookData),
        }
    );

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.error || "Could not create book.");
    }

    return data;
}
export async function updateBook(bookId, bookData) {
    const url = `${API_BASE_URL}/api/books/${bookId}/`;

    const response = await fetch(url, {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(bookData),
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.error || "Could not update book.");
    }

    return data;
}


export async function deleteBook(bookId) {
    const url = `${API_BASE_URL}/api/books/${bookId}/`;

    const response = await fetch(url, {
        method: "DELETE",
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.error || "Could not delete book.");
    }

    return data;
}