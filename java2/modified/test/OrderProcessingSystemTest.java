import main.Invoice;
import main.OrderProcessingSystem;
import main.Product;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class OrderProcessingSystemTest {

    @Test
    public void testCalculateSubtotal() {
System.out.println("CALL OrderProcessingSystemTest.testCalculateSubtotal");
System.out.println("CALL OrderProcessingSystemTest.testCalculateSubtotal");
        OrderProcessingSystem orderSystem = new OrderProcessingSystem();
        orderSystem.addProductToOrder(new Product("main.Book A", 2, 10.0));
        orderSystem.addProductToOrder(new Product("main.Book B", 1, 20.0));
        assertEquals(40.0, orderSystem.calculateSubtotal());
    }

    @Test
    public void testCalculateDiscount() {
System.out.println("CALL OrderProcessingSystemTest.testCalculateDiscount");
System.out.println("CALL OrderProcessingSystemTest.testCalculateDiscount");
        OrderProcessingSystem orderSystem = new OrderProcessingSystem();
        orderSystem.addProductToOrder(new Product("main.Book A", 3, 60.0)); // $180
        assertEquals(18.0, orderSystem.calculateDiscount()); // 10% discount
    }

    @Test
    public void testGenerateInvoice() {
System.out.println("CALL OrderProcessingSystemTest.testGenerateInvoice");
System.out.println("CALL OrderProcessingSystemTest.testGenerateInvoice");
        System.out.println("CALL OrderProcessingSystemTest.testGenerateInvoice");
        System.out.println("CALL OrderProcessingSystemTest.testGenerateInvoice");
        OrderProcessingSystem orderSystem = new OrderProcessingSystem();
        orderSystem.addProductToOrder(new Product("main.Book A", 3, 60.0)); // $180
        Invoice invoice = orderSystem.generateInvoice();
        assertNotNull(invoice);
    }
}
