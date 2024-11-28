package main;

public class Invoice {
    private double subtotal;
    private double discount;
    private double tax;
    private double shippingCost;
    private double totalAmount;

    public Invoice(double subtotal, double discount, double tax, double shippingCost, double totalAmount) {
System.out.println("CALL Invoice.Invoice");
System.out.println("CALL Invoice.Invoice");
System.out.println("CALL Invoice.Invoice");
System.out.println("CALL Invoice.Invoice");
        this.subtotal = subtotal;
        this.discount = discount;
        this.tax = tax;
        this.shippingCost = shippingCost;
        this.totalAmount = totalAmount;

        System.out.println("Creating invoice");
    }

    @Override
    public String toString() {
System.out.println("CALL Invoice.toString");
System.out.println("CALL Invoice.toString");
System.out.println("CALL Invoice.toString");
System.out.println("CALL Invoice.toString");
        System.out.println("Converting to string");
        return "main.Invoice:\n" +
               "Subtotal: $" + subtotal + "\n" +
               "Discount: -$" + discount + "\n" +
               "Tax: $" + tax + "\n" +
               "Shipping: $" + shippingCost + "\n" +
               "Total Amount: $" + totalAmount;
    }

    public double getSubtotal() {
System.out.println("CALL Invoice.getSubtotal");
System.out.println("CALL Invoice.getSubtotal");
System.out.println("CALL Invoice.getSubtotal");
System.out.println("CALL Invoice.getSubtotal");
        return subtotal;
    }

    public double getDiscount() {
System.out.println("CALL Invoice.getDiscount");
System.out.println("CALL Invoice.getDiscount");
System.out.println("CALL Invoice.getDiscount");
System.out.println("CALL Invoice.getDiscount");
        return discount;
    }

    public double getTax() {
System.out.println("CALL Invoice.getTax");
System.out.println("CALL Invoice.getTax");
System.out.println("CALL Invoice.getTax");
System.out.println("CALL Invoice.getTax");
        return tax;
    }

    public double getShippingCost() {
System.out.println("CALL Invoice.getShippingCost");
System.out.println("CALL Invoice.getShippingCost");
System.out.println("CALL Invoice.getShippingCost");
System.out.println("CALL Invoice.getShippingCost");
        return shippingCost;
    }

    public double getTotalAmount() {
System.out.println("CALL Invoice.getTotalAmount");
System.out.println("CALL Invoice.getTotalAmount");
System.out.println("CALL Invoice.getTotalAmount");
System.out.println("CALL Invoice.getTotalAmount");
        return totalAmount;
    }
}
