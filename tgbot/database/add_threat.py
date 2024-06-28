from tgbot.database.models import async_session
from tgbot.database.models import User, Threat, Soft, UsersSoft,SoftsThreat,UsersThreat

from sqlalchemy.orm import aliased
import datetime
from sqlalchemy import select, insert, update

import logging
async def add_threat(threat_info):
    """

@Эта функция добавляет в БД запись об угрозе
@Принимает на вход словарь с информацией об угрозе
@Ничего не возвращает

"""         
    async with async_session() as session:
        print('inserting threat into db...')
        print(f"Данные для вставки: {threat_info}") # Логирование данных перед вставкой
        try:
            await session.execute(insert(Threat).values(description = threat_info["Description"],
                                                   rec_solve = threat_info["Solving method"],
                                                   url = threat_info["url"],
                                                  danger_level = threat_info["Danger level"]))
        except Exception as e:
            print(f'Ошибка при добавлении угрозы в БД - {e}')
        
        print('hellFAGJADLGEAGJAG')
        await session.commit()


