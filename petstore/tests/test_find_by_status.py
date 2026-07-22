import allure
import pytest


@allure.feature("Pet CRUD")
@allure.story("Find Pets by Status")
@pytest.mark.api
@pytest.mark.regression
class TestFindByStatus:
    @allure.title("Find pets by status 'available'")
    def test_find_by_available(self, pet_endpoint, sample_pet):
        pet_endpoint.create(sample_pet)
        result, status = pet_endpoint.find_by_status("available")
        assert status == 200
        assert isinstance(result, list)
        assert any(pet["id"] == sample_pet["id"] for pet in result)

    @allure.title("Find pets by status 'sold'")
    def test_find_by_sold(self, pet_endpoint):
        result, status = pet_endpoint.find_by_status("sold")
        assert status == 200
        assert isinstance(result, list)

    @allure.title("Find pets by invalid status returns 400")
    def test_find_by_invalid_status(self, pet_endpoint):
        result, status = pet_endpoint.find_by_status("invalid_status")
        assert status == 400
