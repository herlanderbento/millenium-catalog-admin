import uuid
import pytest
from django.test import TestCase
from rest_framework import status

from src.django_project.cast_member_app.repository import CastMemberDjangoRepository
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType


@pytest.mark.django_db
class TestCreateCastMemberAPI(TestCase):

    def test_should_be_able_a_cast_member(self):
        url = "/api/cast-members/"

        data = {"name": "John Doe", "type": "ACTOR"}
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_should_be_able_return_400_when_missing_required_fields(self):
        url = "/api/cast-members/"

        data = {"type": "ACTOR"}
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestGetCastMemberAPI(TestCase):
    def setUp(self):
        self.cast_member = CastMember(
            name="John Doe",
            type=CastMemberType.ACTOR,
        )
        cast_member_repository = CastMemberDjangoRepository()
        cast_member_repository.insert(self.cast_member)

    def test_should_be_able_to_get_cast_member(
        self,
    ) -> None:

        url = f"/api/cast-members/{self.cast_member.id}/"
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            "data": {
                "id": str(self.cast_member.id),
                "name": "John Doe",
                "type": "ACTOR",
                "created_at": self.cast_member.created_at.isoformat(),
            }
        }

    def test_should_be_able_return_404_when_cast_member_does_not_exist(self) -> None:

        url = f"/api/cast-members/{uuid.uuid4()}/"
        response = self.client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_should_be_able_return_400_when_cast_member_id_is_invalid(self) -> None:

        url = f"/api/cast-members/invalid_uuid/"
        response = self.client.get(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestListCastMembersAPI(TestCase):

    def setUp(self):

        self.cast_member1 = CastMember(
            name="John Doe",
            type=CastMemberType.ACTOR,
        )
        self.cast_member2 = CastMember(
            name="Jane Doe",
            type=CastMemberType.DIRECTOR,
        )

        cast_member_repository = CastMemberDjangoRepository()
        cast_member_repository.insert(self.cast_member1)
        cast_member_repository.insert(self.cast_member2)

    def test_should_be_able_to_get_cast_members_list(self) -> None:

        url = "/api/cast-members/"
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["data"] == [
            {
                "id": str(self.cast_member1.id),
                "name": "John Doe",
                "type": "ACTOR",
                "created_at": self.cast_member1.created_at.isoformat(),
            },
            {
                "id": str(self.cast_member2.id),
                "name": "Jane Doe",
                "type": "DIRECTOR",
                "created_at": self.cast_member2.created_at.isoformat(),
            },
        ]


@pytest.mark.django_db
class TestUpdateCastMemberAPI(TestCase):

    def setUp(self):
        self.cast_member = CastMember(
            name="John Doe",
            type=CastMemberType.ACTOR,
        )
        cast_member_repository = CastMemberDjangoRepository()
        cast_member_repository.insert(self.cast_member)

    def test_should_be_able_to_update_cast_member(self) -> None:
        url = f"/api/cast-members/{self.cast_member.id}/"
        data = {"name": "John Doe", "type": "ACTOR"}
        response = self.client.put(url, data, content_type="application/json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["data"] == {
            "id": str(self.cast_member.id),
            "name": "John Doe",
            "type": "ACTOR",
            "created_at": self.cast_member.created_at.isoformat(),
        }

    def test_should_be_able_return_404_when_cast_member_does_not_exist(self) -> None:

        url = f"/api/cast-members/{uuid.uuid4()}/"
        data = {"name": "John Doe", "type": "ACTOR"}

        response = self.client.put(url, data, content_type="application/json")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_should_be_able_return_400_when_missing_required_fields(self):
        url = f"/api/cast-members/{self.cast_member.id}/"

        data = {"type": "ACTOR"}
        response = self.client.put(url, data, content_type="application/json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestDeleteCastMemberAPI(TestCase):

    def setUp(self):

        self.cast_member = CastMember(
            name="John Doe",
            type=CastMemberType.ACTOR,
        )
        cast_member_repository = CastMemberDjangoRepository()
        cast_member_repository.insert(self.cast_member)

    def test_should_be_able_to_delete_cast_member(self) -> None:

        url = f"/api/cast-members/{self.cast_member.id}/"
        response = self.client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_should_be_able_return_404_when_cast_member_does_not_exist(self) -> None:

        url = f"/api/cast-members/{uuid.uuid4()}/"
        response = self.client.delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_should_be_able_return_400_when_cast_member_id_is_invalid(self) -> None:

        url = f"/api/cast-members/invalid_uuid/"
        response = self.client.delete(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
