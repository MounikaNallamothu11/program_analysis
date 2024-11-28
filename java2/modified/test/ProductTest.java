import main.Product;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class ProductTest {

    @Test
    public void testProductCreation() {
        Product product = new Product("main.Book A", 2, 15.0);
        assertEquals("main.Book A", product.getName());
        assertEquals(2, product.getQuantity());
        assertEquals(15.0, product.getPrice());

        System.out.println("Running test");
    }
}
