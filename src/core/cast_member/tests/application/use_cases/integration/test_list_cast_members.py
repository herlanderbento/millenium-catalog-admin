from unittest import TestCase
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.application.use_cases.list_cast_members import (
    CastMemberOutput,
    ListCastMembersInput,
    ListCastMembersOutput,
    ListCastMembersUseCase,
)
from src.core.cast_member.infra.cast_member_in_memory_repository import (
    CastMemberInMemoryRepository,
)


class TestListCastMembers(TestCase):

    def setUp(self):
        self.cast_member_in_memory_repository = CastMemberInMemoryRepository()

        self.use_case = ListCastMembersUseCase(
            cast_member_repository=self.cast_member_in_memory_repository
        )

    def test_should_be_able_to_return_an_empty_cast_members_list(self):
        input = ListCastMembersInput()

        output = self.use_case.execute(input)

        assert output == ListCastMembersOutput(data=[])

    def test_should_be_able_to_return_an_cast_members_list(self):
        cast_member1 = CastMember(name="John Doe", type=CastMemberType.ACTOR)
        cast_member2 = CastMember(name="Herlander Bento", type=CastMemberType.ACTOR)

        self.cast_member_in_memory_repository.insert(cast_member1)
        self.cast_member_in_memory_repository.insert(cast_member2)

        output = self.use_case.execute(ListCastMembersInput())

        assert output == ListCastMembersOutput(
            data=[
                CastMemberOutput(
                    id=cast_member1.id, name=cast_member1.name, type=cast_member1.type
                ),
                CastMemberOutput(
                    id=cast_member2.id, name=cast_member2.name, type=cast_member2.type
                ),
            ]
        )
