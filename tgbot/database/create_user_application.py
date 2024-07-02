from tgbot.database.models import async_session
from tgbot.database.models import User, Threat, Soft, UsersSoft,SoftsThreat,UsersThreat,UsersApplication



from sqlalchemy.orm import aliased
import datetime
from sqlalchemy import select, insert, update

import logging

async def create_application(user_info):
    async with async_session() as session:
        await session.execute(insert(UsersApplication).values(tg_id = user_info["tg_id"],name = user_info["name"], application_date = user_info["date"]))
        await session.commit()