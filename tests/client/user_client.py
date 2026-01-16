from tests.client.base_client import BaseClient
from tests.schemas.auth import (
    UpdateUserRequestSchema,
    UserFullResponseSchema,
    ErrorResponseSchema
)


class UserClient(BaseClient):

    def get_user(self, auth_token: str) -> UserFullResponseSchema | ErrorResponseSchema:

        return self.get(
            endpoint = '/api/auth/user',
            success_model = UserFullResponseSchema,
            error_model = ErrorResponseSchema,
            auth_token = auth_token
        )
    
    def update_user(
            self, 
            auth_token: str, 
            update_data: UpdateUserRequestSchema
            ) -> UserFullResponseSchema | ErrorResponseSchema:
        
        return self.patch(
            endpoint = '/api/auth/user',
            success_model = UserFullResponseSchema,
            error_model = ErrorResponseSchema,
            auth_token = auth_token
        )
    
    def delete_user(self, auth_token: str) -> dict:

        response = self.delete(
            endpoint = '/api/auth/user',
            success_model = dict,
            error_model = ErrorResponseSchema,
            auth_token = auth_token
        )

        return response
    