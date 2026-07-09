from pydantic import BaseModel
from pydantic import EmailStr

class UserRegister(BaseModel):

    first_name: str

    last_name: str

    email: EmailStr

    password: str

    phone: str

class UserLogin(BaseModel):

    email: EmailStr

    password: str

class UserResponse(BaseModel):

    id: int

    first_name: str

    last_name: str

    email: EmailStr

    phone: str

    role: str

    class Config:

        from_attributes=True