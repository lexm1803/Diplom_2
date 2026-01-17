from tests.client.base_client import BaseClient
from tests.schemas.auth import (
    RegisterUserRequestSchema,
    LoginUserRequestSchema,
    LoginResponseSchema,
    ErrorResponseSchema,
    EmptyResponse,
)


class AuthClient(BaseClient):
    
    def register(
            self, 
            user_data: RegisterUserRequestSchema
            ) -> tuple[LoginResponseSchema | ErrorResponseSchema, int]:
        
        response, status_code = self.post(
            endpoint = '/api/auth/register',
            request_model = user_data,
            success_model = LoginResponseSchema,
            error_model = ErrorResponseSchema
        )

        return response, status_code
    
    def login(
            self,
            creds: LoginUserRequestSchema,
            ) -> tuple[LoginResponseSchema | ErrorResponseSchema, int]:
        
        response, status_code = self.post(
            endpoint = '/api/auth/login',
            request_model = creds,
            success_model = LoginResponseSchema,
            error_model = ErrorResponseSchema
        )

        return response, status_code
    
    def logout(self, refresh_token: str,) -> tuple[EmptyResponse, int]:
        
        response, status_code = self.post(
            endpoint = '/api/auth/logout',
            request_model = None,
            success_model = EmptyResponse, 
            error_model = ErrorResponseSchema,
            auth_token = refresh_token
            )

        return response, status_code
        
    def refresh_token(self, refresh_token: str) -> tuple[LoginResponseSchema | ErrorResponseSchema, int]:

        response, status_code = self.post(
            endpoint = '/api/auth/token',
            request_model = None,
            success_model = LoginResponseSchema,
            error_model = ErrorResponseSchema,
            auth_token = refresh_token
            )
    
        return response, status_code