from httpx import AsyncClient


class UserTest:
    async def create_user_test(self, client: AsyncClient):
        data = {
            "tg_id": 1,
            "tg_username": "string",
            "email": "user@example.com",
            "password": "string",
        }
        create_response = await client.post("users/create_user", json=data)
        assert create_response.status_code == 200
        create_json = create_response.json()
        assert create_json.get("id") == 1
        assert create_json.get("tg_id") == data.get("tg_id")
        assert create_json.get("tg_username") == data.get("tg_username")
        assert create_json.get("email") == data.get("email")
        assert create_json.get("hashed_password") is not None
