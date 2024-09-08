import uuid
import pytest

from src.core._shared.domain.exceptions import NotFoundException
from src.django_project.cast_member_app.repository import CastMemberDjangoRepository
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.application.use_cases.delete_cast_member import (
    DeleteCastMemberInput,
    DeleteCastMemberUseCase,
)


@pytest.mark.django_db
class TestDeleteCastMemberUseCaseInt:
    use_case: DeleteCastMemberUseCase
    cast_member_repo: CastMemberDjangoRepository

    def setup_method(self) -> None:
        self.cast_member_repo = CastMemberDjangoRepository()
        self.use_case = DeleteCastMemberUseCase(self.cast_member_repo)

    def test_must_be_able_to_return_an_error_when_the_entity_does_not_exist(self):
        input = DeleteCastMemberInput(id=uuid.uuid4())
        with pytest.raises(
            NotFoundException, match=f"CastMember with id {input.id} not found"
        ):
            self.use_case.execute(input)

    def test_should_be_able_to_delete_a_cast_member(self):
        cast_member = CastMember(name="Herlander Bento", type=CastMemberType.DIRECTOR)

        self.cast_member_repo.insert(cast_member)

        input = DeleteCastMemberInput(id=cast_member.id.value)

        self.use_case.execute(input)

        assert self.cast_member_repo.find_by_id(cast_member.id.value) is None
