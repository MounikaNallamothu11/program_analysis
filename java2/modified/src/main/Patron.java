package main;

import java.util.ArrayList;
import java.util.List;

public class Patron {
    private String name;
    private List<Book> borrowedBooks;

    public Patron(String name) {
        this.name = name;
        this.borrowedBooks = new ArrayList<>();
    }

    public String getName() {
        return name;
    }

    public void borrowBook(Book book) {
        book.checkOut();
        borrowedBooks.add(book);
    }

    public void returnBook(Book book) {
        if (borrowedBooks.contains(book)) {
            book.returnBook();
        }
    }

    public List<Book> getBorrowedBooks() {
        return borrowedBooks;
    }
}
