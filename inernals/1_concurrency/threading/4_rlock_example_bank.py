"""
 You need to implement a BankAccount class with transfer and deposit methods. 
 The transfer method should use the deposit method to move funds, and both methods must be thread-safe.

If both transfer and deposit use a standard Lock, a transfer call will acquire the lock and then call deposit. 
The deposit call will try to acquire the same lock, causing a deadlock because the thread is waiting for itself to release a lock it already holds.
"""

# Here spot it's a deadlock
import threading

class BankAccount:
    def __init__(self, initial_banace=0):
        self.balance = initial_banace
        self.lock = threading.RLock()

    def deposit(self, amount):
        with self.lock:
            self.balance += amount
            print(f'Amount {amount} has deposited successfully')

    def transfer(self, amount, other_account):
        with self.lock:
            if self.balance < amount:
                raise ValueError('Insufficient funds')
            self.balance -= amount
            other_account.deposit(amount)

account1 = BankAccount(1000)
account2 = BankAccount(500)

thread = threading.Thread(target= lambda: account1.transfer(200, account2))
thread2 = threading.Thread(target=lambda: account2.transfer(100, account1))
thread.start()
thread.join()
print(f"Final balances: Account1={account1.balance}, Account2={account2.balance}")