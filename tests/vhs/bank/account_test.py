import pytest

from vhs.bank.account import TransactionAccount, Passbook
from vhs.bank.ledger import Ledger


def test_transferaccount_deposit():
    ledger = Ledger()

    acc = TransactionAccount(10000, "Christopher Marchfelder", ledger)
    acc.deposit(50)

    assert acc.balance == 50


def test_transferaccount_withdraw():
    ledger = Ledger()

    acc = TransactionAccount(10000, "Christopher Marchfelder", ledger)
    acc.deposit(50)
    acc.withdraw(15)

    assert acc.balance == 35


def test_transactionaccount_with_overdraft():
    ledger = Ledger()
    acc = TransactionAccount(10000, "Christopher Marchfelder", ledger,
                             overdraft=30)

    acc.deposit(10)
    acc.withdraw(20)

    assert acc.balance == -10


def test_transactionout_without_overdraft():
    ledger = Ledger()

    acc = TransactionAccount(10000, "Christopher Marchfelder", ledger)
    with pytest.raises(ValueError):
        acc.withdraw(10)


def test_passbook_needs_remainder():
    ledger = Ledger()

    acc = Passbook(10000, "Christopher Marchfelder", ledger)
    acc.deposit(10)

    with pytest.raises(ValueError):
        acc.withdraw(9)

    acc.withdraw(5)
    assert acc.balance == 5


def test_transactionaccount_transfer():
    ledger1 = Ledger()
    acc1 = TransactionAccount(10000, "Christopher Marchfelder", ledger1)
    acc1.deposit(50)

    ledger2 = Ledger()
    acc2 = TransactionAccount(10001, "Yoanna Krapova", ledger2)
    acc2.deposit(50)

    acc1.transfer(acc2, 30)

    assert acc1.balance == 20
    assert acc2.balance == 80

    # Verify source too
    assert acc2._ledger._events[1].metadata["source"] == acc1
