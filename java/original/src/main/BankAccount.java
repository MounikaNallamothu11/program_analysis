import java.util.List;

//BankAccount class
public class BankAccount {
    public long accountNr;
    private double balance;

    public BankAccount(long accountNr, double initialBalance) {
System.out.println("CALL BankAccount");
System.out.println("CALL BankAccount");
System.out.println("CALL BankAccount");
System.out.println("CALL BankAccount");
        this.accountNr = accountNr;
        this.balance = initialBalance;
    }

    // 1. Function that Calls Another Function
    public void deposit(double amount) {
System.out.println("CALL deposit");
System.out.println("CALL deposit");
System.out.println("CALL deposit");
System.out.println("CALL deposit");
        balance += add(amount);
    }

    private double add(double amount) {
System.out.println("CALL add");
System.out.println("CALL add");
System.out.println("CALL add");
System.out.println("CALL add");
        return amount; // Simply returns the amount to be added
    }

    // 2. Function with if-else
    public String transfer(double amount, BankAccount destinationAccount) {
System.out.println("CALL transfer");
System.out.println("CALL transfer");
System.out.println("CALL transfer");
System.out.println("CALL transfer");
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
System.out.println("CALL calculateInterest");
System.out.println("CALL calculateInterest");
System.out.println("CALL calculateInterest");
System.out.println("CALL calculateInterest");
        if (years == 0) {
            throw new ArithmeticException("Cannot divide by zero.");
        }
        return balance / years; // Calculates interest based on the number of years
    }

    // 4. Function with Loop and if-else Inside the Loop
    public static double sumPositiveBalances(List<BankAccount> accounts) {
System.out.println("CALL sumPositiveBalances");
System.out.println("CALL sumPositiveBalances");
System.out.println("CALL sumPositiveBalances");
System.out.println("CALL sumPositiveBalances");
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
System.out.println("CALL getBalance");
System.out.println("CALL getBalance");
System.out.println("CALL getBalance");
System.out.println("CALL getBalance");
        return balance; // Returns the current balance
    }

    public void withdraw(double amount) {
System.out.println("CALL withdraw");
System.out.println("CALL withdraw");
System.out.println("CALL withdraw");
System.out.println("CALL withdraw");
        balance -= amount; // Withdraws the specified amount
    }

    public long getAccountNumber() {
System.out.println("CALL getAccountNumber");
System.out.println("CALL getAccountNumber");
System.out.println("CALL getAccountNumber");
System.out.println("CALL getAccountNumber");
        return accountNr;
    }

    public String getAccountSummary() {
System.out.println("CALL getAccountSummary");
System.out.println("CALL getAccountSummary");
System.out.println("CALL getAccountSummary");
System.out.println("CALL getAccountSummary");
        return "Account " + accountNr + " has a balance of " + balance;
    }
}
