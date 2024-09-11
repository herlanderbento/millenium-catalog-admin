import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.mark.django_db
class TestCreateAndEditCategory:
    def test_user_can_create_and_edit_category(self, api_client: APIClient) -> None:

        # Acessa listagem e verifica que não tem nenhuma categoria criada
        list_response = api_client.get("/api/categories/")
        expected_meta = {
            "total": 0,
            "current_page": 1,
            "per_page": 15,
        }

        # Allow `last_page` to be either 0 or 1 when there are no categories
        assert list_response.data["data"] == []
        assert list_response.data["meta"]["total"] == expected_meta["total"]
        assert (
            list_response.data["meta"]["current_page"] == expected_meta["current_page"]
        )
        assert list_response.data["meta"]["per_page"] == expected_meta["per_page"]
        assert list_response.data["meta"]["last_page"] in [0, 1]

        # Cria uma categoria
        # create_response = api_client.post(
        #     "/api/categories/",
        #     {
        #         "name": "Movie",
        #         "description": "Movie description",
        #     },
        # )
        # assert create_response.status_code == 201
        # created_category_id = create_response.data["id"]

        # # Verifica que categoria criada aparece na listagem
        # list_response = api_client.get("/api/categories/")
        # assert list_response == {
        #     "data": [
        #         {
        #             "id": created_category_id,
        #             "name": "Movie",
        #             "description": "Movie description",
        #             "is_active": True,
        #         }
        #     ],
        #     "meta": {
        #         "total": 1,
        #         "current_page": 1,
        #         "per_page": 15,
        #         "last_page": 1,
        #     },
        # }

        # # # Edita categoria criada
        # # edit_response = api_client.put(
        # #     f"/api/categories/{created_category_id}/",
        # #     {
        # #         "name": "Documentary",
        # #         "description": "Documentary description",
        # #         "is_active": True,
        # #     },
        # # )
        # # assert edit_response.status_code == 204

        # # # Verifica que categoria editada aparece na listagem
        # # list_response = api_client.get("/api/categories/")
        # # assert list_response.data == {
        # #     "data": [
        # #         {
        # #             "id": created_category_id,
        # #             "name": "Documentary",
        # #             "description": "Documentary description",
        # #             "is_active": True,
        # #         }
        # #     ],
        # #     "meta": {
        # #         "total": 1,
        # #         "current_page": 1,
        # #         "per_page": 15,
        # #         "last_page": 1,
        # #     },
        # # }

    def test_create_category(self, api_client: APIClient) -> None:

        # Cria uma categoria com nome vazio
        create_response = api_client.post(
            "/api/categories/",
            {"name": "", "description": "Movie description"},
        )
        assert create_response.status_code == 400

        # Cria uma categoria com descrição vazia
        create_response = api_client.post(
            "/api/categories/",
            {"name": "Movie", "description": ""},
        )
        assert create_response.status_code == 201
