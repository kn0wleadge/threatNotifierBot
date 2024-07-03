import asyncio
import logging
import os

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, F

from parser.run_parser import main as parse_data

from bot_init import init_bot

from tgbot.database.models import async_main
from tgbot.database.get_all_soft import get_all_soft
from tgbot.database.connect_soft import connect_soft

from tgbot.database.add_threat import add_threat

from tgbot.services.send_threat import send_threat

from bot_init import bot, dp
 
from tgbot.handlers.startHandlers import StartRouter
from tgbot.handlers.defaultHandlers import DefaultRouter
from tgbot.handlers.new_user_handlers import NewUserRouter
async def scheduled_task():
    threats_info = await parse_data()
    print(f'added threats - {threats_info}')
    print(f"count of threats - {len(threats_info)}")
    for threat in threats_info:
        
        #Отправка пользователям информации об угрозе
        print("Sending info")
        await send_threat(threat)

async def main():
          
    # Инициализация базы данных
    await async_main()

    
    dp.include_router(StartRouter)
    dp.include_router(DefaultRouter)
    dp.include_router(NewUserRouter)
    # Инициализация планировщика
    scheduler = AsyncIOScheduler()
    scheduler.add_job(scheduled_task, 'interval', minutes=30)
    scheduler.start()
    logging.info("Scheduler started")

    # Запуск первого парсинга немедленно
    asyncio.create_task(scheduled_task())

    # Запуск бота
    await dp.start_polling(bot)

if __name__ == '__main__':
    
    logging.basicConfig(level = logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info('Exit')
