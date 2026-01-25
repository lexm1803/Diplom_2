import uuid
from tests.schemas.auth import (
    RegisterUserRequestSchema,
    PartialRegisterUserRequestSchema
)


class UserBuilder:

    def __init__(self):
        self.email = None
        self.password = None
        self.name = None

    def with_email(self, email: str) -> 'UserBuilder':
        self.email = email

        return self
    
    def with_password(self, password: str) -> 'UserBuilder':
        self.password = password

        return self
    
    def with_name(self, name: str) -> 'UserBuilder':
        self.name = name

        return self
    
    def with_unique_email(self) -> 'UserBuilder':
        unique_part = str(uuid.uuid4())[:8]
        self.email = f'user_{unique_part}@example.com'
        
        return self
    
    def with_unique_password(self) -> 'UserBuilder':
        unique_part = str(uuid.uuid4())[:12]
        self.password = f'password_{unique_part}'

        return self
    
    def with_unique_name(self) -> 'UserBuilder':
        unique_part = str(uuid.uuid4())[:8]
        self.name = f'Name_{unique_part}'

        return self
    
    def build(self) -> RegisterUserRequestSchema:
        return RegisterUserRequestSchema(
            email = self.email or self.with_unique_email().email,
            password = self.password or self.with_unique_password().password,
            name = self.name or self.with_unique_name().name
        )
    
    def build_invalid_user(self) -> PartialRegisterUserRequestSchema:
        return PartialRegisterUserRequestSchema(
            email = self.email,
            password = self.password,
            name = self.name
        )
    