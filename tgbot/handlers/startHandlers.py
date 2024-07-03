from aiogram import F,Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.methods.send_message import SendMessage

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from tgbot.keyboards.startKeyboards import startKeyboard
from tgbot.keyboards.defaultKeyboards import defaultKeyboard
from tgbot.keyboards.application_keyboard import application_markup

from tgbot.services.softwareListStrToTuple import softwareListStrToTuple

from tgbot.database.requests import check_if_user_exists_and_create, add_first_users_software_list,check_if_user_exists
from tgbot.database.create_user_application import create_application
from tgbot.database.check_user_application import check_user_application
from tgbot.database.check_user_soft import check_user_soft

from bot_init import bot,dp

import datetime

import os
class UserApplicationCallbackData(CallbackData, prefix = 'Application'):
                state: bool
                tg_id: int

StartRouter = Router()

class Reg(StatesGroup):
    software_input_state = State()


@StartRouter.message(CommandStart())
async def cmd_start(message: Message):

    user = await check_if_user_exists(message.from_user.id)
    print(f'is user exists? - {user}')
    if not user:
        user_application = await check_user_application(message.from_user.id)
        print(f'user sent application already? - {user_application}')
        #Если заявка уже подана
        if not user_application:
            #Получение списка tgid администраторов, которые будут принимать решение по приему пользователей
            admin_list = os.getenv('ADMIN_TG_ID').split(',')

            #await message.answer(f'Привет. Этот бот будет отправлять тебе информацию о последних опубликованных уязвимостях ПО.\nДля начала, тебе необходимо ввести список интересущего тебя ПО.\nCписок доступных команд:\n/start - запуск бота\n/help - справочная информация\n/softlist - список выбранного ПО\n/current_threats - список актуальных угроз ПО\n/solved_threats - список решенных угроз ПО\n/change_softlist - изменить список выбранного ПО\n'                       
            #                    ,reply_markup=startKeyboard)
            await message.answer(f'Привет. Этот бот будет отправлять тебе информацию о последних опубликованных уязвимостях ПО.\nПодожди, пока администратор примет твою заявку.\n')
            application = {'tg_id': message.from_user.id, 'name':message.from_user.first_name, 'date': datetime.datetime.now()}

            #Создание в БД записи о заявке этого пользователя
            await create_application(application)
            
            #Создание Inline клавиатуры, для ответа на заявку пользователя
            builder = InlineKeyboardBuilder()
            builder.button(text = 'Принять ✅', callback_data = UserApplicationCallbackData(state = True, tg_id = application['tg_id']).pack())
            builder.button(text = 'Отклонить 🚫', callback_data = UserApplicationCallbackData(state = False, tg_id = application['tg_id']).pack())
            
            
            str = f"Следующий пользователь отправил заявку на использование бота.\nИмя пользователя - {application['name']}\nДата заявки - {application['date']}"
            for admin_id in admin_list:
                print(f"id админа - {admin_id}")
                await bot.send_message(chat_id= admin_id, text = str
                                       ,reply_markup=builder.as_markup())
        else:
            await message.answer(f'Твоя заявка уже в обработке, подожди пока администратор её одобрит 🙂')
    else:
        await message.answer('Привет. Этот бот будет отправлять тебе информацию о последних опубликованных уязвимостях ПО. Нажми на /help, чтобы получить информацию о возможностях бота')



    
 
@StartRouter.message(F.text == 'Ввести список ПО')
#TODO - продумать ситуацию, если человек нажал ввести список ПО, но при этом не ввёл его
async def software_input(message: Message, state: FSMContext):
    #проверка пользователя на существование и добавление(если надо)
    user_entered_soft = await check_user_soft(message.from_user.id)
    if(not user_entered_soft):
        await state.set_state(Reg.software_input_state)
        await message.answer('Введите список ПО. Ведите перечисление строго через запятую, без пробелов, названия ПО должны начинаться с большой буквы.',
                            reply_markup= None)
    else:
        await message.answer('Вы уже ввели список ПО!',
                            reply_markup= None)


@StartRouter.message(Reg.software_input_state)
async def reg_two(message:Message, state: FSMContext):
    print('registrating new soft')
    data = message.text
    separated_data = softwareListStrToTuple(data)
    for i in separated_data:
        print(i)
    await add_first_users_software_list(message.from_user.id, separated_data)
    await state.update_data(software_input_state = message.text)  
    #TODO - форматировать сообщение
    await message.answer('Список ПО успешно введен, при появлении публикаций о новых уязвимостях, вы тут же получите сообщение!', reply_markup=None)
    await state.clear()
#1)проверяю работает ли убирание пробелов2+
#2)проверка connect_soft
#3)сделать так, чтобы связь происходила только с тем софтом, который обособлен пробелом в описании
#folders - templates(jinja2), handlers, service(?), 
# ORM - SQLAlchemy, 
# ParseLib - PlayWright
# Права доступа
# Логирование - LoGuru
#диджитализируем(https://www.youtube.com/watch?v=ExaQHffBE20,)
