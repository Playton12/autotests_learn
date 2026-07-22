import allure
import pytest


@allure.feature("Pet CRUD")
@allure.story("Get Pet")
@pytest.mark.api
@pytest.mark.smoke
class TestGetPet:
    @allure.title("Get pet by ID")
    def test_get_pet(self, pet_endpoint, sample_pet):
        pet_endpoint.create(sample_pet)
        result, status = pet_endpoint.get_by_id(sample_pet["id"])
        assert status == 200
        assert result["id"] == sample_pet["id"]
        assert result["name"] == sample_pet["name"]

    @allure.title("Get non-existent pet returns 404")
    @pytest.mark.regression
    def test_get_nonexistent_pet(self, pet_endpoint):
        result, status = pet_endpoint.get_by_id(999999999)
        assert status == 404
        assert "message" in result
