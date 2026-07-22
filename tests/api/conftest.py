import uuid

import pytest
from api.client import APIClient
from api.endpoints.pet import PetEndpoint


@pytest.fixture(scope="session")
def api_client(base_url):
    return APIClient(base_url)


@pytest.fixture(scope="session")
def pet_endpoint(api_client):
    return PetEndpoint(api_client)


@pytest.fixture
def sample_pet(pet_endpoint):
    pet = {
        "id": uuid.uuid4().int >> 96,
        "name": "Buddy",
        "status": "available",
        "photoUrls": ["https://example.com/photo.jpg"],
        "category": {"id": 1, "name": "Dogs"},
        "tags": [{"id": 1, "name": "friendly"}],
    }
    yield pet
    try:
        pet_endpoint.delete(pet["id"])
    except Exception:
        pass
