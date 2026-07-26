from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):

    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):

    email: EmailStr
    password: str


class UserResponse(BaseModel):

    id: int
    username: str
    email: str
    role: str
    is_active: bool
    is_verified: bool

    class Config:
        from_attributes = True



class UserRoleUpdate(BaseModel):

    role: str



class TokenResponse(BaseModel):

    access_token: str
    token_type: str