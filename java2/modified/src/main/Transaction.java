package main;

public class Transaction {
    private Patron patron;
    private Book book;
    private boolean isCheckout;

    public Transaction(Patron patron, Book book, boolean isCheckout) {
System.out.println("CALL Transaction.Transaction");
System.out.println("CALL Transaction.Transaction");
System.out.println("CALL Transaction.Transaction");
System.out.println("CALL Transaction.Transaction");
        this.patron = patron;
        this.book = book;
        this.isCheckout = isCheckout;
    }

    public void process() {
System.out.println("CALL Transaction.process");
System.out.println("CALL Transaction.process");
System.out.println("CALL Transaction.process");
System.out.println("CALL Transaction.process");
        patron.borrowBook(book);
    }
}
