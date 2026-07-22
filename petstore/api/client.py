import requests
import allure
from config.settings import BASE_URL, API_KEY, WAIT_TIMEOUT


class APIClient:
    def __init__(self, base_url: str | None = None):
        self.base_url = base_url or BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
        })

    def _inject_api_key(self, kwargs: dict) -> dict:
        if API_KEY and API_KEY != "your_api_key_here":
            kwargs["params"] = {**kwargs.get("params", {}), "api_key": API_KEY}
        kwargs.setdefault("timeout", WAIT_TIMEOUT)
        return kwargs

    @allure.step("Send GET request to {endpoint}")
    def get(self, endpoint: str, **kwargs) -> requests.Response:
        return self.session.get(f"{self.base_url}{endpoint}", **self._inject_api_key(kwargs))

    @allure.step("Send POST request to {endpoint}")
    def post(self, endpoint: str, **kwargs) -> requests.Response:
        return self.session.post(f"{self.base_url}{endpoint}", **self._inject_api_key(kwargs))

    @allure.step("Send PUT request to {endpoint}")
    def put(self, endpoint: str, **kwargs) -> requests.Response:
        return self.session.put(f"{self.base_url}{endpoint}", **self._inject_api_key(kwargs))

    @allure.step("Send DELETE request to {endpoint}")
    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        return self.session.delete(f"{self.base_url}{endpoint}", **self._inject_api_key(kwargs))
