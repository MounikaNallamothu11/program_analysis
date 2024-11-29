import java.util.HashMap;
import java.util.Map;

public class Library {
    private Map<String, Book> books;

    public Library() {
        books = new HashMap<>();
    }

    public void addBook(Book book) {
        String title = book.getTitle();
        books.put(title, book);
    }

    public Book findBookByTitle(String title) {
        return books.get(title);
    }
}