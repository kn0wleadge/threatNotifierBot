
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from bot_init import bot

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
       