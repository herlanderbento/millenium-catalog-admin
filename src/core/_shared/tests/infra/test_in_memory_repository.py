from dataclasses import dataclass
import re
from typing import Type
from unittest import TestCase
from uuid import UUID, uuid4

import pytest
from src.core._shared.domain.exceptions import NotFoundException
from src.core._shared.infra.db.in_memory.in_memory_repository import InMemoryRepository
from src.core._shared.domain.repository_interface import IRepository
from src.core._shared.domain.entity import Entity


class TestRepositoryInterface(TestCase):
    def test_throw_error_when_methods_not_implemented(self):
        with self.assertRaises(TypeError) as assert_error:
            IRepository()
        error_message = assert_error.exception.args[0]

        print("Actual error message:", error_message)

        expected_pattern = (
            r"Can't instantiate abstract class IRepository without an implementation for abstract methods "
            r"'bulk_insert', 'delete', 'exists_by_id', 'find_all', 'find_by_id', 'find_by_ids', 'get_entity', "
            r"'insert', 'update'"
        )

        self.assertTrue(
            re.search(expected_pattern, error_message),
            f"Expected pattern: {expected_pattern}, but got: {error_message}",
        )


@dataclass
class StubEntity(Entity):
    name: str
    price: float

    def validate(self) -> None:
        raise NotImplementedError()


class StubInMemoryRepository(InMemoryRepository[StubEntity]):
    def get_entity(self) -> Type[StubEntity]:
        return StubEntity


class TestInMemoryRepository(TestCase):
    repository = StubInMemoryRepository

    def setUp(self) -> None:
        self.repository = StubInMemoryRepository()

    def test_should_be_able_to_items_prop_is_empty_on_init(self):
        self.assertEqual(self.repository.items, [])

    def test_should_be_able_to_insert(self):
        stub_entity = StubEntity(name="some entity", price=100)

        self.repository.insert(stub_entity)

        assert self.repository.find_by_id(stub_entity.id) == stub_entity

    def test_should_be_able_to_bulk_insert(self):
        stub_entity_1 = StubEntity(name="some entity 1", price=100)
        stub_entity_2 = StubEntity(name="some entity 2", price=100)

        self.repository.bulk_insert([stub_entity_1, stub_entity_2])

        assert self.repository.find_by_id(stub_entity_1.id) == stub_entity_1
        assert self.repository.find_by_id(stub_entity_2.id) == stub_entity_2

    def test_should_be_able_to_find_by_id(self):
        stub_entity = StubEntity(name="some entity", price=100)

        self.repository.insert(stub_entity)

        found_stub_entity = self.repository.find_by_id(stub_entity.id)

        assert found_stub_entity == stub_entity

    def test_should_be_able_to_find_by_ids(self):
        stub_entity_1 = StubEntity(name="some entity 1", price=100)
        stub_entity_2 = StubEntity(name="some entity 2", price=100)

        self.repository.bulk_insert([stub_entity_1, stub_entity_2])

        assert self.repository.find_by_ids([stub_entity_1.id, stub_entity_2.id]) == [
            stub_entity_1,
            stub_entity_2,
        ]

    def test_should_be_able_to_find_all(self):
        stub_entity_1 = StubEntity(name="some entity 1", price=100)
        stub_entity_2 = StubEntity(name="some entity 2", price=100)

        self.repository.bulk_insert([stub_entity_1, stub_entity_2])

        found_stub_entities = self.repository.find_all()
        assert len(found_stub_entities) == 2
        assert found_stub_entities[0] == stub_entity_1
        assert found_stub_entities[1] == stub_entity_2

    def test_should_be_able_to_exists_by_id(self):
        stub_entity_1 = StubEntity(name="entity 1", price=100)
        stub_entity_2 = StubEntity(name="entity 2", price=200)
        stub_entity_3 = StubEntity(name="entity 3", price=300)

        self.repository.bulk_insert([stub_entity_1, stub_entity_2])

        existing_ids = {stub_entity_1.id, stub_entity_2.id}  # Use sets for comparison
        non_existing_id = UUID("12345678-1234-5678-1234-567812345678")
        mixed_ids = [stub_entity_1.id, non_existing_id]

        result = self.repository.exists_by_id(existing_ids)

        assert set(result["exists"]) == existing_ids
        assert result["not_exists"] == []

        result = self.repository.exists_by_id([non_existing_id])
        assert result["exists"] == []
        assert result["not_exists"] == [non_existing_id]

        result = self.repository.exists_by_id(mixed_ids)
        assert set(result["exists"]) == {stub_entity_1.id}
        assert result["not_exists"] == [non_existing_id]

    def test_update_should_raise_not_found_exception_for_non_existent_entity(self):
        non_existent_entity = StubEntity(id=uuid4(), name="Non-existent", price=0.0)

        with pytest.raises(
            NotFoundException,
            match=f"StubEntity Not Found using ID {non_existent_entity.id}",
        ):
            self.repository.update(non_existent_entity)

    def test_should_be_able_to_update(self):
        stub_entity = StubEntity(name="Original Name", price=100.0)
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
        stub_entity = StubEntity(name="Original Name", price=100.0)
        self.repository.insert(stub_entity)

        self.repository.delete(stub_entity.id)

        assert self.repository.find_by_id(stub_entity.id) is None

    def test_should_raise_not_found_exception_when_deleting_non_existent_entity(self):
        self.test_update_should_raise_not_found_exception_for_non_existent_entity()
