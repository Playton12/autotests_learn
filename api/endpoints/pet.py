import json

import allure
from api.client import APIClient


class PetEndpoint:
    def __init__(self, client: APIClient):
        self.client = client
        self.endpoint = "/pet"

    @staticmethod
    def _parse_response(response) -> tuple[dict | list | None, int]:
        try:
            return response.json(), response.status_code
        except (json.JSONDecodeError, ValueError):
            return None, response.status_code

    @allure.step("Create pet")
    def create(self, pet_data: dict) -> tuple[dict | list | None, int]:
        response = self.client.post(self.endpoint, json=pet_data)
        return self._parse_response(response)

    @allure.step("Get pet by ID: {pet_id}")
    def get_by_id(self, pet_id: int) -> tuple[dict | list | None, int]:
        response = self.client.get(f"{self.endpoint}/{pet_id}")
        return self._parse_response(response)

    @allure.step("Update pet")
    def update(self, pet_data: dict) -> tuple[dict | list | None, int]:
        response = self.client.put(self.endpoint, json=pet_data)
        return self._parse_response(response)

    @allure.step("Delete pet by ID: {pet_id}")
    def delete(self, pet_id: int) -> tuple[dict | list | None, int]:
        response = self.client.delete(f"{self.endpoint}/{pet_id}")
        return self._parse_response(response)

    @allure.step("Find pets by status: {status}")
    def find_by_status(self, status: str) -> tuple[list | dict | None, int]:
        response = self.client.get(f"{self.endpoint}/findByStatus", params={"status": status})
        return self._parse_response(response)
