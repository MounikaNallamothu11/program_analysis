import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class OrderProcessingSystemTest {

    @Test
    public void testCalculateSubtotal() {
        OrderProcessingSystem orderSystem = new OrderProcessingSystem();
        orderSystem.addProductToOrder(new Product("Book A", 2, 10.0));
        orderSystem.addProductToOrder(new Product("Book B", 1, 20.0));
        assertEquals(40.0, orderSystem.calculateSubtotal());
    }

    @Test
    public void testCalculateDiscount() {
        OrderProcessingSystem orderSystem = new OrderProcessingSystem();
        orderSystem.addProductToOrder(new Product("Book A", 3, 60.0)); // $180
        assertEquals(18.0, orderSystem.calculateDiscount()); // 10% discount
    }

    @Test
    public void testShippingCost() {
        OrderProcessingSystem orderSystem = new OrderProcessingSystem();
        orderSystem.addProductToOrder(new Product("Book A", 1, 50.0));
        assertEquals(5.0, orderSystem.calculateShippingCost()); // Below threshold
        orderSystem.addProductToOrder(new Product("Book B", 1, 60.0));
        assertEquals(0.0, orderSystem.calculateShippingCost()); // Above threshold
    }

    @Test
    public void testGenerateInvoice() {
        OrderProcessingSystem orderSystem = new OrderProcessingSystem();
        orderSystem.addProductToOrder(new Product("Book A", 3, 60.0)); // $180
        Invoice invoice = orderSystem.generateInvoice();
        assertNotNull(invoice);
        assertEquals(180.0, invoice.getSubtotal());
        assertEquals(18.0, invoice.getDiscount());
    }
}
