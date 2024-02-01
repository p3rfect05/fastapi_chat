import datetime

from fastapi import FastAPI, HTTPException, APIRouter
from jose import jwt
from sqladmin import ModelView, Admin
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import Response, RedirectResponse

from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from auth.token import get_token, get_current_user, validate_token
from chat.models import User, Message
from chat.router import router as chat_router
from auth.router import router as auth_router
from config import SECRET_KEY, HS_ALGORITHM
from database import engine

app = FastAPI()

app.include_router(chat_router)
app.include_router(auth_router)
app.mount("/static", StaticFiles(directory="static"), name="static")
admin = Admin(app, engine)

reserved_routes = ["/openapi.json", "/docs", "/docs/oauth2-redirect", "/redoc", '/favicon', '/static']

class UserAdmin(ModelView, model=User):
    column_list = [User.email]
    column_details_exclude_list = [User.messages]

class MessageAdmin(ModelView, model=Message):
    column_list = [Message.user, Message.text, Message.time_created]

admin.add_view(UserAdmin)
admin.add_view(MessageAdmin)

origins = [

    "http://localhost",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers",
                   "Access-Control-Allow-Origin",
                   "Authorization"],
)

templates = Jinja2Templates(directory="templates")

@app.middleware("http")
async def check_auth(request: Request, call_next):
    path: str = request.scope['path']
    print(request.method, path)
    for route in reserved_routes:
        if route in path:
            response = await call_next(request)
            return response
    try:
        token: str = request.cookies.get('chat_access_token')
        payload = jwt.decode(token, SECRET_KEY, algorithms=[HS_ALGORITHM])
        exp: str = payload.get('exp')
        user_id: str = payload.get('sub')
        if not user_id or not exp or int(exp) < datetime.datetime.utcnow().timestamp():
            raise
        if 'login' in path or 'register' in path:
            #print('lol', path)
            return RedirectResponse(url='/chat/profile', status_code=status.HTTP_303_SEE_OTHER)

        else:
            response: Response = await call_next(request)
            return response
    except Exception as e:
        print(e)
        if 'login' not in path and 'register' not in path:
            response = RedirectResponse(url='/auth/login', status_code=status.HTTP_303_SEE_OTHER)
            response.delete_cookie('chat_access_token')
        else:
            response = await call_next(request)

        return response


@app.exception_handler(404)
async def not_found_exception_handler(request: Request, _):
    print(request.scope['path'], '404 not found')
    return templates.TemplateResponse(request, '404_response.html')



