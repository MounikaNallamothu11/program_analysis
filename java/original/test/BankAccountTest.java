import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.Test;
import java.util.ArrayList;
import java.util.List;

public class BankAccountTest {

    @Test
    public void testDeposit() {
System.out.println("CALL testDeposit");
System.out.println("CALL testDeposit");
System.out.println("CALL testDeposit");
System.out.println("CALL testDeposit");
        BankAccount account = new BankAccount(1, 100);
        account.deposit(50);
        assertEquals(150, account.getBalance());
    }

    @Test
    public void testTransferSuccess() {
System.out.println("CALL testTransferSuccess");
System.out.println("CALL testTransferSuccess");
System.out.println("CALL testTransferSuccess");
System.out.println("CALL testTransferSuccess");
        BankAccount sourceAccount = new BankAccount(1, 100);
        BankAccount destinationAccount = new BankAccount(2, 50);
        String result = sourceAccount.transfer(50, destinationAccount);
        assertEquals("Transfer successful. New balance: 50.0", result);
        assertEquals(100, destinationAccount.getBalance());
    }

    @Test
    public void testTransferInsufficientFunds() {
System.out.println("CALL testTransferInsufficientFunds");
System.out.println("CALL testTransferInsufficientFunds");
System.out.println("CALL testTransferInsufficientFunds");
System.out.println("CALL testTransferInsufficientFunds");
        BankAccount sourceAccount = new BankAccount(1, 100);
        BankAccount destinationAccount = new BankAccount(2, 50);
        String result = sourceAccount.transfer(150, destinationAccount);
        assertEquals("Insufficient funds for transfer. Current balance: 100.0",
                result);
    }

    @Test
    public void testCalculateInterestDivideByZero() {
System.out.println("CALL testCalculateInterestDivideByZero");
System.out.println("CALL testCalculateInterestDivideByZero");
System.out.println("CALL testCalculateInterestDivideByZero");
System.out.println("CALL testCalculateInterestDivideByZero");
        BankAccount account = new BankAccount(1, 100);
        assertThrows(ArithmeticException.class, () -> account.calculateInterest(0));
    }

    @Test
    public void testSumPositiveBalances() {
System.out.println("CALL testSumPositiveBalances");
System.out.println("CALL testSumPositiveBalances");
System.out.println("CALL testSumPositiveBalances");
System.out.println("CALL testSumPositiveBalances");
        List<BankAccount> accounts = new ArrayList<>();
        accounts.add(new BankAccount(1, 100)); // Positive balance
        accounts.add(new BankAccount(2, -50)); // Negative balance
        accounts.add(new BankAccount(3, 200)); // Positive balance
        accounts.add(new BankAccount(4, 0)); // Zero balance

        double total = BankAccount.sumPositiveBalances(accounts);
        assertEquals(300, total); // Only sum positive balances: 100 + 200 = 300
    }

    @Test
    public void testGetAccountSummary() {
System.out.println("CALL testGetAccountSummary");
System.out.println("CALL testGetAccountSummary");
System.out.println("CALL testGetAccountSummary");
System.out.println("CALL testGetAccountSummary");
        BankAccount account = new BankAccount(1, 100);
        String summary = account.getAccountSummary();
        assertEquals("Account 1 has a balance of 100.0", summary);

        account.deposit(50);
        summary = account.getAccountSummary();
        assertEquals("Account 1 has a balance of 150.0", summary);

        account.withdraw(30);
        summary = account.getAccountSummary();
        assertEquals("Account 1 has a balance of 120.0", summary);
    }
}
