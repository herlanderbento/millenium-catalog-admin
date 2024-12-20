import uuid
import pytest
from rest_framework.test import APIClient
from rest_framework import status

from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.django_project.cast_member_app.repository import CastMemberDjangoRepository


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.mark.django_db
class TestCreateCastMemberAPI:
    def test_should_be_able_a_cast_member(self, api_client: APIClient):
        response = api_client.post(
            "/api/cast-members/",
            {
                "name": "John Doe",
                "type": "ACTOR",
            },
        )
        assert response.status_code == status.HTTP_201_CREATED

    def test_should_be_able_return_400_when_missing_required_fields(
        self, api_client: APIClient
    ):
        response = api_client.post(
            "/api/cast-members/",
            {
                "type": "ACTOR",
            },
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestGetCastMemberAPI:
    def test_should_be_able_to_get_cast_member(
        self,
        api_client: APIClient,
    ) -> None:
        cast_member = CastMember(name="John Doe", type="ACTOR")
        cast_member_repository = CastMemberDjangoRepository()
        cast_member_repository.insert(cast_member)

        response = api_client.get(f"/api/cast-members/{cast_member.id.value}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            "data": {
                "id": cast_member.id.value,
                "name": "John Doe",
                "type": "ACTOR",
                "created_at": cast_member.created_at.isoformat(),
            }
        }

    def test_should_be_able_return_404_when_cast_member_does_not_exist(
        self,
        api_client: APIClient,
    ) -> None:

        response = api_client.get(f"/api/cast-members/{uuid.uuid4()}/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_should_be_able_return_400_when_cast_member_id_is_invalid(
        self, api_client: APIClient
    ) -> None:

        response = api_client.get(f"/api/cast-members/invalid_uuid/")

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestListCastMembersAPI:

    def test_should_be_able_to_get_cast_members_list(
        self, api_client: APIClient
    ) -> None:
        cast_member_actor = CastMember(
            name="John Doe",
            type=CastMemberType.ACTOR,
        )
        cast_member_director = CastMember(
            name="Jane Doe",
            type=CastMemberType.DIRECTOR,
        )

        cast_member_repository = CastMemberDjangoRepository()
        cast_member_repository.insert(cast_member_actor)
        cast_member_repository.insert(cast_member_director)

        url = "/api/cast-members/"
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        sorted_response_data = sorted(response.data["data"], key=lambda x: x["id"])
        expected_data = [
            {
                "id": cast_member_actor.id.value,
                "name": "John Doe",
                "type": cast_member_actor.type.value,
                "created_at": cast_member_actor.created_at.isoformat(),
            },
            {
                "id": cast_member_director.id.value,
                "name": "Jane Doe",
                "type": cast_member_director.type.value,
                "created_at": cast_member_director.created_at.isoformat(),
            },
        ]
        sorted_expected_data = sorted(expected_data, key=lambda x: x["id"])
        assert sorted_response_data == sorted_expected_data


@pytest.mark.django_db
class TestUpdateCastMemberAPI:

    def test_should_be_able_to_update_cast_member(self, api_client: APIClient) -> None:
        cast_member = CastMember(
            name="John Doe",
            type=CastMemberType.DIRECTOR,
        )
        cast_member_repository = CastMemberDjangoRepository()
        cast_member_repository.insert(cast_member)

        response = api_client.put(
            f"/api/cast-members/{cast_member.id}/",
            {
                "name": "John Bentley",
                "type": "ACTOR",
            },
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            "data": {
                "id": cast_member.id.value,
                "name": "John Bentley",
                "type": "ACTOR",
                "created_at": cast_member.created_at.isoformat(),
            }
        }

    def test_should_be_able_return_404_when_cast_member_does_not_exist(
        self, api_client: APIClient
    ) -> None:

        response = api_client.put(
            f"/api/cast-members/{uuid.uuid4()}/",
            {
                "name": "John Doe",
                "type": "ACTOR",
            },
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_should_be_able_return_400_when_missing_required_fields(
        self, api_client: APIClient
    ):
        cast_member = CastMember(
            name="John Doe",
            type=CastMemberType.ACTOR,
        )
        cast_member_repository = CastMemberDjangoRepository()
        cast_member_repository.insert(cast_member)

        response = api_client.put(
            f"/api/cast-members/{cast_member.id}/",
            {
                "type": "ACTOR",
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestDeleteCastMemberAPI:

    def test_should_be_able_to_delete_cast_member(self, api_client: APIClient) -> None:
        cast_member = CastMember(
            name="John Doe",
            type=CastMemberType.ACTOR,
        )
        cast_member_repository = CastMemberDjangoRepository()
        cast_member_repository.insert(cast_member)

        response = api_client.delete(f"/api/cast-members/{cast_member.id}/")

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_should_be_able_return_404_when_cast_member_does_not_exist(
        self, api_client: APIClient
    ) -> None:

        response = api_client.delete(f"/api/cast-members/{uuid.uuid4()}/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_should_be_able_return_400_when_cast_member_id_is_invalid(
        self, api_client: APIClient
    ) -> None:

        response = api_client.delete(f"/api/cast-members/invalid_uuid/")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
