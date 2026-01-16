import allure
from tests.builders.user_builder import UserBuilder
from tests.client.user_client import UserClient
from tests.schemas.auth import (
    UpdateUserRequestSchema,
    UserFullResponseSchema,
    ErrorResponseSchema
)


@allure.epic('Профиль пользователя')
@allure.feature('Управление данными пользователя')
class TestUser:

    @allure.title('Обновление имени пользователя')
    @allure.step('Изменение имени пользователя с валидным токеном')
    def test_update_user_with_auth_success(self, user_client, unique_user):
        update_data = UpdateUserRequestSchema(name = 'Update_name')
        response = user_client.update_user(
            auth_token = unique_user['access_token'],
            update_data = update_data
        )

        assert isinstance(response, UserFullResponseSchema) 
        assert response.user.name == 'Update_name'
        assert response.user.email == unique_user['email']
        
    @allure.title('Обновление email пользователя')
    @allure.step('Изменение email пользователя с валидным токеном')
    def test_update_user_email_with_auth_success(self, user_client, unique_user):
        update_email = UserBuilder().with_unique_email().email
        update_data = UpdateUserRequestSchema(email = update_email)
        response = user_client.update_user(
            auth_token = unique_user['access_token'],
            update_data = update_data
        )

        assert isinstance(response, UserFullResponseSchema)
        assert response.user.email == update_email
        assert response.user.name == unique_user['name']

    @allure.title('Обновление пароля пользователя')
    @allure.step('Изменение пароля пользователя с валидным токеном')
    def test_update_user_password_with_auth_success(self, user_client, unique_user):
        update_password = 'New_password'
        update_data = UpdateUserRequestSchema(password = update_password)
        response= user_client.update_user(
            auth_token = unique_user['access_token'],
            update_data = update_data
        )

        assert isinstance(response, UserFullResponseSchema)
        assert response.user.email == unique_user['email']
        assert response.user.name == unique_user['name']
        assert response.success is True
        
    @allure.title('Обновление без авторизации')
    @allure.step('Попытка обновления данных без авторизации пользователя')
    def test_update_user_without_auth_fails(self, user_client):
        update_data = UpdateUserRequestSchema(name = 'Unknow')
        response = user_client.update_user(
            auth_token = None,
            update_data = update_data
        )

        assert isinstance(response, ErrorResponseSchema)
        assert response.success is False
        assert response.message == 'You should be authorised'

    @allure.title('Получение данных пользователя с авторизацией')
    @allure.step('Получение профиля пользователя с валидным токеном')
    def test_get_user_with_auth_success(self, user_client, unique_user):
        response = user_client.get_user(
            auth_token = unique_user['access_token']
        )

        assert isinstance(response, UserFullResponseSchema)
        assert response.user.email == unique_user['email']
        assert response.user.name == unique_user['name']
        assert response.success is True

    @allure.title('Получение данных пользователя без авторизации')
    @allure.step('Попытка получения профиля пользователя без авторизации и проверка ошибки')
    def test_get_user_without_auth_fails(self, user_client):
        response = user_client.get_user(
            auth_token = None
        )

        assert isinstance(response, ErrorResponseSchema)
        assert response.success is False
        assert response.message == 'You should be authorised'
        