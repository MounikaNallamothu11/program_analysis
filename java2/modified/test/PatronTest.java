import main.Book;
import main.Library;
import main.Patron;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class PatronTest {

    @Test
    public void testPatronCreation() {
System.out.println("CALL PatronTest.testPatronCreation");
System.out.println("CALL PatronTest.testPatronCreation");
System.out.println("CALL PatronTest.testPatronCreation");
System.out.println("CALL PatronTest.testPatronCreation");
        Patron patron = new Patron("John Doe");
        assertEquals("John Doe", patron.getName());
    }

    @Test
    public void testBookCreation() {
System.out.println("CALL PatronTest.testBookCreation");
System.out.println("CALL PatronTest.testBookCreation");
System.out.println("CALL PatronTest.testBookCreation");
System.out.println("CALL PatronTest.testBookCreation");
        Book book = new Book("Animal Farm", "George Orwell");
        assertEquals("George Orwell", book.getAuthor());
    }

    @Test
    public void testBorrowBook() {
System.out.println("CALL PatronTest.testBorrowBook");
System.out.println("CALL PatronTest.testBorrowBook");
System.out.println("CALL PatronTest.testBorrowBook");
System.out.println("CALL PatronTest.testBorrowBook");
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
System.out.println("CALL PatronTest.testReturnBook");
System.out.println("CALL PatronTest.testReturnBook");
System.out.println("CALL PatronTest.testReturnBook");
System.out.println("CALL PatronTest.testReturnBook");
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
System.out.println("CALL PatronTest.testReturnBookNotBorrowed");
System.out.println("CALL PatronTest.testReturnBookNotBorrowed");
System.out.println("CALL PatronTest.testReturnBookNotBorrowed");
System.out.println("CALL PatronTest.testReturnBookNotBorrowed");
        Library library = new Library();
        Book book = new Book("1984", "George Orwell");
        library.addBook(book);
        Patron patron = new Patron("John Doe");

        patron.returnBook(book); // main.Book is not borrowed yet
        assertFalse(book.isCheckedOut());
    }
}
