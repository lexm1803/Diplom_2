import allure
from tests.builders.user_builder import UserBuilder
from tests.schemas.auth import LoginResponseSchema, ErrorResponseSchema


@allure.epic('Авторизация')
@allure.feature('Регистрация и вход в систему')
class TestAuth:

    @allure.title('Регистрация пользователя')
    @allure.step('Регистрация уникального пользователя и проверка ответа')
    def test_register_unique_user_success(self, auth_client, clean_up_register):
        user_data = UserBuilder().build()
        response, status_code = auth_client.register(user_data)

        assert isinstance(response, LoginResponseSchema)
        assert response.success is True
        assert response.user.email == user_data.email
        assert response.user.name == user_data.name
        assert response.access_token is not None
        assert response.refresh_token is not None
        assert status_code == 200

        clean_up_register(response.access_token)

    @allure.title('Попытка регистрации существующего пользователя')
    @allure.step('Попытка повторной регичтрации пользователя и проверка ошибки')
    def test_register_existing_user(self, auth_client, unique_user):
        existing_user = UserBuilder().with_email(unique_user['email']).with_password('any_password').with_name('Any').build()
        response, status_code = auth_client.register(existing_user)

        assert isinstance(response, ErrorResponseSchema)
        assert response.success is False
        assert response.message == 'User already exists'
        assert status_code == 403

    @allure.title('Попытка регистрации без обязательного поля')
    @allure.step('Попытка регистрации пользователя без заполнения обязательного поля и проверка ошибки')
    def test_register_missing_required_fild_fails(self, auth_client):
        invalod_data = UserBuilder().with_unique_password().with_unique_name().build_invalid_user()
        response, status_code = auth_client.register(invalod_data)

        assert isinstance(response, ErrorResponseSchema)
        assert response.success is False
        assert response.message == 'Email, password and name are required fields'
        assert status_code == 403

    @allure.title('Успешная авторизация пользователя')
    @allure.step('Авторизация зарегистрированного пользователя и проверка ответа')
    def test_login_existig_user_success(self, auth_client, unique_user):
        creds = UserBuilder().with_email(unique_user['email']).with_password(unique_user['password']).build()
        response, status_code = auth_client.login(creds)

        assert isinstance(response, LoginResponseSchema)
        assert response.success is True
        assert response.user.email == unique_user['email']
        assert response.access_token is not None
        assert response.refresh_token is not None
        assert status_code == 200

    @allure.title('Авторизация с несуществующими данными')
    @allure.step('Попытка авторизации с несуществующими данными и проверка ошибки')
    def test_login_invalid_creds(self, auth_client):
        invalid_creds = UserBuilder().with_email('non_existing@example.com').with_password('wrong_password').build()
        response, status_code = auth_client.login(invalid_creds)

        assert isinstance(response, ErrorResponseSchema)
        assert response.success is False
        assert response.message == 'email or password are incorrect'
        assert status_code == 401
        