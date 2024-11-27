import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class BookTest {

    @Test
    public void testBookCreation() {
        Book book = new Book("1984", "George Orwell");
        assertEquals("1984", book.getTitle());
        assertEquals("George Orwell", book.getAuthor());
    }

    @Test
    public void testCheckOutAndReturn() {
        Book book = new Book("1984", "George Orwell");
        assertFalse(book.isCheckedOut());
        book.checkOut();
        assertTrue(book.isCheckedOut());
        book.returnBook();
        assertFalse(book.isCheckedOut());
    }
}
