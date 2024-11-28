package main;

import java.util.ArrayList;
import java.util.List;

public class Patron {
    private String name;
    private List<Book> borrowedBooks;

    public Patron(String name) {
System.out.println("CALL Patron.Patron");
System.out.println("CALL Patron.Patron");
System.out.println("CALL Patron.Patron");
System.out.println("CALL Patron.Patron");
        this.name = name;
        this.borrowedBooks = new ArrayList<>();
    }

    public String getName() {
System.out.println("CALL Patron.getName");
System.out.println("CALL Patron.getName");
System.out.println("CALL Patron.getName");
System.out.println("CALL Patron.getName");
        return name;
    }

    public void borrowBook(Book book) {
System.out.println("CALL Patron.borrowBook");
System.out.println("CALL Patron.borrowBook");
System.out.println("CALL Patron.borrowBook");
System.out.println("CALL Patron.borrowBook");
        book.checkOut();
        borrowedBooks.add(book);
    }

    public void returnBook(Book book) {
System.out.println("CALL Patron.returnBook");
System.out.println("CALL Patron.returnBook");
System.out.println("CALL Patron.returnBook");
System.out.println("CALL Patron.returnBook");
        if (borrowedBooks.contains(book)) {
            book.returnBook();
        }
    }

    public List<Book> getBorrowedBooks() {
        return borrowedBooks;
    }
}
