import main.Book;
import main.Library;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class LibraryTest {

    @Test
    public void testAddBookToLibrary() {
        Library library = new Library();
        Book book = new Book("1984", "George Orwell");
        library.addBook(book);

        assertNotNull(library.findBookByTitle("1984"));
        assertEquals("George Orwell", library.findBookByTitle("1984").getAuthor());
    }

    @Test
    public void testFindBookByTitleNotFound() {
        Library library = new Library();
        Book book = new Book("1984", "George Orwell");
        library.addBook(book);

        assertNull(library.findBookByTitle("The Great Gatsby"));
    }
}
