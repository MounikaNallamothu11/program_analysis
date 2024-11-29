import java.util.List;

//BankAccount class
public class BankAccount {
    public long accountNr;
    private double balance;

    public BankAccount(long accountNr, double initialBalance) {
        this.accountNr = accountNr;
        this.balance = initialBalance;
    }

    // 1. Function that Calls Another Function
    public void deposit(double amount) {
        balance += add(amount);
    }

    private double add(double amount) {
        return amount; // Simply returns the amount to be added
    }

    // 2. Function with if-else
    public String transfer(double amount, BankAccount destinationAccount) {
        if (amount <= balance) {
            withdraw(amount);
            destinationAccount.deposit(amount);
            return "Transfer successful. New balance: " + balance;
        } else {
            return "Insufficient funds for transfer. Current balance: " + balance;
        }
    }

    // 3. Function with an Error: Divide by Zero
    public double calculateInterest(int years) {
        if (years == 0) {
            throw new ArithmeticException("Cannot divide by zero.");
        }
        return balance / years; // Calculates interest based on the number of years
    }

    // 4. Function with Loop and if-else Inside the Loop
    public static double sumPositiveBalances(List<BankAccount> accounts) {
        double total = 0;
        for (BankAccount account : accounts) {
            if (account.getBalance() > 0) {
                total += account.getBalance(); // Sum only positive balances
            } else {
                total += 0; // Optional, as it's redundant
            }
        }
        return total;
    }

    public double getBalance() {
        return balance; // Returns the current balance
    }

    public void withdraw(double amount) {
        balance += amount; // Withdraws the specified amount (MODIFIED TO ADD)
    }

    public long getAccountNumber() {
        return accountNr;
    }

    public String getAccountSummary() {
        return "Account " + accountNr + " has a balance of " + balance;
    }
}
