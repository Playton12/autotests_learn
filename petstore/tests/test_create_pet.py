import allure
import pytest
from petstore.schemas.pet_schema import PetSchema


@allure.feature("Pet CRUD")
@allure.story("Create Pet")
@pytest.mark.api
@pytest.mark.smoke
class TestCreatePet:
    @allure.title("Create a new pet successfully")
    def test_create_pet(self, pet_endpoint, sample_pet):
        result, status = pet_endpoint.create(sample_pet)
        assert status == 200
        assert result["name"] == sample_pet["name"]
        assert result["status"] == sample_pet["status"]

    @allure.title("Validate created pet with Pydantic schema")
    @pytest.mark.regression
    def test_create_pet_schema(self, pet_endpoint, sample_pet):
        result, status = pet_endpoint.create(sample_pet)
        assert status == 200
        pet = PetSchema(**result)
        assert pet.name == sample_pet["name"]
