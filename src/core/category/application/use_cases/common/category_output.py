from dataclasses import asdict, dataclass
from uuid import UUID

from src.core.category.domain.category import Category


@dataclass
class CategoryOutput:
    id: UUID
    name: str
    description: str
    is_active: bool


class CategoryOutputMapper:

    @staticmethod
    def to_output(entity: Category, output_class=CategoryOutput) -> CategoryOutput:
        entity_dict = asdict(entity)
        entity_dict.pop("notification", None)
        return output_class(**entity_dict)
