from tgbot.database.models import async_session
from tgbot.database.models import User, Threat, Soft, UsersSoft,SoftsThreat,UsersThreat, UsersApplication

from sqlalchemy.orm import aliased
import datetime
from sqlalchemy import select, insert, update

async def create_user(tg_id:int):
    async with async_session() as session:
        print("Creating new user...")
        #Создание записи о новом пользователе в БД
        session.add(User(id = tg_id))
        await session.commit()

        print("Updating user's application...")
        #Обновление записи о заявке на использование бота в БД 
        await session.execute(update(UsersApplication).where((UsersApplication.tg_id == tg_id)).values(is_applied = True))
        await session.commit()

