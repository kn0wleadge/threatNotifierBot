from tgbot.database.models import async_session
from tgbot.database.models import User, Threat, Soft, UsersSoft,SoftsThreat,UsersThreat

from sqlalchemy.orm import aliased
import datetime
from sqlalchemy import select, insert, update

async def get_threatid(info):
    print("Getting threatid by info...")
    async with async_session() as session:
        threat_id = await session.scalar(select(Threat).where((Threat.description == info['Description']) & (Threat.rec_solve == info['Solving method']) & (Threat.danger_level == info['Danger level'])))
       # print (f'found threat_id --- {threat_id}')
        return threat_id