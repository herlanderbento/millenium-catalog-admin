from src.core.cast_member.infra.cast_member_in_memory_repository import (
    CastMemberInMemoryRepository,
)

from src.core.cast_member.domain.cast_member import CastMemberType
from src.core.cast_member.application.use_cases.create_cast_member import (
    CreateCastMemberInput,
    CreateCastMemberOutput,
    CreateCastMemberUseCase,
)

class TestCreateCastMemberUseCase:
    use_case: CreateCastMemberUseCase
    cast_member_repo: CastMemberInMemoryRepository

    def setup_method(self) -> None:
        self.cast_member_repo = CastMemberInMemoryRepository()
        self.use_case = CreateCastMemberUseCase(self.cast_member_repo)

    def test_should_be_able_to_create_cast_member(self):
        input = CreateCastMemberInput(name="John Doe", type=CastMemberType.ACTOR)

        output = self.use_case.execute(input)

        assert output == CreateCastMemberOutput(
            id=self.cast_member_repo.items[0].id.value,
            name="John Doe",
            type=CastMemberType.ACTOR,
            created_at=self.cast_member_repo.items[0].created_at,
        )

        input = CreateCastMemberInput(name="John McQueen", type=CastMemberType.DIRECTOR)

        output = self.use_case.execute(input)

        assert output == CreateCastMemberOutput(
            id=self.cast_member_repo.items[1].id.value,
            name="John McQueen",
            type=CastMemberType.DIRECTOR,
            created_at=self.cast_member_repo.items[1].created_at,
        )
