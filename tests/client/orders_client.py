from tests.client.base_client import BaseClient
from tests.schemas.orders import (
    CreateOrderRequestSchema,
    CreateOrderResponseSchema,
    GetUserOrdersResponseSchema,
    GetIngredientsResponseSchema
)
from tests.schemas.auth import ErrorResponseSchema


class OrdersClient(BaseClient):

    def get_ingredients(self) -> GetIngredientsResponseSchema | ErrorResponseSchema:
        
        return self.get(
            endpoint = '/api/ingredients',
            success_model = GetIngredientsResponseSchema,
            error_model = ErrorResponseSchema
        )
    
    def create_order(
        self, 
        auth_token: str | None, 
        ingredients: CreateOrderRequestSchema
        ) -> CreateOrderResponseSchema | ErrorResponseSchema:

        return self.post(
            endpoint = '/api/orders',
            request_model = ingredients,
            success_model = CreateOrderResponseSchema,
            error_model = ErrorResponseSchema,
            auth_token = auth_token
        )
    
    def get_user_orders(self, auth_token: str) -> GetUserOrdersResponseSchema | ErrorResponseSchema:
         
        return self.get(
            endpoint = '/api/orders',
            success_model = GetUserOrdersResponseSchema,
            error_model = ErrorResponseSchema,
            auth_token = auth_token
        )
    