from httpx import AsyncClient

class PromoPositiveTest:
    async def create_get_promo_test(self, client: AsyncClient):
        description = "test"
        params = {"description": description}
        response_create = await client.post("promos/create_promo", params=params)
        response_create_json = response_create.json()
        assert response_create.status_code == 200
        assert response_create_json.get("description") == description

        id = response_create_json.get("id")
        params = {
            "id": id
        }
        response_get = await client.get("promos/get_promo", params=params)
        assert response_get.status_code == 200
        response_get_json = response_get.json()
        assert response_get_json.get("id")
        assert response_get_json.get("description") == description


class PromoNegativeTest:
    async def create_promo_test(self, client: AsyncClient):
        params = {"description": ""}
        response_create = await client.post("promos/create_promo", params=params)
        assert response_create.status_code == 422
    
    async def get_promo_test(self, client: AsyncClient):
        params = {
            "id": 10
        }
        response_get = await client.get("promos/get_promo", params=params)
        assert response_get.status_code == 404
