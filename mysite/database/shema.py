from typing import Optional
from pydantic import BaseModel, EmailStr
from .models import StatusChoices
from datetime import date, datetime


class UserProfileInputSchema(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    password: str
    age: Optional[int]
    phone_number: Optional[str]

class UserProfileOutSchema(BaseModel):
    id:int
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    password: str
    age: Optional[int]
    phone_number: Optional[str]
    status: StatusChoices
    data_registered: date

class UserLoginSchema(BaseModel):
    username: str
    password: str

class CategoryInputShema(BaseModel):
    category_image: str
    category_name: str

class CategoryOutShema(BaseModel):
    id: int
    category_image: str
    category_name: str

class SubCategoryInputShema(BaseModel):
    sub_category_name: str
    category_id: int

class SubCategoryOutShema(BaseModel):
    id: int
    sub_category_name: str
    category_id: int

class ProductInputShema(BaseModel):
    subcategory_id: int
    product_name: str
    price: int
    article_number: int
    description: str
    video: Optional[str]
    product_type: bool
    created_date: datetime

class ProductOutShema(BaseModel):
    id: int
    subcategory_id: int
    product_name: str
    price: int
    article_number: int
    description: str
    video: Optional[str]
    product_type: bool
    created_date: datetime

class ProductImageInputShema(BaseModel):
    image: str
    product_id: int

class ProductImageOutShema(BaseModel):
    id: int
    image: str
    product_id: int

class ReviewInputShema(BaseModel):
    user_id: int
    product_id: int
    text: str
    stars: int
    created_date: date

class ReviewOutShema(BaseModel):
    id: int
    user_id: int
    product_id: int
    text: str
    stars: int
    created_date: date

