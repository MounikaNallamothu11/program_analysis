package main;

public class Invoice {
    private double subtotal;
    private double discount;
    private double tax;
    private double shippingCost;
    private double totalAmount;

    public Invoice(double subtotal, double discount, double tax, double shippingCost, double totalAmount) {
        this.subtotal = subtotal;
        this.discount = discount;
        this.tax = tax;
        this.shippingCost = shippingCost;
        this.totalAmount = totalAmount;
    }

    @Override
    public String toString() {
        return "main.Invoice:\n" +
               "Subtotal: $" + subtotal + "\n" +
               "Discount: -$" + discount + "\n" +
               "Tax: $" + tax + "\n" +
               "Shipping: $" + shippingCost + "\n" +
               "Total Amount: $" + totalAmount;
    }

    public double getSubtotal() {
        return subtotal;
    }

    public double getDiscount() {
        return discount;
    }

    public double getTax() {
        return tax;
    }

    public double getShippingCost() {
        return shippingCost;
    }

    public double getTotalAmount() {
        return totalAmount;
    }
}
