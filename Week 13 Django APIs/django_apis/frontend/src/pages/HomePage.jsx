import { Link } from "react-router-dom";

function HomePage() {
    return (
        <section>
            <h1>Welcome to the Book Store</h1>

            <p>
                This website uses React for the frontend and Django
                for the backend.
            </p>

            <Link to="/books">Browse Books</Link>
        </section>
    );
}

export default HomePage;