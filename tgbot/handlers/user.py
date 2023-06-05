from datetime import datetime, timedelta

from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram import F, Router
from aiogram.fsm.context import FSMContext

from tgbot.services.tasks import schedule_task

router = Router()


@router.message(Command('start'))
async def user_start(message: Message):
    schedule_task.apply_async(eta=datetime.utcnow() + timedelta(seconds=20))
    await message.answer('Доступ в бота возможен только из админской группы')


@router.message(F.text)
async def user_start(message: Message):
    await message.answer('Доступ в бота возможен только из админской группы')
