def add(num1:int,num2:int):
    return num1 + num2

def subtract(num1:int,num2:int):
    return num1 - num2

def multiply(num1:int,num2:int):
    return num1 * num2

def divide(num1:int,num2:int):
    return num1 / num2

class InsufficientFunds(Exception):      # creating Insufficient funds class to reference in withdrwal() which refrences Exception class
    pass

class BankAccount():
    def __init__(self,starting_balance=0):     #Initializes the account amount/starting balance
        self.balance = starting_balance        

    def deposit(self,amount):
        self.balance += amount

    def withdraw(self,amount):
        if amount > self.balance:
            raise InsufficientFunds("Insufficient funds")    # to make sure we're raising exception for only Insufficint funds
        self.balance -= amount

    def collect_interest(self):
        self.balance *= 1.1
