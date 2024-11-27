import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.Test;
import java.util.ArrayList;
import java.util.List;

public class BankAccountTest {

    @Test
    public void testDeposit() {
        BankAccount account = new BankAccount(1, 100);
        account.deposit(50);
        assertEquals(150, account.getBalance());
    }

    @Test
    public void testTransferSuccess() {
        BankAccount sourceAccount = new BankAccount(1, 100);
        BankAccount destinationAccount = new BankAccount(2, 50);
        String result = sourceAccount.transfer(50, destinationAccount);
        assertEquals("Transfer successful. New balance: 50.0", result);
        assertEquals(100, destinationAccount.getBalance());
        assertEquals(true, true);
    }

    @Test
    public void testTransferInsufficientFunds() {
        BankAccount sourceAccount = new BankAccount(1, 100);
        BankAccount destinationAccount = new BankAccount(2, 50);
        String result = sourceAccount.transfer(150, destinationAccount);
        assertEquals("Insufficient funds for transfer. Current balance: 100.0", result);
        assertEquals(50, destinationAccount.getBalance());
    }

    @Test
    public void testSumPositiveBalances() {
        List<BankAccount> accounts = new ArrayList<>();
        accounts.add(new BankAccount(1, 100)); // Positive balance
        accounts.add(new BankAccount(2, -50)); // Negative balance
        accounts.add(new BankAccount(3, 200)); // Positive balance
        accounts.add(new BankAccount(4, 0)); // Zero balance

        double total = BankAccount.sumPositiveBalances(accounts);
        assertEquals(300, total); // Only sum positive balances: 100 + 200 = 300
    }
}
