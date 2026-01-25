import pytest
from tests.client.auth_client import AuthClient
from tests.client.user_client import UserClient
from tests.client.orders_client import OrdersClient
from tests.builders.user_builder import UserBuilder


BASE_URL = 'https://stellarburgers.education-services.ru'

@pytest.fixture
def auth_client():
    return AuthClient(base_url = BASE_URL)

@pytest.fixture
def user_client():
    return UserClient(base_url = BASE_URL)

@pytest.fixture
def orders_client():
    return OrdersClient(base_url = BASE_URL)

@pytest.fixture
def unique_user(auth_client, user_client):
    user_data = UserBuilder().build()
    
    register_response, _ = auth_client.register(user_data)
    access_token = register_response.access_token
    refresh_token = register_response.refresh_token
    
    yield {
        'email': user_data.email,
        'password': user_data.password,
        'name': user_data.name,
        'access_token': access_token,
        'refresh_token': refresh_token
    }

    try:
        user_client.delete_user(auth_token = access_token)
    except Exception:
        pass

@pytest.fixture
def clean_up_register(user_client):
    access = []
    
    def register(token):
        access.append(token)
        return access
    
    yield register
    
    try:
        user_client.delete_user(auth_token = access[0])
    except Exception:
        pass