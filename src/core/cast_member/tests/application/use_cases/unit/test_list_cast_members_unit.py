from unittest.mock import create_autospec
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.application.use_cases.list_cast_members import (
    CastMemberOutput,
    ListCastMembersInput,
    ListCastMembersOutput,
    ListCastMembersUseCase,
)
from src.core.cast_member.domain.cast_member_repository import (
    CastMemberRepository,
    CastMemberSearchResult,
)


class TestListCastMembers:
    def test_should_be_able_to_return_an_empty_cast_members_list(self):
        cast_member_mock_repository = create_autospec(CastMemberRepository)
        cast_member_mock_repository.search.return_value = CastMemberSearchResult(
            items=[], total=0, current_page=1, per_page=10
        )
        use_case = ListCastMembersUseCase(
            cast_member_repository=cast_member_mock_repository
        )
        output = use_case.execute(ListCastMembersInput())

        total = 0
        per_page = 10
        last_page = 0 if per_page == 0 else (total + per_page - 1) // per_page

        expected_output = ListCastMembersOutput(
            items=[],
            total=0,
            current_page=1,
            per_page=10,
            last_page=last_page,
        )
        assert output == expected_output

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
        cast_member_mock_repository.search.return_value = CastMemberSearchResult(
            items=[cast_member1, cast_member2],
            total=2,
            current_page=1,
            per_page=10,
        )

        use_case = ListCastMembersUseCase(
            cast_member_repository=cast_member_mock_repository
        )

        output = use_case.execute(ListCastMembersInput())

        expected_output = ListCastMembersOutput.from_search_result(
            items=[
                CastMemberOutput.from_entity(cast_member1),
                CastMemberOutput.from_entity(cast_member2),
            ],
            result=CastMemberSearchResult(
                items=[cast_member1, cast_member2], total=2, current_page=1, per_page=10
            ),
        )

        assert output == expected_output
