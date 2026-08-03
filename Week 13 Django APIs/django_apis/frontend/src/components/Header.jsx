import { NavLink } from "react-router-dom";

function Header() {
    return (
        <header className="header">
            <h1>Japan 47 Book Store</h1>

            <nav>
                <NavLink
                    to="/"
                    className={({ isActive }) =>
                        isActive ? "nav-link active" : "nav-link"
                    }
                >
                    Home
                </NavLink>

                <NavLink
                    to="/books"
                    className={({ isActive }) =>
                        isActive ? "nav-link active" : "nav-link"
                    }
                >
                    Books
                </NavLink>

                <NavLink
                    to="/books/create"
                    className={({ isActive }) =>
                        isActive ? "nav-link active" : "nav-link"
                    }
                >
                    Create Book
                </NavLink>
            </nav>
        </header>
    );
}

export default Header;