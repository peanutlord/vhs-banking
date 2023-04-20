import datetime
from dataclasses import dataclass, field
from typing import Dict, Any, List, Tuple


@dataclass(frozen=True)
class Event:
    amount: float
    purpose: str
    value_date: datetime.datetime = field(default_factory=datetime.datetime.today)
    metadata: Dict[str, Any] = field(default_factory=dict)  # only "source" supported


class Ledger:

    def __init__(self):
        self._events = []

    def add_event(self, event: Event) -> None:
        self._events.append(event)

    def aggregate_sum(self) -> float:
        return sum(event.amount for event in self._events)
