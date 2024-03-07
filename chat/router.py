import json
from uuid import uuid4

from fastapi import APIRouter, Request, Depends, HTTPException, Path
from sqlalchemy import update, select
from starlette import status
from starlette.templating import Jinja2Templates
from starlette.websockets import WebSocket, WebSocketDisconnect


from auth.token import get_current_user
from chat.dao import MessageDAO, UserDAO, ChatDAO
from chat.models import User, Chat, Message, UserAndChatsTable
from database import async_sessionmaker


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


router = APIRouter(prefix="/chat", tags=["Communication"])


templates = Jinja2Templates(directory="templates")
manager = ConnectionManager()


@router.get("")
async def get_chats(request: Request, user: User = Depends(get_current_user)):
    async with async_sessionmaker() as session:
        chats_query = select(UserAndChatsTable).filter_by(user_id=user.id)
        user_chats = (await session.execute(chats_query)).scalars().all()
        chat_info = []

        for chat in user_chats:

            query = select(Chat).filter_by(id=chat.chat_id)
            messages = (await session.execute(query)).scalar().messages
            members = len((await session.execute(query)).scalar().users)
            if messages:
                chat_info.append(
                    {
                        "last_msg": messages[-1].text,
                        "chat_id": chat.chat_id,
                        "members": members,
                    }
                )
            else:
                chat_info.append(
                    {"last_msg": "", "chat_id": chat.chat_id, "members": members}
                )

        return templates.TemplateResponse(
            request=request, name="chat_list.html", context={"chats": chat_info}
        )


@router.get("/profile")
async def get_profile(request: Request, user: User = Depends(get_current_user)):
    return templates.TemplateResponse(
        request=request, name="profile.html", context={"user_email": user.email}
    )


@router.post("/create_chat")
async def create_chat(user: User = Depends(get_current_user)) -> dict:
    new_chat_uuid = str(uuid4())
    async with async_sessionmaker() as session:
        new_chat = await ChatDAO.add(id=new_chat_uuid)
        new_chat.users.append(user)
        session.add(new_chat)
        await session.commit()
        return {"chat_id": new_chat.id}


@router.get("/{chat_id}")
async def show_chat(
    chat_id: str, request: Request, user: User = Depends(get_current_user)
):
    chat = await ChatDAO.find_one_or_none(id=chat_id)
    if not chat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        # return Response(status_code=status.HTTP_404_NOT_FOUND)

    for user_chat in user.chats:
        if user_chat.id == chat_id:
            break
    else:
        async with async_sessionmaker() as session:
            user.chats.append(chat)
            session.add(user)
            await session.commit()
    messages = await MessageDAO.find_all(chat_id=chat_id)

    return templates.TemplateResponse(
        request=request,
        name="message_template.html",
        context={"client_id": user.id, "messages": messages},
    )


# @router.post('/{chat_id}/send_message')
# async def send_message(chat_id: str, message: SMessage, user: User = Depends(get_current_user)):
#     await MessageDAO.add(text=message.text, user_id=user.id, chat_id=chat_id)


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            user_id, chat_id, text = data["client_id"], data["chat_id"], data["text"]
            # print(websocket.cookies, websocket.headers)
            msg = await MessageDAO.add(text=text, user_id=user_id, chat_id=chat_id)
            # await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(
                json.dumps(
                    {
                        "user_id": user_id,
                        "email": msg.user.email,
                        "text": msg.text,
                        "time_created": msg.time_created.strftime("%Y-%m-%d %H:%M"),
                    }
                )
            )
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")
