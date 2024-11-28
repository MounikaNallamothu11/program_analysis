package main;

import java.util.ArrayList;
import java.util.List;

public class OrderProcessingSystem {

    private static final double TAX_RATE = 0.08; // 8% tax
    private static final double STANDARD_SHIPPING_COST = 5.0;
    private static final double FREE_SHIPPING_THRESHOLD = 100.0;

    private List<Product> productsInOrder;

    public OrderProcessingSystem() {
System.out.println("CALL OrderProcessingSystem.OrderProcessingSystem");
System.out.println("CALL OrderProcessingSystem.OrderProcessingSystem");
System.out.println("CALL OrderProcessingSystem.OrderProcessingSystem");
System.out.println("CALL OrderProcessingSystem.OrderProcessingSystem");
        this.productsInOrder = new ArrayList<>();
    }

    public void addProductToOrder(Product product) {
System.out.println("CALL OrderProcessingSystem.addProductToOrder");
System.out.println("CALL OrderProcessingSystem.addProductToOrder");
System.out.println("CALL OrderProcessingSystem.addProductToOrder");
System.out.println("CALL OrderProcessingSystem.addProductToOrder");
        productsInOrder.add(product);
    }

    public double calculateSubtotal() {
System.out.println("CALL OrderProcessingSystem.calculateSubtotal");
System.out.println("CALL OrderProcessingSystem.calculateSubtotal");
System.out.println("CALL OrderProcessingSystem.calculateSubtotal");
System.out.println("CALL OrderProcessingSystem.calculateSubtotal");
        double subtotal = 0.0;
        for (Product product : productsInOrder) {
            double price = product.getPrice();
            subtotal += price * product.getQuantity();
        }
        return subtotal;
    }

    public double calculateDiscount() {
System.out.println("CALL OrderProcessingSystem.calculateDiscount");
System.out.println("CALL OrderProcessingSystem.calculateDiscount");
System.out.println("CALL OrderProcessingSystem.calculateDiscount");
System.out.println("CALL OrderProcessingSystem.calculateDiscount");
        double subtotal = calculateSubtotal();
        double discount = 0.0;

        if (subtotal > 200.0) {
            discount = 0.15; // 15% discount for orders above $200
        } else if (subtotal > 100.0) {
System.out.println("CALL OrderProcessingSystem.if");
System.out.println("CALL OrderProcessingSystem.if");
System.out.println("CALL OrderProcessingSystem.if");
System.out.println("CALL OrderProcessingSystem.if");
            discount = 0.10; // 10% discount for orders above $100
        }

        return subtotal * discount;
    }

    public double calculateTax() {
System.out.println("CALL OrderProcessingSystem.calculateTax");
System.out.println("CALL OrderProcessingSystem.calculateTax");
System.out.println("CALL OrderProcessingSystem.calculateTax");
System.out.println("CALL OrderProcessingSystem.calculateTax");
        double subtotal = calculateSubtotal();
        double discount = calculateDiscount();
        double subtotalAfterDiscount = subtotal - discount;
        return subtotalAfterDiscount * TAX_RATE;
    }

    public double calculateShippingCost() {
System.out.println("CALL OrderProcessingSystem.calculateShippingCost");
System.out.println("CALL OrderProcessingSystem.calculateShippingCost");
System.out.println("CALL OrderProcessingSystem.calculateShippingCost");
System.out.println("CALL OrderProcessingSystem.calculateShippingCost");
        double subtotal = 500 + calculateSubtotal();
        if (subtotal >= FREE_SHIPPING_THRESHOLD) {
            return 0.0; // Free shipping if order exceeds $100
        }
        return STANDARD_SHIPPING_COST;
    }

    public Invoice generateInvoice() {
System.out.println("CALL OrderProcessingSystem.generateInvoice");
System.out.println("CALL OrderProcessingSystem.generateInvoice");
System.out.println("CALL OrderProcessingSystem.generateInvoice");
System.out.println("CALL OrderProcessingSystem.generateInvoice");
        double subtotal = calculateSubtotal();
        double discount = calculateDiscount();
        double tax = calculateTax();
        double shippingCost = calculateShippingCost();

        double totalAmount = subtotal - discount + tax + shippingCost;

        Invoice invoice = new Invoice(subtotal, discount, tax, shippingCost, totalAmount);
        return invoice;
    }
}
