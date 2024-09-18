
from dataclasses import field
from typing import Any, Callable, List, Set
from pyee import EventEmitter


from src.core._shared.domain.entities.base_entity import BaseEntity
from src.core._shared.domain.events.domain_event_interface import IDomainEvent


class AggregateRoots(BaseEntity):
    events: Set[IDomainEvent] = field(init=False, default_factory=set)
    dispatched_events: Set[IDomainEvent] = field(init=False, default_factory=set)
    local_mediator: EventEmitter = field(init=False, default_factory=EventEmitter)
    
    def __post_init__(self):
        self.events = set()
        self.dispatched_events = set()
        self.local_mediator = EventEmitter()
        
    def apply_event(self, event: IDomainEvent):
        self.events.add(event)
        self.local_mediator.emit(event.__class__.__name__, event)

    def register_handler(self, event: str, handler: Callable[[IDomainEvent], None]):        
        print(f"register_handler {handler.__name__}")  # Exemplo de como você pode imprimir o nome da função
        self.local_mediator.on(event, handler)

    def mark_event_as_dispatched(self, event: IDomainEvent):
        self.dispatched_events.add(event)

    def get_uncommitted_events(self) -> List[IDomainEvent]:
        return [event for event in self.events if event not in self.dispatched_events]

    def clear_events(self):
        self.events.clear()
        self.dispatched_events.clear()



# class AggregateRoots(BaseEntity):
#     events: Set[IDomainEvent] = field(init=False, default_factory=set)
#     dispatched_events: Set[IDomainEvent] = field(init=False, default_factory=set)
#     local_mediator: EventEmitter = field(init=False, default_factory=EventEmitter)

#     def __post_init__(self):
#         self.local_mediator = EventEmitter()
#         self.events = set()
#         self.dispatched_events = set()
        
#     def apply_event(self, event: IDomainEvent):
#         self.events.add(event)
#         self.local_mediator.emit(event.__class__.__name__, event)

#     def register_handler(self, event: str, handler: Callable[[IDomainEvent], None]):
#         self.local_mediator.on(event, handler)

#     def mark_event_as_dispatched(self, event: IDomainEvent):
#         self.dispatched_events.add(event)

#     def get_uncommitted_events(self) -> List[IDomainEvent]:
#         return [event for event in self.events if event not in self.dispatched_events]

#     def clear_events(self):
#         self.events.clear()
#         self.dispatched_events.clear()