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
from tgbot.handlers.startHandlers import UserApplicationCallbackData
from bot_init import bot,dp

import datetime

import os
#ТЕСТ ОТКЛОНИТЬ ЗАЯВКУ И ПРИНЯТЬ ЗАЯВКУ

NewUserRouter = Router()

@NewUserRouter.callback_query(UserApplicationCallbackData.filter(F.state == True))
async def accept_user(query:CallbackQuery, callback_data:UserApplicationCallbackData):
    print('User accepted...')

    await query.message.answer('Заявка пользователя успешно принята!')
    await create_user(callback_data.tg_id)

    await bot.send_message(chat_id = callback_data.tg_id, text='Ваша заявка успешно принята!\nВоспользуйтесь командой /help, чтобы подробнее узнать о возможностях бота')


@NewUserRouter.callback_query(UserApplicationCallbackData.filter(F.state == False))
async def decline_userr(query:CallbackQuery, callback_data:UserApplicationCallbackData):
    print('User declined...')

    await query.message.answer('Заявка пользователя отклонена!')
    await decline_user(callback_data.tg_id)
