from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

startKeyboard = ReplyKeyboardMarkup(keyboard = [
    [KeyboardButton(text = 'Ввести список ПО')]
],
resize_keyboard = True,
input_field_placeholder = 'Выберите пункт меню')

# @inline keyboard
#settings = InlineKeyboardMarkup(inline_keyboard = [[InlineKeyboardButton(text = 'Go to GitHub', url = 'https://github.com')]])

