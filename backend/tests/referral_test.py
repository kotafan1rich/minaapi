from httpx import AsyncClient


class ReferralTest:
    async def create_get_referral_test(self, client: AsyncClient):
        password = "string"
        data = {
            "password": password,
        }
        for _ in range(3):
            user_response = await client.post("users/create_user", json=data)
            assert user_response.status_code == 200
        id_from = 1
        id_to1 = 2
        id_to2 = 3
        params = {"id_from": id_from, "id_to": id_to1}
        create_response = await client.post("referrals/create_referral", params=params)
        assert create_response.status_code == 200
        create_json = create_response.json()
        assert create_json.get("id_from") == id_from
        assert create_json.get("id_to") == id_to1

        params = {"id_from": id_from, "id_to": id_to2}
        create_response = await client.post("referrals/create_referral", params=params)
        assert create_response.status_code == 200

        params = {"id_from": id_from}
        get_response = await client.get("referrals/get_referrals", params=params)
        assert get_response.status_code == 200
        get_json = get_response.json().get("result")

        assert id_to1 in get_json
        assert id_to2 in get_json
