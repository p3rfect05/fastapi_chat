from fastapi import APIRouter, HTTPException, BackgroundTasks
from starlette import status
from starlette.requests import Request
from starlette.responses import Response, RedirectResponse
from starlette.templating import Jinja2Templates

from auth.schemas import SUser, SUserAuth
from auth.token import get_password_hash, authenticate_user, create_access_token
from chat.dao import UserDAO
from chat.tasks import send_registration_email

router = APIRouter(prefix="/auth", tags=["Authentication"])

templates = Jinja2Templates(directory="templates")


@router.get("/register")  # localhost:80/
async def show_register(request: Request):
    return templates.TemplateResponse(request, "register.html")


@router.get("/login")
async def show_login(request: Request):
    return templates.TemplateResponse(request, "login.html")


@router.post("/register")
async def user_register(
    user_data: SUserAuth, response: Response, background_task: BackgroundTasks
):
    existing_user = await UserDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise HTTPException(
            detail="User already exists", status_code=status.HTTP_403_FORBIDDEN
        )
    hashed_password = get_password_hash(user_data.password)
    user = await UserDAO.add(email=user_data.email, hashed_password=hashed_password)
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("chat_access_token", access_token, httponly=True, samesite=None)
    response.status_code = status.HTTP_200_OK
    background_task.add_task(send_registration_email, user.email)
    return response


@router.post("/login")
async def user_login(user_data: SUserAuth, response: Response) -> dict:
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise HTTPException(
            detail="User is not registered", status_code=status.HTTP_401_UNAUTHORIZED
        )
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("chat_access_token", access_token, httponly=True, samesite=None)
    return {"token": access_token}


@router.post("/logout")
async def user_logout(response: Response):
    response.delete_cookie("chat_access_token")


@router.get("/logout")
async def user_logout():
    response = RedirectResponse("/auth/login", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("chat_access_token")
    return response
