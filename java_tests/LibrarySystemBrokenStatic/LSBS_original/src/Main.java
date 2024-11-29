public class Main {
    public static void main(String[] args) {
        // Create an instance of the library
        Library library = new Library();
        Book book1 = new Book("The Great Gatsby", "F. Scott Fitzgerald");
        Book book2 = new Book("1984", "George Orwell");
        library.addBook(book1);
        library.addBook(book2);

        // Create a patron
        Patron patron = new Patron("John Doe");

        // Create and process book transactions
        Transaction transaction1 = new Transaction(patron, book1, true); // Checkout
        transaction1.process();

        // Create an order for the patron
        OrderProcessingSystem orderProcessingSystem = new OrderProcessingSystem();
        Product product1 = new Product("The Great Gatsby", 1, 15.99);
        Product product2 = new Product("1984", 1, 12.99);
        orderProcessingSystem.addProductToOrder(product1);
        orderProcessingSystem.addProductToOrder(product2);

        // Generate and print the invoice
        Invoice invoice = orderProcessingSystem.generateInvoice();
        System.out.println(invoice);
    }
}