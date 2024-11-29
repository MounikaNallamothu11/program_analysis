import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class TransactionTest {

    @Test
    public void testProcessCheckoutTransaction() {
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
        Library library = new Library();
        Book book = new Book("1984", "George Orwell");
        library.addBook(book);
        Patron patron = new Patron("John Doe");

        Transaction transaction = new Transaction(patron, book, false); // Trying to return without borrowing
        transaction.process();

        assertFalse(book.isCheckedOut());
    }

    @Test
    public void testCheckoutAndReturn() {
        Library library = new Library();
        Book book = new Book("1984", "George Orwell");
        library.addBook(book);
        Patron patron = new Patron("John Doe");

        Transaction checkoutTransaction = new Transaction(patron, book, true);
        checkoutTransaction.process();
        assertTrue(book.isCheckedOut());

        Transaction returnTransaction = new Transaction(patron, book, false);
        returnTransaction.process();
        assertFalse(book.isCheckedOut());
    }

    @Test
    public void testCheckoutUnavailableBook() {
        Library library = new Library();
        Book book = new Book("1984", "George Orwell");
        library.addBook(book);
        Patron patron = new Patron("John Doe");

        book.checkOut(); // Manually mark as checked out
        Transaction transaction = new Transaction(patron, book, true);
        assertTrue(book.isCheckedOut());
    }
}
