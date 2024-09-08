from dataclasses import dataclass

import pytest
from src.core._shared.domain.value_objects import Uuid
from src.core._shared.domain.exceptions import NotFoundException
from src.core._shared.infra.db.in_memory.in_memory_repository import InMemoryRepository
from src.core._shared.domain.entity import AggregateRoot


@dataclass(slots=True)
class StubEntity(AggregateRoot):
    id: Uuid
    name: str
    price: float

    @property
    def entity_id(self) -> Uuid:
        return self.id


class StubInMemoryRepository(InMemoryRepository[StubEntity, Uuid]):
    def get_entity(self):
        return StubEntity


class TestInMemoryRepository:
    repository: StubInMemoryRepository

    def setup_method(self):
        self.repository = StubInMemoryRepository()

    def test_should_be_able_to_insert(self):
        stub_entity = StubEntity(id=Uuid(), name="some entity", price=100)

        self.repository.insert(stub_entity)

        assert self.repository.find_by_id(stub_entity.id) == stub_entity

    def test_should_be_able_to_bulk_insert(self):
        entities = [
            StubEntity(id=Uuid(), name="some entity 1", price=100) for _ in range(3)
        ]

        self.repository.bulk_insert(entities)

        assert all(entity in self.repository.items for entity in entities)

    def test_should_be_able_to_find_by_id(self):
        stub_entity = StubEntity(id=Uuid(), name="some entity", price=100)

        self.repository.insert(stub_entity)

        found_stub_entity = self.repository.find_by_id(stub_entity.id)

        assert found_stub_entity == stub_entity

    def test_should_be_able_to_find_all(self):
        entities = [
            StubEntity(id=Uuid(), name="some entity 1", price=100) for _ in range(3)
        ]

        self.repository.bulk_insert(entities)

        found_entities = self.repository.find_all()
        assert all(entity in found_entities for entity in entities)

    def test_update_should_raise_not_found_exception_for_non_existent_entity(self):
        non_existent_entity = StubEntity(id=Uuid(), name="Non-existent", price=0.0)

        with pytest.raises(NotFoundException):
            self.repository.update(non_existent_entity)

    def test_should_be_able_to_update(self):
        stub_entity = StubEntity(id=Uuid(), name="Original Name", price=100.0)
        self.repository.insert(stub_entity)

        updated_entity = StubEntity(id=stub_entity.id, name="Updated Name", price=200)
        self.repository.update(updated_entity)

        result = self.repository.find_by_id(stub_entity.id)

        assert result is not None
        assert result.name == "Updated Name"
        assert result.price == 200

    def test_should_raise_not_found_exception_when_updating_non_existent_entity(self):
        self.test_update_should_raise_not_found_exception_for_non_existent_entity()

    def test_should_be_able_to_delete(self):
        stub_entity = StubEntity(id=Uuid(), name="Original Name", price=100.0)
        self.repository.insert(stub_entity)

        self.repository.delete(stub_entity.id)

        assert self.repository.find_by_id(stub_entity.id) is None

    def test_should_raise_not_found_exception_when_deleting_non_existent_entity(self):
        self.test_update_should_raise_not_found_exception_for_non_existent_entity()

    def test_get_entity(self):
        entity = self.repository.get_entity()
        assert entity == StubEntity
