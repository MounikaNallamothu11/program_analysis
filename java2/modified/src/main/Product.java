package main;

public class Product {
    private String name;
    private int quantity;
    private double price;

    public Product(String name, int quantity, double price) {
System.out.println("CALL Product.Product");
System.out.println("CALL Product.Product");
System.out.println("CALL Product.Product");
System.out.println("CALL Product.Product");
        this.name = name;
        this.quantity = quantity;
        this.price = price;
    }

    public String getName() {
System.out.println("CALL Product.getName");
System.out.println("CALL Product.getName");
System.out.println("CALL Product.getName");
System.out.println("CALL Product.getName");
        return name;
    }

    public int getQuantity() {
System.out.println("CALL Product.getQuantity");
System.out.println("CALL Product.getQuantity");
System.out.println("CALL Product.getQuantity");
System.out.println("CALL Product.getQuantity");
        return quantity;
    }

    public double getPrice() {
System.out.println("CALL Product.getPrice");
System.out.println("CALL Product.getPrice");
System.out.println("CALL Product.getPrice");
System.out.println("CALL Product.getPrice");
        return price;
    }
}
