import aiohttp
import logging

_LOGGER = logging.getLogger(__name__)

BASE_URL = "https://www.cloudinverter.net/dist/server/api/CodeIgniter/index.php/Senergytec/web/v2/Inverterapi/"

class CloudInverterApiClient:
    def __init__(self, username, password, sign, goods_id, datasign, session: aiohttp.ClientSession):
        self.username = username
        self.password = password
        self.sign = sign
        self.goods_id = goods_id
        self.datasign = datasign
        self.session = session
        self.token = None
        self.member_auto_id = None

    async def async_login(self) -> bool:
        url = f"{BASE_URL}UserLogin_v1"
        payload = {
            "sign": self.sign,
            "MemberID": self.username,
            "Password": self.password,
            "remember": True,
            "type": "1"
        }
        headers = {
            "Content-Type": "application/json",
            "Cookie": "timezone=Europe%2FAthens"
        }
        async with self.session.post(url, json=payload, headers=headers) as response:
            data = await response.json()
            if data.get("status") == "ok" and "token" in data:
                self.token = data["token"]
                self.member_auto_id = data.get("MemberAutoID")
                _LOGGER.debug("CloudInverter login succeeded.")
                return True
            raise Exception(f"Login failed: {data.get('message', 'Unknown error')}")

    async def _authenticated_post(self, endpoint: str):
        if not self.token:
            await self.async_login()

        url = f"{BASE_URL}{endpoint}"
        payload = {
            "sign": self.datasign,
            "GoodsID": self.goods_id,
            "MemberAutoID": self.member_auto_id
        }
        headers = {
            "Authorization": self.token,
            "Content-Type": "application/json",
            "Cookie": "timezone=Europe%2FAthens"
        }
        async with self.session.post(url, json=payload, headers=headers) as response:
            if response.status == 401:  # Token expired, retry once
                await self.async_login()
                headers["Authorization"] = self.token
                async with self.session.post(url, json=payload, headers=headers) as retry_response:
                    return await retry_response.json()
            return await response.json()

    async def async_get_hybrid_flowgraph(self):
        return await self._authenticated_post("getHybridFlowgraph")

    async def async_get_detail_info(self):
        return await self._authenticated_post("InverterDetailInfoNewone")
