import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class InvoiceTest {

    @Test
    public void testInvoiceGeneration() {
        Invoice invoice = new Invoice(100.0, 10.0, 8.0, 5.0, 103.0);
        assertEquals(100.0, invoice.getSubtotal());
        assertEquals(10.0, invoice.getDiscount());
        assertEquals(8.0, invoice.getTax());
        assertEquals(5.0, invoice.getShippingCost());
        assertEquals(103.0, invoice.getTotalAmount());
    }

    @Test
    public void testInvoiceToString() {
        Invoice invoice = new Invoice(150.0, 15.0, 10.5, 0.0, 145.5);
        String expected = "Invoice:\n" +
                "Subtotal: $150.0\n" +
                "Discount: -$15.0\n" +
                "Tax: $10.5\n" +
                "Shipping: $0.0\n" +
                "Total Amount: $145.5";
        assertEquals(expected, invoice.toString());
    }
}
