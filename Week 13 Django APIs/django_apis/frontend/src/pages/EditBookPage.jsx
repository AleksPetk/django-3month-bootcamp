import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import { getBook, updateBook } from "../api/books";

function EditBookPage() {
    const { bookId } = useParams();
    const navigate = useNavigate();

    const [formData, setFormData] = useState({
        title: "",
        author: "",
        pages: "",
    });

    const [loading, setLoading] = useState(true);
    const [submitting, setSubmitting] = useState(false);
    const [error, setError] = useState("");

    useEffect(() => {
        async function loadBook() {
            try {
                const data = await getBook(bookId);

                setFormData({
                    title: data.book.title,
                    author: data.book.author,
                    pages: data.book.pages,
                });
            } catch (error) {
                setError(error.message);
            } finally {
                setLoading(false);
            }
        }

        loadBook();
    }, [bookId]);

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
        setSubmitting(true);

        const bookData = {
            title: formData.title,
            author: formData.author,
            pages: Number(formData.pages),
        };

        try {
            await updateBook(bookId, bookData);
            navigate(`/books/${bookId}`);
        } catch (error) {
            setError(error.message);
        } finally {
            setSubmitting(false);
        }
    }

    if (loading) {
        return <p>Loading book...</p>;
    }

    return (
        <section>
            <h1>Edit Book</h1>

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
                    {submitting ? "Saving..." : "Save Changes"}
                </button>
            </form>
        </section>
    );
}

export default EditBookPage;