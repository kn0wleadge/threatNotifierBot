from tgbot.database.models import async_session
from tgbot.database.models import User, Threat, Soft, UsersSoft,SoftsThreat,UsersThreat

from sqlalchemy.orm import aliased
import datetime
from sqlalchemy import select, insert, update

import logging
async def add_threat(threat_info) -> bool:
    """

@Эта функция добавляет в БД запись об угрозе
@Принимает на вход словарь с информацией об угрозе
@Ничего не возвращает

"""         
    async with async_session() as session:

        print('inserting threat into db...')
        is_added = True
        threat_id = await session.scalar(select(Threat).where(Threat.url == threat_info["url"]))

        if not threat_id:

            #Логирование данных перед вставкой
            print(f"Данные для вставки: {threat_info}") 
            try:
                await session.execute(insert(Threat).values(description = threat_info["Description"],
                                                    rec_solve = threat_info["Solving method"],
                                                    url = threat_info["url"],
                                                    danger_level = threat_info["Danger level"]))
                await session.commit()
            except Exception as e:
                print(f'Ошибка при добавлении угрозы в БД - {e}')

        else:
            print(f"Угроза уже добавлена")
            is_added = False

        return is_added
            
        


