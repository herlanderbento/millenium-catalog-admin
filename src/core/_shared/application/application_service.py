from typing import TypeVar
from src.core._shared.domain.events.domain_event_mediator import DomainEventMediator
from src.core._shared.domain.repositories.unit_of_work_interface import IUnitOfWork


T = TypeVar("T")


class ApplicationService:
    def __init__(
        self,
        uow: IUnitOfWork,
        domain_event_mediator: DomainEventMediator,
    ):
        self.uow = uow
        self.domain_event_mediator = domain_event_mediator

    def start(self):
        self.uow.start()

    def finish(self):
        aggregate_roots = list(self.uow.get_aggregate_roots())


        for aggregate_root in aggregate_roots:
            print(f"aggregate_roots: {aggregate_root.events}")

            self.domain_event_mediator.handle(aggregate_root.events)

        self.uow.commit()


    def fail(self):
        self.uow.rollback()

    def run(self, callback: callable) -> T:
        self.start()
        try:
            result = callback()
            self.finish()
            return result
        except Exception as error:
            self.fail()
            raise error