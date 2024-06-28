from tgbot.database.models import async_session
from tgbot.database.models import User, Threat, Soft, UsersSoft,SoftsThreat,UsersThreat,UsersApplication

from sqlalchemy.orm import aliased
import datetime
from sqlalchemy import select, insert, update


async def check_user_application(tg_id) -> bool:
    async with async_session() as session:
        user = await session.scalar(select(UsersApplication).where(tg_id == tg_id))
        print(user)
        flag = True
        if not user:
            flag = False
        return flag