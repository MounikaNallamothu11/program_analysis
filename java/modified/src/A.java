public class A {

    public A() {
        System.out.println("A constructor");
    }

    public void b() {
        BankAccount.sumPositiveBalances(null);
    }

    public void c() {
        BankAccount bankAccount = new BankAccount(1, 100);
        B b = new B();

        bankAccount.calculateInterest(0);
        b.crazy();
    }

}
