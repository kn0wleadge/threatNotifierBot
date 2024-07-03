from tgbot.database.models import async_session
from tgbot.database.models import User, Threat, Soft, UsersSoft,SoftsThreat,UsersThreat

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

import datetime
from sqlalchemy import select, insert, update
from sqlalchemy.orm import make_transient
class CurrentThreatCallbackData(CallbackData, prefix = 'Current threat'):
                threat_id:int


async def current_threats(tg_id):
    async with async_session() as session:
        stmt = (
            select(Threat)
            .join(
                UsersThreat,
                UsersThreat.id_threat == Threat.id
            )
            .where(
                UsersThreat.id_user == tg_id, 
                UsersThreat.threat_status == 'Accepted'
            )
            )
        current_threats = await session.scalars(stmt)
        counter = 0
        threats = []
        for row in current_threats:
            print(f'current row - {row}')
            counter = counter + 1
            builder = InlineKeyboardBuilder()   
            builder.button(text = "Подробнее 📄", url =(row.url))
            builder.button(text = "Отправить решение ✅", callback_data = CurrentThreatCallbackData(threat_id = (row.id)).pack())
            builder.adjust(1)
            threat = {}
            threat['builder'] = builder
            threat_message =f'{counter})'+ f'Код угрозы - BDU:{row.url[25:]}\n' + 'Описание угрозы:' + row.description + '\n' + 'Возможное решение:' + row.rec_solve + '\n'
            threat['message'] = threat_message
            threats.append(threat)
        return threats
