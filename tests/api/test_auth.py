import allure
from tests.builders.user_builder import UserBuilder
from tests.client.auth_client import AuthClient
from tests.schemas.auth import LoginResponseSchema, ErrorResponseSchema


@allure.epic('Авторизация')
@allure.feature('Регистрация и вход в систему')
class TestAuth:

    @allure.title('Регистрация пользователя')
    @allure.step('Регистрация уникального пользователя и проверка ответа')
    def test_register_unique_user_success(self, auth_client, clean_up_register):
        user_data = UserBuilder().build()
        response = auth_client.register(user_data)

        assert isinstance(response, LoginResponseSchema)
        assert response.success is True
        assert response.user.email == user_data.email
        assert response.user.name == user_data.name
        assert response.access_token is not None
        assert response.refresh_token is not None

        clean_up_register(response.access_token)

    @allure.title('Попытка регистрации существующего пользователя')
    @allure.step('Попытка повторной регичтрации пользователя и проверка ошибки')
    def test_register_existing_user(self, auth_client, unique_user):
        existing_user = UserBuilder().with_email(unique_user['email']).with_password('any_password').with_name('Any').build()
        response = auth_client.register(existing_user)

        assert isinstance(response, ErrorResponseSchema)
        assert response.success is False
        assert response.message == 'User already exists'

    @allure.title('Успешная авторизация пользователя')
    @allure.step('Авторизация зарегистрированного пользователя и проверка ответа')
    def test_login_existig_user_success(self, auth_client, unique_user):
        creds = UserBuilder().with_email(unique_user['email']).with_password(unique_user['password']).build()
        response = auth_client.login(creds)

        assert isinstance(response, LoginResponseSchema)
        assert response.success is True
        assert response.user.email == unique_user['email']
        assert response.access_token is not None
        assert response.refresh_token is not None

    @allure.title('Авторизация с несуществующими данными')
    @allure.step('Попытка авторизации с несуществующими данными и проверка ошибки')
    def test_login_invalid_creds(self, auth_client):
        invalid_creds = UserBuilder().with_email('non_existing@example.com').with_password('wrong_password').build()
        response = auth_client.login(invalid_creds)

        assert isinstance(response, ErrorResponseSchema)
        assert response.success is False
        assert response.message == 'email or password are incorrect'
        