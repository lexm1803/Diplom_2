import allure
from tests.client.orders_client import OrdersClient
from tests.schemas.orders import (
    CreateOrderRequestSchema, 
    GetUserOrdersResponseSchema,
    CreateOrderResponseSchema,
    OrderResponseSchema,
    ListOrderSchema,
    )
from tests.schemas.auth import ErrorResponseSchema


@allure.epic('Заказы')
@allure.feature('Создание и получение заказа')
class TestOrders:

    @allure.title('Создание заказа')
    @allure.step('Создание заказа с валидными ингредиентами и токеном')
    def test_create_order_with_auth_success(self, orders_client, unique_user):
        ingredient_response, _ = orders_client.get_ingredients()
        valid_ids = [ing.id for ing in ingredient_response.data[:2]]
        ingredients = CreateOrderRequestSchema(ingredients = valid_ids)
        
        response, status_code = orders_client.create_order(
            auth_token = unique_user['access_token'],
            ingredients = ingredients
            )
        
        assert isinstance(response, CreateOrderResponseSchema)
        assert isinstance(response.order, OrderResponseSchema)
        assert response.success is True
        assert response.order.number > 0
        assert response.name is not None
        assert status_code == 200

    @allure.title('Создание заказа с пустым списком ингредиентов')
    @allure.step('Попытка создания заказа без ингредиентов')
    def test_create_order_with_empty_ingredients_fails(self, orders_client, unique_user):
        ingredients = CreateOrderRequestSchema(ingredients = [])
        
        response, status_code = orders_client.create_order(
            auth_token = unique_user['access_token'],
            ingredients = ingredients
        )

        assert isinstance(response, ErrorResponseSchema)
        assert response.message == 'Ingredient ids must be provided'
        assert response.success is False
        assert status_code == 400

    @allure.title('Создание заказа с неверным хэшем ингредиентов')
    @allure.step('Попытка создания заказа с неверным id ингредиентов')
    def test_create_order_with_invalid_id_ingredients(self, orders_client, unique_user):
        ingredients = CreateOrderRequestSchema(ingredients = ['invalid_id_1234'])
        
        _, status_code = orders_client.create_order(
            auth_token = unique_user['access_token'],
            ingredients = ingredients
            )

        assert status_code == 500

    @allure.title('Получение заказов авторизованным пользователем')
    @allure.step('Получение списка заказов с валидным токеном')
    def test_get_user_orders_with_auth_success(self, orders_client, unique_user):
        ingredient_response, _ = orders_client.get_ingredients()
        valid_id = ingredient_response.data[0].id
        ingredients = CreateOrderRequestSchema(ingredients = [valid_id])
        
        orders_client.create_order(
            auth_token = unique_user['access_token'],
            ingredients = ingredients
        )
        
        response, status_code = orders_client.get_user_orders(
            auth_token = unique_user['access_token'],
            )
        
        assert isinstance(response, GetUserOrdersResponseSchema)
        assert response.success is True
        assert isinstance(response.orders, list)
        assert response.total > 0
        assert isinstance(response.orders[0], ListOrderSchema)
        assert response.orders[0].id is not None
        assert response.orders[0].status is not None
        assert response.orders[0].number > 0
        assert response.orders[0].created_at is not None
        assert response.orders[0].updated_at is not None
        assert status_code == 200

    @allure.title('Получение заказов без авторизации')
    @allure.step('Получение списка заказов без токена авторизации')
    def test_get_user_orders_without_auth_fails(self, orders_client: OrdersClient):
        response, status_code = orders_client.get_user_orders(auth_token = None)

        assert isinstance(response, ErrorResponseSchema)
        assert response.success is False
        assert response.message == 'You should be authorised'
        assert status_code == 401
        