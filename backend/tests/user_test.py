from httpx import AsyncClient


class UserTest:
    async def create_get_user_test(self, client: AsyncClient):
        tg_id = 1
        tg_username = "string"
        email = "user@example.com"
        password = "string"
        data = {
            "tg_id": tg_id,
            "tg_username": tg_username,
            "email": email,
            "password": password,
        }
        create_response = await client.post("users/create_user", json=data)
        assert create_response.status_code == 200
        create_json = create_response.json()
        assert create_json.get("id") == 1
        assert create_json.get("tg_id") == tg_id
        assert create_json.get("tg_username") == tg_username
        assert create_json.get("email") == email
        assert create_json.get("hashed_password") is not None

        params = {"id": 1}
        get_response = await client.get("users/get_user", params=params)
        get_json = get_response.json()
        assert get_json.get("id") == 1
        assert get_json.get("tg_id") == tg_id
        assert get_json.get("tg_username") == tg_username
        assert get_json.get("email") == email
        assert get_json.get("hashed_password") is not None
