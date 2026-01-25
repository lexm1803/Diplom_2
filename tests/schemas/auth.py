from pydantic import BaseModel, ConfigDict, Field, EmailStr


class RegisterUserRequestSchema(BaseModel):
    email: EmailStr
    password: str=Field(min_length=6)
    name: str

class LoginUserRequestSchema(BaseModel):
    email: EmailStr
    password: str

class UpdateUserRequestSchema(BaseModel):
    email: EmailStr | None = None
    password: str | None = None
    name: str | None = None

class UserResponseSchema(BaseModel):
    email: EmailStr
    name: str

class LoginResponseSchema(BaseModel):
    success: bool
    access_token: str=Field(alias='accessToken')
    refresh_token: str=Field(alias='refreshToken')
    user: UserResponseSchema
    model_config = ConfigDict(populate_by_name=True)

class ErrorResponseSchema(BaseModel):
    success: bool
    message: str

class UserFullResponseSchema(BaseModel):
    success: bool
    user: UserResponseSchema

class PartialRegisterUserRequestSchema(BaseModel):
    email: EmailStr | None = None
    password: str | None = None
    name: str | None = None

class EmptyResponse(BaseModel):
    pass