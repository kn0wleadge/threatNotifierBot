from aiogram import F,Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.utils.formatting import Text
from aiogram.utils.formatting import Bold

from tgbot.services.softwareListStrToTuple import softwareListStrToTuple

from tgbot.database.requests import get_users_softlist,check_if_user_registrated, change_users_softlist
from tgbot.database.current_threats import current_threats
from tgbot.database.all_solved_threats import all_solved_threats
from tgbot.keyboards.all_threats_keyboard import all_threats_keyboard
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
async def change_softlist_command(message:Message,state:FSMContext):
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
async def changing_softlist(message:Message,state:FSMContext):
    print('registrating new soft')
    data = message.text
    software_list = softwareListStrToTuple(data)
    for i in software_list:
        print(i)
    await change_users_softlist(message.from_user.id, software_list)
    await message.answer('Список ПО успешно изменен.')
    await state.clear()

@DefaultRouter.message(Command('help'))
async def help_command(message:Message):
    print('help command')
    await message.answer('Этот бот будет оперативно отправлять вам информацию о новых угрозах, которые публикуются на онлайн-порталах угроз информационной безопасности. Перечень команд:\n/help -справочная информация\n/softlist - актуальный список выбранного вами ПО\n/change_softlist - изменить список ПО\n/threats - вывести угрозы, находящиеся в обработке\n/all_threats - вывести список всех решенных угроз')

@DefaultRouter.message(Command('threats'))
async def threats_command(message:Message):
    #TODO - предусмотреть возможность отправки огромного количество угроз
    print('threats')
    threats = await current_threats(message.chat.id)
    await message.answer(text = "Список обрабатываемых угроз:")
    for threat in threats:        
        await message.answer(text = threat['message'], reply_markup=threat['builder'].as_markup())

@DefaultRouter.message(Command('all_threats'))
async def all_threats_command(message:Message):
    #TODO - предусмотреть возможность отправки огромного количество угроз
    print('all_threats')

    await message.answer(text = "Список устраненных угроз:",
                         reply_markup=all_threats_keyboard)
    solved_threats = await all_solved_threats(message.chat.id)
    threat_counter = 0
    for threat in solved_threats:
        threat_counter = threat_counter + 1     
        print(solved_threats)
        try:

            await message.answer(text = f'{threat_counter}' + ')'+'BDU' + threat.url[25:] + '\n' + 'Описание угрозы:\n' + threat.description + '\nДата устранения:\n' + threat.solve_date.strftime("%m/%d/%Y, %H:%M:%S") + '\nОписание устранения уязвимости:\n' + threat.threat_solution)
        except Exception as e:
            print(f'all_threats_command - {e}')