from tgbot.database.models import async_session
from tgbot.database.models import User, Threat, Soft, UsersSoft,SoftsThreat,UsersThreat

from sqlalchemy.orm import aliased
import datetime
from sqlalchemy import select, insert, update


async def get_all_soft() -> list[str]:
    print("Getting soft...")
    async with async_session() as session:
        stmt = (
           select(Soft.name)
    .where(Soft.id.in_(
        select(UsersSoft.id_soft)
        .where(UsersSoft.is_active == 1)
    )))
        softlist = await session.execute(stmt)
        #soft_names_tuple = await session.execute(select(Soft.name))
        soft_names = [soft[0] for soft in softlist]
        for name in soft_names:
            print(name)
        return soft_names
                

