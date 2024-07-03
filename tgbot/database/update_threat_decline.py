from tgbot.database.models import async_session
from tgbot.database.models import User, Threat, Soft, UsersSoft,SoftsThreat,UsersThreat
from tgbot.database.find_threatid_by_info import get_threatid
from sqlalchemy.orm import aliased
import datetime
from sqlalchemy import select, insert, update

async def update_threat_decline(user_id, threat_id):
    async with async_session() as session:
        print(f'updating threat, user id - {user_id}, threat id - {threat_id}, THREAT DECLINED!')
        try:
            await session.execute(update(UsersThreat)
                                .where((UsersThreat.id_user == user_id) & (UsersThreat.id_threat == threat_id))
                                .values(threat_status = 'Declined', refuse_date= datetime.datetime.now()))
        except Exception as e:
            print(f"update_threat_decline: error - {e}")
        await session.commit()