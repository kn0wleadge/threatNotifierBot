import asyncio
import logging
import os

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv
load_dotenv()
from aiogram import Bot, Dispatcher, F


bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()

def init_bot():
# Загрузка переменных окружения
    
    print("bot init ;)")
    
