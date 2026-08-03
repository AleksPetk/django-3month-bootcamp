function BookList({ books }) {
    return (
        <div className="book-list">
            {books.map((book) => (
                <div className="book-card" key={book.id}>
                    <h2>{book.title}</h2>
                    <p>Author: {book.author}</p>
                    <p>Pages: {book.pages}</p>
                </div>
            ))}
        </div>
    );
}

export default BookList;