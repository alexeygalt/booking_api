from pydantic import BaseModel, EmailStr


class SUserAuth(BaseModel):
    email: EmailStr
    password: str


class UserMeSchema(BaseModel):
    id: int
    email: str
