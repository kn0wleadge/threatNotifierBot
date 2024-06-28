from tgbot.database.models import async_session
from tgbot.database.models import User, Threat, Soft, UsersSoft,SoftsThreat,UsersThreat

from sqlalchemy.orm import aliased
import datetime
from sqlalchemy import select, insert, update

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

async def check_if_user_exists(tg_id) -> bool:
    """

@Эта функция проверят, существует ли информация о пользователе в базе.
@Принимает на вход id телеграм-аккаунта пользователя
@Возвращает BOOl-значение, которое обозначает, 
    существовует ли пользователь, или нет.

"""
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == tg_id))
        print(user)
        flag = True
        if not user:
            flag = False
        return flag

async def check_if_user_exists_and_create(tg_id) -> bool:
    """

@Эта функция проверят, существует ли информация о пользователе в базе.
    Если информации нет - она добавит запись о нем в базу данных
@Принимает на вход id телеграм-аккаунта пользователя
@Возвращает BOOl-значение, которое обозначает, 
    существовал ли пользователь до этого, или нет.

"""
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == tg_id))
        print(user)
        flag = True
        if not user:
            session.add(User(id = tg_id))
            await session.commit()
            flag = False
        return flag

async def check_if_user_registrated(tg_id) -> bool:
    """

@Эта функция проверят, ввёл ли пользователь информацию о интересующем его ПО
@Принимает на вход id телеграм-аккаунта пользователя
@Возвращает BOOl-значение, которое обозначает, 
    ввел ли пользователь информацию о ПО, или нет.

"""         
    async with async_session() as session:
        stmt =(select(UsersSoft).where((UsersSoft.id_user == tg_id) & (UsersSoft.is_active == 1)))
        active_users_softlist = await session.scalar(stmt)
        if active_users_softlist:
            return True
        else:
            return False





async def add_first_users_software_list(tg_id, software_list):
    """

@Эта функция добавляет в базу данных информацию об интересующем
    пользователя ПО, когда он вводит его впервые
@Принимает на вход id телеграм-аккаунта пользователя, а также list с названиями ПО
@Ничего не возвращает
"""   
    async with async_session() as session:
        print(f"user id {tg_id}")
        for soft in software_list:
            soft_id = await session.scalar(select(Soft.id).where(Soft.name == soft))
            print(f"soft id {soft_id}")
            # Если такой софт уже есть в базе
            if soft_id:
                await session.execute(insert(UsersSoft) \
                                               .values(id_user = tg_id, id_soft = soft_id,\
                                                       choose_date = datetime.datetime.now(), \
                                                         is_active = 1))
                await session.commit()
            # Если софта в базе нет
            else:
                await session.execute(insert(Soft).values(name = soft, add_date = datetime.datetime.now()))
                await session.commit()
                print('insert into soft --------------------')
                soft_id = await session.scalar(select(Soft.id).where(Soft.name == soft))
                print(f"soft id {soft_id}")
                await session.execute(insert(UsersSoft).values(id_user = tg_id, id_soft = soft_id, choose_date = datetime.datetime.now(),is_active = 1))
                await session.commit()
                print('insert into UsersSoft --------------------')
    


async def get_users_softlist(tg_id) -> str:
    """

@Эта функция получает актуальный список выбранного пользователем ПО и преобразует его в str,
    в строке через \n ведется перечисление названий ПО
@Принимает на вход id телеграм-аккаунта пользователя
@Возвращает строку с выбранным пользователем ПО

"""   
    print('started getting softlist')
    async with async_session() as session:
        user_alias = aliased(User)
        users_soft_alias = aliased(UsersSoft)

        stmt = (
            select(Soft.name)
            .join(
                users_soft_alias,
                users_soft_alias.id_soft == Soft.id
            )
            .where(
                users_soft_alias.id_user == tg_id, 
                users_soft_alias.is_active == 1
            )
            )
        softlist = await session.execute(stmt)
        soft_names = [row[0] for row in softlist]
        soft_names_str = ''
        for i in range(len(soft_names)):
            soft_names_str = soft_names_str + f'{i+1}){soft_names[i]}\n'

        print(f'soft_namesfor soft in soft_names: soft_names_str {soft_names}')
        return soft_names_str


async def get_users_softlist_list(tg_id) -> list:
    """

@Эта функция получает актуальный список выбранного пользователем ПО
@Принимает на вход id телеграм-аккаунта пользователя
@Возвращает список с выбранным пользователем ПО

"""       
    print('started getting softlist')
    async with async_session() as session:
        users_soft_alias = aliased(UsersSoft)

        stmt = (
            select(Soft.name)
            .join(
                users_soft_alias,
                users_soft_alias.id_soft == Soft.id
            )
            .where(
                users_soft_alias.id_user == tg_id, 
                users_soft_alias.is_active == 1
            )
            )
        softlist = await session.execute(stmt)
        soft_names = [row[0] for row in softlist]
        
        return soft_names
    


#TODO - FULL CHECK FUNCTION
async def change_users_softlist(tg_id, softlist):
    """

@Эта функция изменяет выбранный пользователем список ПО на новый,
    который ввёл пользователь
@Принимает на вход id телеграм-аккаунта пользователя и новый список ПО
@Ничего не позвращает

"""   
    print('staretd changing softlist')
    async with async_session() as session:
        #Получение старого списка ПО
        users_old_softlist = await get_users_softlist_list(tg_id)

        #Нахождение одинакового ПО в старом и новом списках ПО
        softlists_intersection = intersection(softlist,users_old_softlist)

        #Нахождение ПО в старом списке ПО, которое больше не актуально для пользователя
        old_soft_to_disactivate = list(set(users_old_softlist) - set(softlists_intersection))

        #Нахождение ПО в новом списке ПО, которое пользователь хочет отслеживать
        new_soft_to_add = list(set(softlist) - set(softlists_intersection))

        #Проверка для каждого ПО в списке нового ПО на добавление(new_soft_to_add), есть ли о нем информация в базе
        for soft in new_soft_to_add:
            soft_check = await session.scalar(select(Soft).where(Soft.name == soft))

            #Если в базе информации нет, тогда она добавляется
            if not soft_check:
                await session.execute(insert(Soft).values(name = soft, add_date = datetime.datetime.now()))
                await session.commit()
                print('insert into soft --------------------')

        #Для каждого ПО в списке нового ПО на добавление(new_soft_to_add), добавляется запись о выборе пользователем этого софта
        for soft in new_soft_to_add:
            soft_id = await session.scalar(select(Soft.id).where(Soft.name == soft))
            await session.execute(insert(UsersSoft).values(id_user = tg_id, id_soft = soft_id, choose_date = datetime.datetime.now(),is_active = 1))
            await session.commit()
            print('insert into UsersSoft --------------------')

        #Для каждого ПО, которое больше не актуально для пользователя, проводится операция скрытого удаления
        for soft in old_soft_to_disactivate:
            soft_id = await session.scalar(select(Soft.id).where(Soft.name == soft))
            await session.execute(update(UsersSoft).where((UsersSoft.id_soft == soft_id) & (UsersSoft.id_user == tg_id)).values(is_active = 0))
            await session.commit()
            print('update on UsersSoft--------------------')


