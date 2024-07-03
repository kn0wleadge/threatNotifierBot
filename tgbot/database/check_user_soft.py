from tgbot.database.models import async_session
from tgbot.database.models import User, Threat, Soft, UsersSoft,SoftsThreat,UsersThreat

from sqlalchemy.orm import aliased
import datetime
from sqlalchemy import select, insert, update


async def check_user_soft(tg_id):
    async with async_session() as session:
        soft = (await session.scalars(select(UsersSoft).where(UsersSoft.id_user == tg_id))).first()
        print(soft)
        if soft:
            return True
        else:
            return False