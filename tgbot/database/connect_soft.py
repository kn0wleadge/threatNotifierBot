from tgbot.database.models import async_session
from tgbot.database.models import User, Threat, Soft, UsersSoft,SoftsThreat,UsersThreat

from sqlalchemy.orm import aliased
import datetime
from sqlalchemy import select, insert, update

from tgbot.database.get_all_soft import get_all_soft
from tgbot.services.find_soft_in_description import find_soft_in_description

async def connect_soft(threat_url:str):
    async with async_session() as session:
        print('connecting threat to some soft...')
        soft_names = await get_all_soft()
        threat_info = (await session.execute(select(Threat.description,Threat.id).where(Threat.url == threat_url))).one()
        threat_soft = await find_soft_in_description(threat_info[0],soft_names)
        threat_id = threat_info[1]
        print(threat_info)

        for soft in threat_soft:
            soft_id = await session.scalar(select(Soft.id).where(Soft.name == soft))
            await session.execute(insert(SoftsThreat).values(id_soft = soft_id, id_threat = threat_id))
            await session.commit()
        


                



