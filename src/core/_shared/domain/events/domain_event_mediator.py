from pyee import EventEmitter
from typing import Any

from src.core._shared.domain.entities.aggregate_roots import AggregateRoots


class DomainEventMediator:
    def __init__(self, event_emitter: EventEmitter = EventEmitter):
        self.event_emitter = event_emitter

    def register(self, event: str, handler: Any):
        self.event_emitter.on(event, handler)

    def publish(self, aggregate_root: AggregateRoots):
        for event in aggregate_root.get_uncommitted_events():
            event_class_name = event.__class__.__name__
            aggregate_root.mark_event_as_dispatched(event)
            self.event_emitter.emit(event_class_name, event)

    def publish_integration_events(self, aggregate_root: AggregateRoots):
        for event in aggregate_root.events:
            integration_event = getattr(event.get_integration_event(), None)

            if integration_event:
                integration_event_instance = integration_event()
                self.event_emitter.emit(
                    integration_event_instance.__class__.__name__,
                    integration_event_instance,
                )
