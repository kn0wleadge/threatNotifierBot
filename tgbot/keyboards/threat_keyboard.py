from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

threat_solution_keyboard = ReplyKeyboardMarkup(keyboard = [
    [KeyboardButton(text = 'Угроза устранена рекомендованным способом ✅')]
    ,[KeyboardButton(text = 'Назад ⬅️')]
    
],
)