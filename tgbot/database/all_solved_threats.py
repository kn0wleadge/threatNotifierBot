from tgbot.database.models import async_session
from tgbot.database.models import User, Threat, Soft, UsersSoft,SoftsThreat,UsersThreat

from sqlalchemy.orm import aliased
import datetime
from sqlalchemy import select, insert, update

async def all_solved_threats(tg_id):
    async with async_session() as session:
        threats = await session.execute(select(UsersThreat.solve_date, UsersThreat.threat_solution, Threat.description,Threat.danger_level, Threat.url)
                                       .join(Threat, Threat.id == UsersThreat.id_threat)
                                       .where(UsersThreat.id_user == tg_id, UsersThreat.threat_status == 'Solved'))
        return threats