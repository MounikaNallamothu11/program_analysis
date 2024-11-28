package main;

public class Book {
    private String title;
    private String author;
    private boolean isCheckedOut;

    public Book(String title, String author) {
System.out.println("CALL Book.Book");
System.out.println("CALL Book.Book");
System.out.println("CALL Book.Book");
System.out.println("CALL Book.Book");
        this.title = title;
        this.author = author;
        this.isCheckedOut = false;
    }

    public String getTitle() {
System.out.println("CALL Book.getTitle");
System.out.println("CALL Book.getTitle");
System.out.println("CALL Book.getTitle");
System.out.println("CALL Book.getTitle");
        return title;
    }

    public String getAuthor() {
System.out.println("CALL Book.getAuthor");
System.out.println("CALL Book.getAuthor");
System.out.println("CALL Book.getAuthor");
System.out.println("CALL Book.getAuthor");
        return author;
    }

    public boolean isCheckedOut() {
System.out.println("CALL Book.isCheckedOut");
System.out.println("CALL Book.isCheckedOut");
System.out.println("CALL Book.isCheckedOut");
System.out.println("CALL Book.isCheckedOut");
        return isCheckedOut;
    }

    public void checkOut() {
System.out.println("CALL Book.checkOut");
System.out.println("CALL Book.checkOut");
System.out.println("CALL Book.checkOut");
System.out.println("CALL Book.checkOut");
        isCheckedOut = true;
    }

    public void returnBook() {
System.out.println("CALL Book.returnBook");
System.out.println("CALL Book.returnBook");
System.out.println("CALL Book.returnBook");
System.out.println("CALL Book.returnBook");
        isCheckedOut = false;
    }
}
