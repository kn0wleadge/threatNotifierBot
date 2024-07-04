from aiogram import F,Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message,CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.methods.send_message import SendMessage

from tgbot.keyboards.startKeyboards import startKeyboard
from tgbot.keyboards.defaultKeyboards import defaultKeyboard
from tgbot.keyboards.application_keyboard import application_markup

from tgbot.services.softwareListStrToTuple import softwareListStrToTuple

from tgbot.database.requests import check_if_user_exists_and_create, add_first_users_software_list,check_if_user_exists
from tgbot.database.create_user_application import create_application
from tgbot.database.check_user_application import check_user_application
from tgbot.database.create_user import create_user
from tgbot.database.decline_user import decline_user
from tgbot.database.update_threat_accept import update_threat_accept
from tgbot.database.update_threat_decline import update_threat_decline
from tgbot.database.add_solution import add_solution


from tgbot.handlers.startHandlers import UserApplicationCallbackData
from tgbot.services.send_threat import ThreatCallbackData
from tgbot.database.current_threats import CurrentThreatCallbackData
from bot_init import bot,dp

import datetime

import os

class InputtingSolution(StatesGroup):
    threat_id = State()
    solution = State()


CallbackRouter = Router()

@CallbackRouter.callback_query(UserApplicationCallbackData.filter(F.state == True))
async def accept_user(query:CallbackQuery, callback_data:UserApplicationCallbackData):
    print('User accepted...')
    await bot.delete_message(query.message.chat.id,query.message.message_id)
    await query.message.answer('Заявка пользователя успешно принята!')
    await create_user(callback_data.tg_id)

    await bot.send_message(chat_id = callback_data.tg_id, text='Ваша заявка успешно принята!\nЧтобы ввести интересующее вас ПО, нажмите кнопку "Ввести список ПО"\nВоспользуйтесь командой /help, чтобы подробнее узнать о возможностях бота',reply_markup=startKeyboard)


@CallbackRouter.callback_query(UserApplicationCallbackData.filter(F.state == False))
async def decline_userr(query:CallbackQuery, callback_data:UserApplicationCallbackData):
    print('User declined...')
    await bot.delete_message(query.message.from_user.id,query.message.message_id)
    await query.message.answer('Заявка пользователя отклонена!')
    await decline_user(callback_data.tg_id)



@CallbackRouter.callback_query(ThreatCallbackData.filter(F.state == True))
async def accept_threat(query:CallbackQuery, callback_data: ThreatCallbackData):
    print('Threat accepted')
    await bot.edit_message_text(text = "Угроза добавлена в список обрабатываемых угроз",chat_id = query.message.chat.id, message_id=query.message.message_id)
    await update_threat_accept(query.message.chat.id, callback_data.id)


@CallbackRouter.callback_query(ThreatCallbackData.filter(F.state == False))
async def decline_threat(query:CallbackQuery, callback_data: ThreatCallbackData):
    print('Threat declined')
    await bot.edit_message_text(text = "Угроза пропущена",chat_id = query.message.chat.id, message_id=query.message.message_id)
    await update_threat_decline(query.message.chat.id, callback_data.id)


@CallbackRouter.callback_query(CurrentThreatCallbackData.filter(F.id > 0))
async def input_solve(query:CallbackQuery, callback_data: ThreatCallbackData, state:FSMContext):
    print('Tapped on Input solve')
    await state.set_state(InputtingSolution.solution)
    await state.update_data(threat_id = callback_data.id)
    await query.message.answer('Введите всю необходимую информацию о том, как вы устранили эту уязвимость')

@CallbackRouter.message(InputtingSolution.solution)
async def inputting_solve(message:Message, state:FSMContext):
    print('Inputting solution')
    threat_data = await state.get_data()
    
    await state.update_data(solution = message.text)
    await add_solution(tg_id=message.chat.id,threat_id=threat_data['threat_id'] ,solution=message.text)
    await message.answer('Информация записана!', 
                         reply_markup=None)
    
    await state.clear()