import allure
import pytest


@allure.feature("Pet CRUD")
@allure.story("Update Pet")
@pytest.mark.api
@pytest.mark.regression
class TestUpdatePet:
    @allure.title("Update pet status to sold")
    def test_update_pet(self, pet_endpoint, sample_pet):
        pet_endpoint.create(sample_pet)
        updated = {**sample_pet, "status": "sold"}
        result, status = pet_endpoint.update(updated)
        assert status == 200
        assert result["status"] == "sold"

    @allure.title("Update pet name")
    def test_update_pet_name(self, pet_endpoint, sample_pet):
        pet_endpoint.create(sample_pet)
        updated = {**sample_pet, "name": "Max"}
        result, status = pet_endpoint.update(updated)
        assert status == 200
        assert result["name"] == "Max"
