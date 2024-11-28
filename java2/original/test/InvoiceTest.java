import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class InvoiceTest {

    @Test
    public void testInvoiceCalculation() {
        OrderProcessingSystem orderSystem = new OrderProcessingSystem();
        orderSystem.addProductToOrder(new Product("Book A", 3, 60.0)); // $180
        Invoice invoice = orderSystem.generateInvoice();
        
        assertEquals(180.0, invoice.getSubtotal(), "Subtotal is incorrect");
        assertEquals(18.0, invoice.getDiscount(), "Discount is incorrect");
        assertEquals(12.96, invoice.getTax(), "Tax is incorrect");
        assertEquals(0.0, invoice.getShippingCost(), "Shipping cost is incorrect");
        assertEquals(174.96, invoice.getTotalAmount(), "Total amount is incorrect");
    }
}
