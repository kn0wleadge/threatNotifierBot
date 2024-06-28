from tgbot.database.models import async_session
from tgbot.database.models import User, Threat, Soft, UsersSoft,SoftsThreat,UsersThreat, UsersApplication

from sqlalchemy.orm import aliased
import datetime
from sqlalchemy import select, insert, update

async def decline_user(tg_id:int):
    async with async_session() as session:
        print("Declining user's application")
        #Изменения состояния заявки пользователя
        await session.execute(update(UsersApplication).where((UsersApplication.tg_id == tg_id)).values(is_applied = False))
        await session.commit()