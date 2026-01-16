import httpx
from typing import Optional, Type, TypeVar, Union
from pydantic import BaseModel


T = TypeVar('T', bound=BaseModel)

class BaseClient:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url
        self.client = httpx.Client(base_url=base_url, timeout=30.0)

    def build_headers(self, auth_token: str = None) -> dict[str, str]:
        headers = {'Content-Type': 'application/json'}
        if auth_token:
            headers['Authorization'] = auth_token
        return headers
    
    def send(
            self, 
            method: str, 
            endpoint: str, 
            *, 
            request_model: Optional[BaseModel] = None, 
            success_model: Type[T], 
            error_model: Type[BaseModel], 
            auth_token: str = None
            ) -> Union[T, BaseModel]:
        
        headers = self.build_headers(auth_token)
        
        json_data = request_model.model_dump(exclude_unset = True) if request_model else None
        
        response = self.client.request(
            method = method, 
            url = endpoint, 
            json = json_data, 
            headers = headers
            )
        
        if 200 <= response.status_code < 300:
            return success_model.model_validate_json(response.text)
        else:
            content_type = response.headers.get('content-type', '')
            if 'application/json' in content_type:
                return error_model.model_validate_json(response.text)
            else:
                raise ValueError(f'Ответ не json объекта со статусом {response.status_code}')
    
    def post(
            self, 
            endpoint: str, *, 
            request_model: Optional[BaseModel] = None, 
            success_model: Type[T], 
            error_model: Type[BaseModel], 
            auth_token: str = None
            ) -> Union[T, BaseModel]:
        
        return self.send(
            method = 'POST',
            endpoint = endpoint,
            request_model = request_model,
            success_model = success_model,
            error_model = error_model,
            auth_token = auth_token
        )
    
    def get(
            self, 
            endpoint: str, 
            *, 
            success_model: Type[T], 
            error_model: Type[BaseModel], 
            auth_token: str = None
            ) -> Union[T, BaseModel]:
        
        return self.send(
            method = 'GET',
            endpoint = endpoint,
            success_model = success_model,
            error_model = error_model,
            auth_token = auth_token
        )
    
    def patch(
            self, 
            endpoint: str, 
            *, 
            request_model: Optional[BaseModel] = None, 
            success_model: Type[T], 
            error_model: Type[BaseModel], 
            auth_token: str = None
            ) -> Union[T, BaseModel]:
        
        return self.send(
            method = 'PATCH',
            endpoint = endpoint,
            request_model = request_model,
            success_model = success_model,
            error_model = error_model,
            auth_token = auth_token
        )
    
    def delete(
            self, 
            endpoint: str, 
            *, 
            success_model: Type[T], 
            error_model: Type[BaseModel], 
            auth_token: str = None
            ) -> Union[T, BaseModel]:
        
        return self.send(
            method = 'DELETE',
            endpoint = endpoint,
            success_model = success_model,
            error_model = error_model,
            auth_token = auth_token
        )
    