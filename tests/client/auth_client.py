from tests.client.base_client import BaseClient
from tests.schemas.auth import (
    RegisterUserRequestSchema,
    LoginUserRequestSchema,
    LoginResponseSchema,
    ErrorResponseSchema,
)


class AuthClient(BaseClient):
    
    def register(
            self, 
            user_data: RegisterUserRequestSchema
            ) -> LoginResponseSchema | ErrorResponseSchema:
        
        return self.post(
            endpoint = '/api/auth/register',
            request_model = user_data,
            success_model = LoginResponseSchema,
            error_model = ErrorResponseSchema
        )
    
    def login(
            self,
            creds: LoginUserRequestSchema,
            ) -> LoginResponseSchema | ErrorResponseSchema:
        
        return self.post(
            endpoint = '/api/auth/login',
            request_model = creds,
            success_model = LoginResponseSchema,
            error_model = ErrorResponseSchema
        )
    
    def logout(self, refresh_token: str,) -> dict:
        
        return self.post(
            endpoint = '/api/auth/logout',
            request_model = None,
            success_model = dict, 
            error_model = ErrorResponseSchema,
            auth_token = refresh_token
            )
        
    def refresh_token(self, refresh_token: str) -> LoginResponseSchema | ErrorResponseSchema:

        return self.post(
            endpoint = '/api/auth/token',
            request_model = None,
            success_model = LoginResponseSchema,
            error_model = ErrorResponseSchema,
            auth_token = refresh_token
            )
    