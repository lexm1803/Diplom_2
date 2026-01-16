import pytest
import os
from tests.client.auth_client import AuthClient
from tests.client.user_client import UserClient
from tests.client.orders_client import OrdersClient
from tests.builders.user_builder import UserBuilder


@pytest.fixture(scope = 'session')
def api_base_url():
    return os.getenv('API_BASE_URL', 'https://stellarburgers.education-services.ru')

@pytest.fixture
def auth_client(api_base_url):
    return AuthClient(base_url = api_base_url)

@pytest.fixture
def user_client(api_base_url):
    return UserClient(base_url = api_base_url)

@pytest.fixture
def orders_client(api_base_url):
    return OrdersClient(base_url = api_base_url)

@pytest.fixture
def unique_user(auth_client, user_client):
    user_data = UserBuilder().build()
    
    register_response = auth_client.register(user_data)
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
    except Exception as e:
        print(f'Ошибка при попытке удаления пользователя: \n{e}')
