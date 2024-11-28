import main.Book;
import main.Library;
import main.Patron;
import main.Transaction;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TransactionTest {

    @Test
    public void testProcessCheckoutTransaction() {
System.out.println("CALL TransactionTest.testProcessCheckoutTransaction");
System.out.println("CALL TransactionTest.testProcessCheckoutTransaction");
System.out.println("CALL TransactionTest.testProcessCheckoutTransaction");
System.out.println("CALL TransactionTest.testProcessCheckoutTransaction");
        Library library = new Library();
        Book book = new Book("1984", "George Orwell");
        library.addBook(book);
        Patron patron = new Patron("John Doe");

        Transaction transaction = new Transaction(patron, book, true); // Checkout transaction
        transaction.process();

        assertTrue(book.isCheckedOut());
        assertTrue(patron.getBorrowedBooks().contains(book));
    }

    @Test
    public void testProcessReturnTransaction() {
System.out.println("CALL TransactionTest.testProcessReturnTransaction");
System.out.println("CALL TransactionTest.testProcessReturnTransaction");
System.out.println("CALL TransactionTest.testProcessReturnTransaction");
System.out.println("CALL TransactionTest.testProcessReturnTransaction");
        Library library = new Library();
        Book book = new Book("1984", "George Orwell");
        library.addBook(book);
        Patron patron = new Patron("John Doe");

        patron.borrowBook(book); // Borrow book first
        Transaction transaction = new Transaction(patron, book, false); // Return transaction
        transaction.process();

        assertFalse(book.isCheckedOut());
        assertFalse(patron.getBorrowedBooks().contains(book));
    }

    @Test
    public void testProcessTransactionNotAllowed() {
System.out.println("CALL TransactionTest.testProcessTransactionNotAllowed");
System.out.println("CALL TransactionTest.testProcessTransactionNotAllowed");
System.out.println("CALL TransactionTest.testProcessTransactionNotAllowed");
System.out.println("CALL TransactionTest.testProcessTransactionNotAllowed");
        Library library = new Library();
        Book book = new Book("1984", "George Orwell");
        library.addBook(book);
        Patron patron = new Patron("John Doe");

        Transaction transaction = new Transaction(patron, book, false); // Trying to return without borrowing
        transaction.process();

        assertFalse(book.isCheckedOut());
    }
}
