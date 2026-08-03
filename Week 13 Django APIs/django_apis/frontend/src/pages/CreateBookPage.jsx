import { useState } from "react";

import { createBook } from "../api/books";

function CreateBookPage() {
    const [formData, setFormData] = useState({
        title: "",
        author: "",
        pages: "",
    });

    const [error, setError] = useState("");
    const [submitting, setSubmitting] = useState(false);
    const [successMessage, setSuccessMessage] = useState("");

    function handleChange(event) {
        const { name, value } = event.target;

        setFormData((currentData) => ({
            ...currentData,
            [name]: value,
        }));
    }

    async function handleSubmit(event) {
        event.preventDefault();

        setError("");
        setSuccessMessage("");
        setSubmitting(true);

        const bookData = {
            title: formData.title,
            author: formData.author,
            pages: Number(formData.pages),
        };

        try {
            await createBook(bookData);

            setSuccessMessage("Book created successfully!");

            setFormData({
                title: "",
                author: "",
                pages: "",
            });
        } catch (error) {
            setError(error.message);
        } finally {
            setSubmitting(false);
        }
    }

    return (
        <section>
            <h1>Create Book</h1>

            {successMessage && (
                <p className="success-message">
                    {successMessage}
                </p>
            )}

            {error && (
                <p className="error-message">
                    {error}
                </p>
            )}

            <form onSubmit={handleSubmit}>
                <div>
                    <label htmlFor="title">Title</label>

                    <input
                        id="title"
                        name="title"
                        type="text"
                        value={formData.title}
                        onChange={handleChange}
                        required
                    />
                </div>

                <div>
                    <label htmlFor="author">Author</label>

                    <input
                        id="author"
                        name="author"
                        type="text"
                        value={formData.author}
                        onChange={handleChange}
                        required
                    />
                </div>

                <div>
                    <label htmlFor="pages">Number of Pages</label>

                    <input
                        id="pages"
                        name="pages"
                        type="number"
                        min="1"
                        value={formData.pages}
                        onChange={handleChange}
                        required
                    />
                </div>

                <button type="submit" disabled={submitting}>
                    {submitting ? "Creating..." : "Create Book"}
                </button>
            </form>
        </section>
    );
}

export default CreateBookPage;