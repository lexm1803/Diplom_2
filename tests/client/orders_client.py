from tests.client.base_client import BaseClient
from tests.schemas.orders import (
    CreateOrderRequestSchema,
    CreateOrderResponseSchema,
    GetUserOrdersResponseSchema,
    GetIngredientsResponseSchema
)
from tests.schemas.auth import ErrorResponseSchema


class OrdersClient(BaseClient):

    def get_ingredients(self) -> tuple[GetIngredientsResponseSchema | ErrorResponseSchema, int]:
        
        response, status_code = self.get(
            endpoint = '/api/ingredients',
            success_model = GetIngredientsResponseSchema,
            error_model = ErrorResponseSchema
        )

        return response, status_code
    
    def create_order(
        self, 
        auth_token: str | None, 
        ingredients: CreateOrderRequestSchema
        ) -> tuple[CreateOrderResponseSchema | ErrorResponseSchema, int]:

        response, status_code = self.post(
            endpoint = '/api/orders',
            request_model = ingredients,
            success_model = CreateOrderResponseSchema,
            error_model = ErrorResponseSchema,
            auth_token = auth_token
        )

        return response, status_code
    
    def get_user_orders(self, auth_token: str) -> tuple[GetUserOrdersResponseSchema | ErrorResponseSchema, int]:

        response, status_code = self.get(
            endpoint = '/api/orders',
            success_model = GetUserOrdersResponseSchema,
            error_model = ErrorResponseSchema,
            auth_token = auth_token
        )

        return response, status_code 
    