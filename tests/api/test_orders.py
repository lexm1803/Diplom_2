import allure
from tests.client.orders_client import OrdersClient
from tests.schemas.orders import CreateOrderRequestSchema, GetUserOrdersResponseSchema
from tests.schemas.auth import ErrorResponseSchema


@allure.epic('Заказы')
@allure.feature('Создание и получение заказа')
class TestOrders:

    @allure.title('Создание заказа')
    @allure.step('Создание заказа с валидными ингредиентами и токеном')
    def test_create_order_with_auth_success(self, orders_client, unique_user):
        ingredient_response = orders_client.get_ingredients()
        valid_ids = [ing.id for ing in ingredient_response.data[:2]]
        ingredients = CreateOrderRequestSchema(ingredients = valid_ids)
        response = orders_client.create_order(
            auth_token = unique_user['access_token'],
            ingredients = ingredients
            )
        
        assert hasattr(response, 'order')
        assert response.order.number > 0

    @allure.title('Создание заказа с пустым списком ингредиентов')
    @allure.step('Попытка создания заказа без ингредиентов')
    def test_create_order_with_empty_ingredients_fails(self, orders_client, unique_user):
        ingredients = CreateOrderRequestSchema(ingredients = [])
        response = orders_client.create_order(
            auth_token = unique_user['access_token'],
            ingredients = ingredients
        )

        assert isinstance(response, ErrorResponseSchema)
        assert response.message == 'Ingredient ids must be provided'
        assert response.success is False

    @allure.title('Создание заказа с неверным хэшем ингредиентов')
    @allure.step('Попытка создания заказа с неверным id ингредиентов')
    def test_create_order_with_invalid_id_ingredients(self, orders_client, unique_user):
        ingredients = CreateOrderRequestSchema(ingredients = ['invalid_id_1'])
        response = orders_client.create_order(
            auth_token = unique_user['access_token'],
            ingredients = ingredients
            )

        assert isinstance(response, ErrorResponseSchema)
        assert response.message == 'One or more ids provided are incorrect'
        assert response.success is False

    @allure.title('Получение заказов авторизованным пользователем')
    @allure.step('Получение списка заказов с валидным токеном')
    def test_get_user_orders_with_auth_success(self, orders_client, unique_user):
        ingredient_response = orders_client.get_ingredients()
        valid_id = ingredient_response.data[0].id
        ingredients = CreateOrderRequestSchema(ingredients = [valid_id])
        orders_client.create_order(
            auth_token = unique_user['access_token'],
            ingredients = ingredients
        )
        response = orders_client.get_user_orders(
            auth_token = unique_user['access_token'],
            )
        
        assert isinstance(response, GetUserOrdersResponseSchema)
        assert response.success is True
        assert isinstance(response.orders, list)
        assert response.total > 0

    @allure.title('Получение заказов без авторизации')
    @allure.step('Получение списка заказов без токена авторизации')
    def test_get_user_orders_without_auth_fails(self, orders_client: OrdersClient):
        response = orders_client.get_user_orders(auth_token = None)

        assert isinstance(response, ErrorResponseSchema)
        assert response.success is False
        assert response.message == 'You should be authorised'
        