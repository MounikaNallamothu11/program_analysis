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
    public void testGenerateInvoice() {
        OrderProcessingSystem orderSystem = new OrderProcessingSystem();
        orderSystem.addProductToOrder(new Product("Book A", 3, 60.0)); // $180
        Invoice invoice = orderSystem.generateInvoice();
        assertNotNull(invoice);
    }
}
