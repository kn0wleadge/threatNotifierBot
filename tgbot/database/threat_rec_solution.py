from tgbot.database.models import async_session
from tgbot.database.models import User, Threat, Soft, UsersSoft,SoftsThreat,UsersThreat,UsersApplication



from sqlalchemy.orm import aliased
import datetime
from sqlalchemy import select, insert, update

async def threat_rec_solution(threat_id):
    async with async_session() as session:
        threat_solution = await session.scalar(select(Threat.rec_solve).where(Threat.id == threat_id))
        return threat_solution