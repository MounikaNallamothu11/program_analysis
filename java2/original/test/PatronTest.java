import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class PatronTest {

    @Test
    public void testPatronCreation() {
        Patron patron = new Patron("John Doe");
        assertEquals("John Doe", patron.getName());
    }

    @Test
    public void testBorrowBook() {
        Library library = new Library();
        Book book = new Book("1984", "George Orwell");
        library.addBook(book);
        Patron patron = new Patron("John Doe");

        patron.borrowBook(book);
        assertTrue(book.isCheckedOut());
        assertTrue(patron.getBorrowedBooks().contains(book));
    }

    @Test
    public void testReturnBook() {
        Library library = new Library();
        Book book = new Book("1984", "George Orwell");
        library.addBook(book);
        Patron patron = new Patron("John Doe");

        patron.borrowBook(book);
        patron.returnBook(book);
        assertFalse(book.isCheckedOut());
        assertFalse(patron.getBorrowedBooks().contains(book));
    }

    @Test
    public void testReturnBookNotBorrowed() {
        Library library = new Library();
        Book book = new Book("1984", "George Orwell");
        library.addBook(book);
        Patron patron = new Patron("John Doe");

        patron.returnBook(book); // Book is not borrowed yet
        assertFalse(book.isCheckedOut());
    }
}