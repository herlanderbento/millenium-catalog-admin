from unittest.mock import create_autospec
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.application.use_cases.list_cast_members import (
    CastMemberOutput,
    ListCastMembersInput,
    ListCastMembersOutput,
    ListCastMembersUseCase,
)
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


class TestListCastMembers:
    def test_should_be_able_to_return_an_empty_cast_members_list(self):
        cast_member_mock_repository = create_autospec(CastMemberRepository)
        use_case = ListCastMembersUseCase(
            cast_member_repository=cast_member_mock_repository
        )
        output = use_case.execute(ListCastMembersInput())

        assert output == ListCastMembersOutput(data=[])

    def test_should_be_able_to_return_an_cast_members_list(self):
        cast_member1 = CastMember(
            name="John Doe",
            type=CastMemberType.ACTOR,
        )
        cast_member2 = CastMember(
            name="Herlander Bento",
            type=CastMemberType.DIRECTOR,
        )

        cast_member_mock_repository = create_autospec(CastMemberRepository)
        cast_member_mock_repository.findAll.return_value = [cast_member1, cast_member2]

        use_case = ListCastMembersUseCase(
            cast_member_repository=cast_member_mock_repository
        )

        output = use_case.execute(ListCastMembersInput())

        assert output == ListCastMembersOutput(
            data=[
                CastMemberOutput(
                    id=cast_member1.id,
                    name=cast_member1.name,
                    type=cast_member1.type.value,
                ),
                CastMemberOutput(
                    id=cast_member2.id,
                    name=cast_member2.name,
                    type=cast_member2.type.value,
                ),
            ]
        )
