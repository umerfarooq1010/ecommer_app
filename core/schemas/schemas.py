import math
from datetime import datetime, date
from typing import Union
from pydantic import BaseModel,field_validator,Field,validator
import re
from passlib.hash import pbkdf2_sha256


def check_email(value: str):
    email_regex = re.compile(
        r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    )
    if not email_regex.match(value):
        raise ValueError("Invalid email address.")
    else:
        return True

def has_special_char(value: str):
    special_char_regex = re.compile(r"[^a-zA-Z0-9]")
    return special_char_regex.search(value) is not None



class UserEmailSchema(BaseModel):
    email: str

    @field_validator("email")
    def check_email(v: str):
        if check_email(v):
            return v.lower()


class UserCreateSchema(UserEmailSchema):
    first_name: str
    last_name: str
    username: str
    password: str
    contact: Union[str, None] = None
    active: Union[bool, None] = None
    company_name: Union[str, None] = None
    address: Union[str, None] = None
    city: Union[str, None] = None
    country: Union[str, None] = None
    postal_code: Union[str, None] = None

    @field_validator("password")
    def password_hash(cls, v: str):
        if len(v) < 8:
            raise ValueError(
                "Password must have at least one (digit, upper case, lower case, special character) & min 8 in length"
            )
        if len(v) > 20:
            raise ValueError(
                "Password must have at least one (digit, upper case, lower case, special character) & min 8 in length"
            )
        if not any(char.isdigit() for char in v):
            raise ValueError(
                "Password must have at least one (digit, upper case, lower case, special character) & min 8 in length"
            )
        if not any(char.isupper() for char in v):
            raise ValueError(
                "Password must have at least one (digit, upper case, lower case, special character) & min 8 in length"
            )
        if not any(char.islower() for char in v):
            raise ValueError(
                "Password must have at least one (digit, upper case, lower case, special character) & min 8 in length"
            )
        if not has_special_char(v):
            raise ValueError(
                "Password must have at least one (digit, upper case, lower case, special character) & min 8 in length"
            )
        return pbkdf2_sha256.hash(v)


class UserSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    contact: Union[str, None] = None
    active: Union[bool, None] = None
    company_name: Union[str, None] = None
    address: Union[str, None] = None
    city: Union[str, None] = None
    country: Union[str, None] = None
    postal_code: Union[str, None] = None

class UserSchemaUpdate(BaseModel):
    first_name: str
    # last_name: str
    # contact: str
    # active: bool
    # company_name: str
    # address: str
    # city: str
    # country:  str
    # postal_code: str



#Product Category Schema
class ProductCategoryCreateSchema(BaseModel):
    name: str =Field(...,example="Pen")
    description: str=Field(...,example="X-Ray Pen")




class ProductCategorySchema(BaseModel):
    id: int
    name: str
    description: str
    created_by: Union[int, None] = None
    updated_by: Union[int, None] = None
    created_at: Union[datetime, None] = None
    updated_at: Union[datetime, None] = None



#Product Schema
class ProductCreateSchema(BaseModel):
    name: str =Field(...,example="Pen")
    description: str=Field(...,example="X-Ray Pen")
    price: float=Field(...,example=10.00)
    category_id: int=Field(...,example=1)





#Inventory Schema
class InventorySchema(BaseModel):
    product_id: int
    quantity: int



#Sale Order Schema
class SaleOrderSchema(BaseModel):
    id:int
    name:str=Field(...,example="Sale Order 1")
    description:str=Field(...,example="Sale Order 1")
    date:datetime=Field(...,example=datetime.now())
    customer_id:int=Field(...,example=1)
    product_id:int=Field(...,example=1)
    quantity:int=Field(...,example=1)
    price:float=Field(...,example=10.00)
    total:float=Field(...,example=10.00)



class InventorySchemaPatch(BaseModel):
    quantity: Union[float, None] = None
    threshold: Union[int, None] = None


class InventorySchema(InventorySchemaPatch):
    id: int
    product_id: Union[int, None] = None
    alert: Union[bool, None] = None
    creadted_by:Union[int, None] = None
    updated_by: Union[int, None] = None
    created_at: Union[datetime, None] = None
    updated_at:Union[datetime, None] = None

    @validator('alert', pre=True, always=True)
    def calculate_alert(cls, value, values):
        threshold = values.get('threshold')
        if threshold is not None and threshold <= 80:
            return True
        else:
            return False

