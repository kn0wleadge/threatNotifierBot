from aiogram import F,Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.utils.formatting import Text
from aiogram.utils.formatting import Bold

from tgbot.services.softwareListStrToTuple import softwareListStrToTuple

from tgbot.database.requests import get_users_softlist,check_if_user_registrated, change_users_softlist
import tgbot.keyboards.defaultKeyboards as kb

class Reg(StatesGroup):
    software_change_state = State()



DefaultRouter = Router()

@DefaultRouter.message(Command('softlist'))
async def checkCurrentSoftwareList(message:Message,state:FSMContext):
    """
    Обработчик команды /softlist.
    @/softlist - отправляет информацию о выбранном ПО для пользователя
    """
    print(message.chat.id)
    is_user_new = await check_if_user_registrated(message.from_user.id)
    print(f" is user registrated? - {is_user_new}")
    if is_user_new:
        softlist = await get_users_softlist(message.from_user.id)
        content = Text(Bold('Выбранное вами ПО для отслеживания:'))
        await message.answer(**content.as_kwargs(), reply_markup=ReplyKeyboardRemove())
        await message.answer(softlist)
    else:
        await message.answer('Вы не ввели список используемого ПО. Воспользуйтесь командой /start и нажмите на кнопку "Ввести список ПО" ')



@DefaultRouter.message(Command('change_softlist'))
async def anotherfunc(message:Message,state:FSMContext):
    """
    Обработчик команды /change_softlist.
    @/change_softlist - ожидает ввод нового списка ПО, после чего закрепляет его за пользователем
    """
    is_user_new = await check_if_user_registrated(message.from_user.id)
    print(f" is user old? - {is_user_new}")
    if is_user_new:
        await message.answer('Введите новый список ПО. Ведите перечисление строго через запятую, без пробелов, названия ПО должны начинаться с большой буквы.')
        await state.set_state(state = Reg.software_change_state)
    else:
        await message.answer('Вы не ввели список используемого ПО. Воспользуйтесь командой /start и нажмите на кнопку "Ввести список ПО" ')

@DefaultRouter.message(Reg.software_change_state)
async def anotherfunc(message:Message,state:FSMContext):
    print('registrating new soft')
    data = message.text
    software_list = softwareListStrToTuple(data)
    for i in software_list:
        print(i)
    await change_users_softlist(message.from_user.id, software_list)
    await message.answer('Список ПО успешно изменен.')
    await state.clear()
