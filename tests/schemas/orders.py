from pydantic import BaseModel, ConfigDict, Field, EmailStr
from typing import Optional


class CreateOrderRequestSchema(BaseModel):
    ingredients: list[str]

class OrderResponseSchema(BaseModel):
    number: int

class CreateOrderResponseSchema(BaseModel):
    success: bool
    name: str
    order: OrderResponseSchema

class GetUserOrdersResponseSchema(BaseModel):
    success: bool
    orders: list[ListOrderSchema]
    total: int
    total_today: int=Field(alias='totalToday')
    model_config = ConfigDict(populate_by_name = True, extra = 'forbid')

class IngredientSchema(BaseModel):
    id: str=Field(alias='_id')
    name: str
    type: str
    proteins: int
    fat: int
    carbohydrates: int
    calories: int
    price: int
    image: str
    image_mobile: str
    image_large: str
    version: Optional[int]=Field(alias='__v', default = None)
    model_config = ConfigDict(populate_by_name = True)

class GetIngredientsResponseSchema(BaseModel):
    success: bool
    data: list[IngredientSchema]
    
class ListOrderSchema(BaseModel):
    ingredients: list[str]
    id: str=Field(alias='_id')
    status: str
    number: int
    created_at: str=Field(alias='createdAt')
    updated_at: str=Field(alias='updatedAt')
    model_config = ConfigDict(populate_by_name = True)
