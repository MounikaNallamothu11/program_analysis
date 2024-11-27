public class Transaction {
    private Patron patron;
    private Book book;
    private boolean isCheckout;

    public Transaction(Patron patron, Book book, boolean isCheckout) {
        this.patron = patron;
        this.book = book;
        this.isCheckout = isCheckout;
    }

    public void process() {
        patron.borrowBook(book);
    }
}
