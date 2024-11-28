package main;

import java.util.HashMap;
import java.util.Map;

public class Library {
    private Map<String, Book> books;

    public Library() {
System.out.println("CALL Library.Library");
System.out.println("CALL Library.Library");
System.out.println("CALL Library.Library");
System.out.println("CALL Library.Library");
        books = new HashMap<>();
    }

    public void addBook(Book book) {
System.out.println("CALL Library.addBook");
System.out.println("CALL Library.addBook");
System.out.println("CALL Library.addBook");
System.out.println("CALL Library.addBook");
        String title = book.getTitle();
        books.put(title, book);
    }

    public Book findBookByTitle(String title) {
System.out.println("CALL Library.findBookByTitle");
System.out.println("CALL Library.findBookByTitle");
System.out.println("CALL Library.findBookByTitle");
System.out.println("CALL Library.findBookByTitle");
        return books.get(title);
    }
}
