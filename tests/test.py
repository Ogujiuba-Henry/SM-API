import pytest
from app.test_calculations import add,subtract,multiply,divide,BankAccount,InsufficientFunds

@pytest.fixture                     # to replace the bank_account=BankAccount()
def zero_bank_account():
    return BankAccount()

@pytest.fixture                     #to replace bank_account=BankAccount(50)
def bank_account():
    return BankAccount(50)

@pytest.mark.parametrize("num1,num2,expected",[   # to include multiple params for our functions || the irregular var "" is a convention
    (1,2,3),
    (2,3,5),
    (10,11,21)
])
def test_add(num1,num2,expected):
    print("Testing add functions")
    assert add(num1,num2)==expected
    

def test_subtract():
    assert subtract(9,4) ==5 

def test_multiply():
    assert multiply(9,4) ==36 

def test_divide():
    assert divide(9,3) == 3

def test_bank_set_initial_amount(bank_account):   
    # bank_account=BankAccount(50)
    assert bank_account.balance == 50

def test_bank_default_amount(zero_bank_account):
    # bank_account=BankAccount()
    assert zero_bank_account.balance == 0

def test_withdraw(bank_account):
    # bank_account = BankAccount(50)
    bank_account.withdraw(20)
    assert bank_account.balance == 30

def test_deposit(bank_account):
    # bank_account = BankAccount(50)
    bank_account.deposit(20)
    assert bank_account.balance == 70

def test_collect_interest(bank_account):
    # bank_account = BankAccount(50)
    bank_account.collect_interest()
    assert round(bank_account.balance,6) == 55

@pytest.mark.parametrize("deposited,withdraw,expected",[
    (200,100,100),
    (50,3,47),
    (1200,200,1000)
])

def test_bank_transactions(zero_bank_account,deposited,withdraw,expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdraw)
    assert zero_bank_account.balance == expected


def test_insufficient_funds(bank_account):
    with pytest.raises(InsufficientFunds):   #allows a further code to run in case of Exception
        bank_account.withdraw(200)



