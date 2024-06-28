from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

defaultKeyboard = ReplyKeyboardMarkup(keyboard = [
    [KeyboardButton(text = 'Список выбранного ПО')]
    ,[KeyboardButton(text = 'Список обрабатываемых уязвимостей')]
    ,[KeyboardButton(text = 'Список устраненных уявзимостей')]
    
],
resize_keyboard = True,
input_field_placeholder = 'Выберите пункт меню')

checkActualSoftwareKeyboard = ReplyKeyboardMarkup(keyboard = [
    [KeyboardButton(text = 'Изменить список ПО')]
    ,[KeyboardButton(text = 'На главную')]
],
resize_keyboard = True,
input_field_placeholder = 'Выберите пункт меню')
