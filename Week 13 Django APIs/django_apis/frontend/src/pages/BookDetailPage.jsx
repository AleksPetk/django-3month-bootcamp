import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";

import { deleteBook, getBook } from "../api/books";

function BookDetailPage() {
    const { bookId } = useParams();
    const navigate = useNavigate();

    const [book, setBook] = useState(null);
    const [loading, setLoading] = useState(true);
    const [deleting, setDeleting] = useState(false);
    const [error, setError] = useState("");

    useEffect(() => {
        async function loadBook() {
            try {
                const data = await getBook(bookId);
                setBook(data.book);
            } catch (error) {
                setError(error.message);
            } finally {
                setLoading(false);
            }
        }

        loadBook();
    }, [bookId]);

    async function handleDelete() {
        const confirmed = window.confirm(
            `Are you sure you want to delete "${book.title}"?`
        );

        if (!confirmed) {
            return;
        }

        setError("");
        setDeleting(true);

        try {
            await deleteBook(bookId);
            navigate("/books");
        } catch (error) {
            setError(error.message);
            setDeleting(false);
        }
    }

    if (loading) {
        return <p>Loading book...</p>;
    }

    if (error && !book) {
        return (
            <section>
                <p className="error-message">{error}</p>

                <Link to="/books">Back to Books</Link>
            </section>
        );
    }

    if (!book) {
        return <p>Book not found.</p>;
    }

    return (
        <section className="book-detail">
            <h1>{book.title}</h1>

            {error && (
                <p className="error-message">
                    {error}
                </p>
            )}

            <p>
                <strong>Author:</strong> {book.author}
            </p>

            <p>
                <strong>Pages:</strong> {book.pages}
            </p>

            <div className="detail-actions">
                <Link
                    className="edit-button"
                    to={`/books/${book.id}/edit`}
                >
                    Edit Book
                </Link>

                <button
                    className="delete-button"
                    type="button"
                    onClick={handleDelete}
                    disabled={deleting}
                >
                    {deleting ? "Deleting..." : "Delete Book"}
                </button>

                <Link
                    className="back-button"
                    to="/books"
                >
                    Back to Books
                </Link>
            </div>
        </section>
    );
}

export default BookDetailPage;