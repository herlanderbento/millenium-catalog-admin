from typing import Callable, List, TypeVar
from django.db import transaction
from src.core._shared.domain.entities.aggregate_roots import AggregateRoots
from src.core._shared.domain.repository.unit_of_work_interface import IUnitOfWork

T = TypeVar('T')

class UnitOfWork(IUnitOfWork):
    def __init__(self):
        self._transaction_started = False
        self._aggregate_roots = set()

    def start(self) -> None:
        if not self._transaction_started:
            transaction.set_autocommit(False)
            self._transaction_started = True

    def commit(self) -> None:
        if not self._transaction_started:
            raise RuntimeError("No transaction started")

        transaction.commit()
        self._transaction_started = False
        transaction.set_autocommit(True)

    def rollback(self) -> None:
        if not self._transaction_started:
            raise RuntimeError("No transaction started")

        transaction.rollback()
        self._transaction_started = False
        transaction.set_autocommit(True)

    def get_transaction(self) -> bool:
        return self._transaction_started

    def do(self, work_fn: Callable[["IUnitOfWork"], T]) -> T:
        if self._transaction_started:
            return work_fn(self)

        with transaction.atomic():
            self._transaction_started = True
            try:
                result = work_fn(self)
                self._transaction_started = False
                return result
            except Exception:
                self._transaction_started = False
                raise

    def add_aggregate_root(self, aggregate_root: AggregateRoots) -> None:
        self._aggregate_roots.add(aggregate_root)

    def get_aggregate_roots(self) -> List[AggregateRoots]:
        return list(self._aggregate_roots)
