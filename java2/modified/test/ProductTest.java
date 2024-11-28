import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class ProductTest {

    @Test
    public void testProductCreation() {
        Product product = new Product("Book A", 2, 15.0);
        assertEquals("Book A", product.getName());
        assertEquals(2, product.getQuantity());
        assertEquals(15.0, product.getPrice());
        
        System.out.println("Running test");
    }
}
