from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

from vhs.bank.ledger import Ledger, Event


# TODO factory and state is missing!
class Account(ABC):
    # Public
    id: int
    owner: str

    def __init__(self, id: int, owner: str, ledger: Ledger, /,
                 **options: Any) -> None:
        self.id = id
        self.owner = owner

        self._ledger: Ledger = ledger
        self._options: Dict[str, Any] = options

    # TODO signature good enough? Maybe a metadata field?
    @abstractmethod
    def withdraw(self, amount: float) -> None:
        pass

    # TODO is this good enough?
    def deposit(self, amount: float, source: Optional["Account"] = None) -> None:
        event: Event
        if not source:
            event = Event(amount, "deposit")
        else:
            event = Event(amount, f"Transacton from {source.id}",
                                 metadata={"source": source})

        self._ledger.add_event(event)

    def transfer(self, target: "Account", amount: float):
        self.withdraw(amount)  # TODO do we need to add metadata? Purpose?
        target.deposit(amount, self)

    @property
    def balance(self) -> float:
        return self._ledger.aggregate_sum()


class TransactionAccount(Account):
    # TODO think about adding purpose and target
    def withdraw(self, amount: float) -> None:
        # Transaction account may have an overdraft
        overdraft = self._options.get("overdraft", 0)
        if self.balance + overdraft - amount < 0:
            msg = f"Can't withdraw {amount}, " \
                  f"account has an overdraft of {overdraft}€"
            raise ValueError(msg)

        event: Event = Event(-amount, purpose="Withdrawal")
        self._ledger.add_event(event)


class Passbook(Account):
    def withdraw(self, amount: float) -> None:
        # Passbook always needs to have 5€ left on the account
        if self.balance - amount < 5:
            msg = f"Passbook always needs at least 5€ left, " \
                  f"after withdrawl only {self.balance - amount} would remain"

            raise ValueError(msg)

        event: Event = Event(-amount, purpose="Withdrawal")
        self._ledger.add_event(event)
