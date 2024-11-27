public class Main {
    public static void main(String[] args) {
System.out.println("CALL main");
System.out.println("CALL main");
        BankAccount account = new BankAccount(123456789, 1000.00);

        System.out.println("Account Number: " + account.getAccountNumber());
        System.out.println("Initial Balance: " + account.getBalance());

        account.deposit(500.00);
        System.out.println("Balance after deposit: " + account.getBalance());

        account.withdraw(300.00);
        System.out.println("Balance after withdrawal: " + account.getBalance());
    }
}