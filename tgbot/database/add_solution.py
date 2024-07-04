from tgbot.database.models import async_session
from tgbot.database.models import User, Threat, Soft, UsersSoft,SoftsThreat,UsersThreat

from sqlalchemy.orm import aliased
import datetime
from sqlalchemy import select, insert, update

async def add_solution(tg_id, threat_id, solution):
    async with async_session() as session:
        print('add_solution: adding solution')
        await session.execute(update(UsersThreat)
                              .where(UsersThreat.id_user == tg_id, UsersThreat.id_threat == threat_id)
                              .values(threat_status = 'Solved', threat_solution = solution, solve_date = datetime.datetime.now()))
        await session.commit()