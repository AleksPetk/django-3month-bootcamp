import { Route, Routes } from "react-router-dom";

import Layout from "./components/Layout";
import HomePage from "./pages/HomePage";
import BooksPage from "./pages/BooksPage";
import BookDetailPage from "./pages/BookDetailPage";
import CreateBookPage from "./pages/CreateBookPage";
import EditBookPage from "./pages/EditBookPage"

import "./App.css";

function App() {
    return (
        <Layout>
            <Routes>
                <Route path="/" element={<HomePage />} />

                <Route
                    path="/books"
                    element={<BooksPage />}
                />

                <Route
                    path="/books/create"
                    element={<CreateBookPage />}
                />

                <Route
                    path="/books/:bookId"
                    element={<BookDetailPage />}
                />
                <Route
                    path="/books/:bookId/edit"
                    element={<EditBookPage />}
                />
            </Routes>
        </Layout>
    );
}

export default App;