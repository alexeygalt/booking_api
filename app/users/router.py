from fastapi import APIRouter, Depends, Response
from app.exceptions import IncorrectEmailOrPasswordException, UserAlreadyExistsException
from app.users.auth import authenticate_user, create_access_token, get_password_hash
from app.users.dao import UsersDAO
from app.users.dependencies import get_current_user
from app.users.schemas import SUserAuth, UserMeSchema

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
async def register_user(user_data: SUserAuth):
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if not existing_user:
        hashed_password = get_password_hash(user_data.password)
        await UsersDAO.add(email=user_data.email, hashed_password=hashed_password)
        return Response(status_code=201)

    raise UserAlreadyExistsException


@router.post("/login")
async def login_user(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return {"access_token": access_token}


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("booking_access_token")


@router.get("/me", response_model=UserMeSchema)
async def read_users_me(current_user=Depends(get_current_user)):
    return current_user
