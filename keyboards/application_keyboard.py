from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


application_markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = 'Принять ✅', callback_data='accept'), InlineKeyboardButton(text = 'Отклонить 🚫', callback_data='deny')]
    ])