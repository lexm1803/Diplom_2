from tests.client.base_client import BaseClient
from tests.schemas.auth import (
    UpdateUserRequestSchema,
    UserFullResponseSchema,
    ErrorResponseSchema,
    EmptyResponse
)


class UserClient(BaseClient):

    def get_user(self, auth_token: str) -> tuple[UserFullResponseSchema | ErrorResponseSchema, int]:

        response, status_code = self.get(
            endpoint = '/api/auth/user',
            success_model = UserFullResponseSchema,
            error_model = ErrorResponseSchema,
            auth_token = auth_token
        )

        return response, status_code
    
    def update_user(
            self, 
            auth_token: str, 
            update_data: UpdateUserRequestSchema
            ) -> tuple[UserFullResponseSchema | ErrorResponseSchema, int]:
        
        response, status_code = self.patch(
            endpoint = '/api/auth/user',
            request_model = update_data,
            success_model = UserFullResponseSchema,
            error_model = ErrorResponseSchema,
            auth_token = auth_token
        )

        return response, status_code
    
    def delete_user(self, auth_token: str) -> tuple[EmptyResponse, int]:

        response, status_code = self.delete(
            endpoint = '/api/auth/user',
            success_model = EmptyResponse,
            error_model = ErrorResponseSchema,
            auth_token = auth_token
        )

        return response, status_code
    