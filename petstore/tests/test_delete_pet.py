import allure
import pytest


@allure.feature("Pet CRUD")
@allure.story("Delete Pet")
@pytest.mark.api
@pytest.mark.regression
class TestDeletePet:
    @allure.title("Delete pet by ID")
    def test_delete_pet(self, pet_endpoint, sample_pet):
        pet_endpoint.create(sample_pet)
        result, status = pet_endpoint.delete(sample_pet["id"])
        assert status == 200
        assert result["message"] == str(sample_pet["id"])

    @allure.title("Delete non-existent pet returns 404")
    def test_delete_nonexistent_pet(self, pet_endpoint):
        result, status = pet_endpoint.delete(999999999)
        assert status == 404
