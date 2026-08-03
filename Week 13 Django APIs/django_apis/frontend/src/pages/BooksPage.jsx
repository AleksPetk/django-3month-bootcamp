import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import { getBooks } from "../api/books";

function BooksPage() {
    const [books, setBooks] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        async function loadBooks() {
            try {
                const data = await getBooks();
                setBooks(data.books);
            } catch (error) {
                setError(error.message);
            } finally {
                setLoading(false);
            }
        }

        loadBooks();
    }, []);

    if (loading) {
        return <p>Loading books...</p>;
    }

    if (error) {
        return <p>{error}</p>;
    }

    return (
        <section>
            <h1>All Books</h1>

            {books.length === 0 ? (
                <p>No books have been added yet.</p>
            ) : (
                <div className="book-list">
                    {books.map((book) => (
                        <article className="book-card" key={book.id}>
                            <h2>{book.title}</h2>
                            <p>Author: {book.author}</p>

                            <Link to={`/books/${book.id}`}>
                                View Details
                            </Link>
                        </article>
                    ))}
                </div>
            )}
        </section>
    );
}

export default BooksPage;