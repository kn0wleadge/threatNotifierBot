from tgbot.database.models import async_session
from tgbot.database.models import User, Threat, Soft, UsersSoft,SoftsThreat,UsersThreat
from tgbot.database.find_threatid_by_info import get_threatid
from sqlalchemy.orm import aliased
import datetime
from sqlalchemy import select, insert, update

async def get_soft_id(names:list):
    print('getting soft id')
    async with async_session() as session:
        soft_id = []
        for name in names:
            try:
                id = await session.scalar(select(Soft.id).where(Soft.name == name))
                soft_id.append(id)
            except Exception as e:
                 print(f'Error while getting softs id  - {e}')
        return soft_id

async def get_users_by_soft(soft_id:list):
    print('getting users id')
    async with async_session() as session:
        users_id = []
        for id in soft_id:
            try:
                user_id = await session.scalar(select(UsersSoft.id_user).where((UsersSoft.id_soft == id) & (UsersSoft.is_active == 1)))
                users_id.append(user_id)
            except Exception as e:
                 print(f'Error while getting user id  - {e}')
            
        return users_id
        
async def connect_user(threat):
    async with async_session() as session:
        print("connecting threat to some user...")

        try:
            threat_id:int = (await get_threatid(threat)).id
        except Exception as e:
            print(f'error while getting threat_id - {e}')
        threat["id"] = threat_id

        try:
            soft_id:list = await get_soft_id(threat['Soft'])
        except Exception as e:
            print(f'Error while getting softs id - {e}')
        
        try:
            users_id:list = await get_users_by_soft(soft_id)
        except Exception as e:
            print(f'Error while getting users id - {e}')

        #Может быть несколько одинаковых id, так как в одной угрозе могут быть обноружены несколько ПО, которые привязаны к одному пользователю
        for user_id in users_id:
            print(f"user id - {user_id}, threat_id - {threat_id}")
            try:
                await session.execute(insert(UsersThreat).values(id_user = user_id,id_threat = threat_id,
                                                             send_date = datetime.datetime.now(),threat_status = 'Undefined',
                                                             ))
                await session.commit()
            except Exception as e:
                print(f'Error while inserting into users_threat- {e}')
        #Возвращается та же самая угроза, только в словаре еще хранится её id
        return threat
            
            
            



