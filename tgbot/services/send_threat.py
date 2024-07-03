from aiogram import F,Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.methods.send_message import SendMessage
from aiogram.utils.formatting import Text
from aiogram.utils.formatting import Bold
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from tgbot.keyboards.startKeyboards import startKeyboard
from tgbot.keyboards.defaultKeyboards import defaultKeyboard
from tgbot.keyboards.application_keyboard import application_markup

from tgbot.services.softwareListStrToTuple import softwareListStrToTuple

from tgbot.database.requests import check_if_user_exists_and_create, add_first_users_software_list,check_if_user_exists
from tgbot.database.create_user_application import create_application
from tgbot.database.check_user_application import check_user_application

from bot_init import bot,dp

import datetime

import os

class ThreatCallbackData(CallbackData, prefix = 'Threat'):
                id: int
                state:bool

async def send_threat(threat):
    print("send_threat: started sending...")
    print(f"send_threat: threat users id - {threat['user id']}")
    try:  
      for id_group in (threat["user id"]):
            for id in id_group:
              print(f"user id - {id}")
              builder = InlineKeyboardBuilder()
              builder.button(text = 'Принять ✅', callback_data = ThreatCallbackData(id = threat['id'], state = True).pack())
              builder.button(text = 'Отклонить 🚫', callback_data = ThreatCallbackData(id = threat['id'], state = False).pack())  
              await bot.send_message(chat_id = id,
                                  text = "Была обнаружена новая угроза!"
                                    )
              await bot.send_message(chat_id = id, 
                                     text = "Описание угрозы:\n" + threat["Description"] + '\n\n' + "Возможное решение:\n" + threat["Solving method"] + '\n\n' + "Ссылка на полную информацию об угрозе:\n" + threat["url"],
                                     reply_markup=builder.as_markup())
    except Exception as e:
       print(f"Error occurred: {e}")
       