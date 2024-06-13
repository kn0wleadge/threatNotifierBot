from aiogram import F,Router
from aiogram.filters import CommandStart
from aiogram.types import Message

import app.keyboards as kb

startRouter = Router()

@startRouter.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f'Привет. \nТвой ID: {message.from_user.id}\nИмя:{message.from_user.first_name}',
                         reply_markup=kb.settings)

#folders for templates(jinja2), handlers, service(?), ORM - SQLAlchemy, PlayWright
#диджитализируем(https://www.youtube.com/watch?v=ExaQHffBE20,)
