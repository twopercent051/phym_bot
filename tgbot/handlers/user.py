from datetime import datetime, timedelta

from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram import F, Router
from aiogram.fsm.context import FSMContext

from create_bot import bot, config
from tgbot.keyboards.inline import UserInlineKeyboard
from tgbot.misc.states import UserFSM
from tgbot.misc.text_config import msg_config, next_step_timer, user_profile_config
from tgbot.models.sql_connector import UsersDAO, FeedbacksDAO
from tgbot.services.scheduler import update_scheduler

admin_group = config.tg_bot.admin_group
router = Router()


@router.message(Command('start'))
async def user_start(message: Message):
    user_id = str(message.from_user.id)
    username = f"@{message.from_user.username}" if message.from_user.username else ""
    user_profile = await UsersDAO.get_one_or_none(user_id=user_id)
    if user_profile:
        pass
    else:
        await UsersDAO.create(user_id=user_id, username=username)
    await msg_config(user_id=user_id, chapter="intro|greeting")
    # await update_scheduler(user_id=user_id, next_step="intro|how_it_work",
    #                        dtime=datetime.utcnow() + timedelta(hours=1))
    await update_scheduler(user_id=user_id, next_step="intro|how_it_work",
                           dtime=datetime.utcnow() + timedelta(seconds=5))


@router.callback_query(F.data == "no_ready")
async def heating(callback: CallbackQuery):
    user_id = callback.from_user.id
    next_step = "intro|heating"
    next_step_dtime = datetime.utcnow() + timedelta(days=2)
    next_step_dtime = datetime.utcnow() + timedelta(seconds=5)
    kb = UserInlineKeyboard.heating_kb()
    await msg_config(user_id=user_id, chapter="intro|heating", kb=kb)
    # await update_scheduler(user_id=user_id, next_step=next_step, dtime=next_step_dtime)


@router.callback_query(F.data == "yes_ready")
async def what_i_need(callback: CallbackQuery):
    user_id = str(callback.from_user.id)
    next_step_time = datetime.utcnow() + timedelta(hours=1)
    next_step_time = datetime.utcnow() + timedelta(seconds=5)
    await msg_config(user_id=user_id, chapter="intro|what_i_need")
    await update_scheduler(user_id=user_id, next_step="intro|start_polling", dtime=next_step_time)
    await bot.answer_callback_query(callback.id)


@router.callback_query(F.data == "ok")
async def start_polling(callback: CallbackQuery, state: FSMContext):
    text = 'Год рождения (YYYY)'
    await state.set_state(UserFSM.year)
    await callback.message.answer(text)
    await bot.answer_callback_query(callback.id)


@router.message(F.text, UserFSM.year)
async def year(message: Message, state: FSMContext):
    user_id = str(message.from_user.id)
    if message.text.isdigit() and 1900 < int(message.text) < 2022:
        await UsersDAO.update_user_id(user_id=user_id, year=int(message.text))
        text = 'Рост (в сантиметрах)'
        await state.set_state(UserFSM.height)
    else:
        text = 'Не похоже на правду'
    await message.answer(text)


@router.message(F.text, UserFSM.height)
async def height(message: Message, state: FSMContext):
    user_id = str(message.from_user.id)
    if message.text.isdigit() and 30 < int(message.text) < 250:
        await UsersDAO.update_user_id(user_id=user_id, height=int(message.text))
        text = 'Вес (в килограммах)'
        await state.set_state(UserFSM.weight)
    else:
        text = 'Не похоже на правду'
    await message.answer(text)


@router.message(F.text, UserFSM.weight)
async def weight(message: Message, state: FSMContext):
    user_id = str(message.from_user.id)
    if message.text.isdigit() and 30 < int(message.text) < 250:
        await UsersDAO.update_user_id(user_id=user_id, weight=int(message.text))
        text = 'Курите?'
        kb = UserInlineKeyboard.smoking_kb()
        await state.set_state(UserFSM.home)
    else:
        text = 'Не похоже на правду'
        kb = None
    await message.answer(text, reply_markup=kb)


@router.callback_query(F.data.split(":")[0] == "smoking")
async def smoking(callback: CallbackQuery):
    user_id = str(callback.from_user.id)
    is_smoking = callback.data.split(":")[1]
    await UsersDAO.update_user_id(user_id=user_id, smoking=is_smoking)
    text = 'Выпиваете?'
    kb = UserInlineKeyboard.drinking_kb()
    await callback.message.answer(text, reply_markup=kb)
    await bot.answer_callback_query(callback.id)


@router.callback_query(F.data.split(":")[0] == "drinking")
async def drinking(callback: CallbackQuery):
    user_id = str(callback.from_user.id)
    is_drinking = callback.data.split(":")[1]
    await UsersDAO.update_user_id(user_id=user_id, drinking=is_drinking)
    text = 'Ваш часовой пояс'
    kb = UserInlineKeyboard.timezone_kb()
    await callback.message.answer(text, reply_markup=kb)
    await bot.answer_callback_query(callback.id)


@router.callback_query(F.data.split(":")[0] == "tz")
async def timezone(callback: CallbackQuery):
    user_id = str(callback.from_user.id)
    tz = int(callback.data.split(":")[1]) + 3
    await UsersDAO.update_user_id(user_id=user_id, timezone=tz)
    text = "Отлично, спасибо. Ожидайте дальнейших сообщений."
    await callback.message.answer(text)
    next_step_time = next_step_timer(user_tz=tz, days_offset=1, tm_hours=20)
    next_step_time = datetime.utcnow() + timedelta(seconds=5)
    await update_scheduler(user_id=user_id, next_step="week:1|program", dtime=next_step_time)
    await bot.answer_callback_query(callback.id)


@router.callback_query(F.data.split(":")[0] == "feedback_1")
async def feedback_1(callback: CallbackQuery):
    user_id = str(callback.from_user.id)
    feedback = callback.data.split(":")[1]
    week_id = int(callback.data.split(':')[2])
    workout_id = int(callback.data.split(':')[3])
    await FeedbacksDAO.create(user_id=user_id, week_id=week_id, workout_id=workout_id, feedback_1=feedback)
    if feedback == 'positive' or feedback == 'partly':
        text = 'Насколько сложной оказалась тренировка?'
        kb = UserInlineKeyboard.feedback_2_kb(week_id=week_id, workout_id=workout_id)
    else:
        text = "Отлично, спасибо. Ожидайте дальнейших сообщений."
        kb = None
        next_step_time = datetime.utcnow() + timedelta(minutes=2)
        next_step_time = datetime.utcnow() + timedelta(seconds=5)
        await update_scheduler(user_id=user_id, next_step=f"workout:{workout_id}|week:{week_id}|support",
                               dtime=next_step_time)
    await callback.message.answer(text, reply_markup=kb)
    await bot.answer_callback_query(callback.id)


@router.callback_query(F.data.split(":")[0] == "feedback_2")
async def feedback_2(callback: CallbackQuery):
    user_id = str(callback.from_user.id)
    feedback = callback.data.split(':')[1]
    week_id = int(callback.data.split(':')[2])
    workout_id = int(callback.data.split(':')[3])
    await FeedbacksDAO.update_workout_id(user_id=user_id, workout_id=workout_id, week_id=week_id, feedback_2=feedback)
    text = "Отлично, спасибо. Ожидайте дальнейших сообщений."
    next_step_time = datetime.utcnow() + timedelta(minutes=2)
    next_step_time = datetime.utcnow() + timedelta(seconds=5)
    await update_scheduler(user_id=user_id, next_step=f"workout:{workout_id}|week:{week_id}|support",
                           dtime=next_step_time)
    await callback.message.answer(text)
    await bot.answer_callback_query(callback.id)


@router.callback_query(F.data.split(":")[0] == "feedback_week")
async def feedback_week(callback: CallbackQuery):
    user_id = str(callback.from_user.id)
    feedback = callback.data.split(':')[1]
    week_id = int(callback.data.split(':')[2])
    await FeedbacksDAO.update_week_id(user_id=user_id, week_id=week_id, feedback_week=feedback)
    if week_id == 3:
        kb = UserInlineKeyboard.trainer_kb()
        await msg_config(user_id=user_id, chapter="intro|finish_course", kb=kb)
    else:
        text = "Отлично, спасибо. Ожидайте дальнейших сообщений."
        user_profile = await UsersDAO.get_one_or_none(user_id=user_id)
        next_step_time = next_step_timer(user_tz=user_profile["timezone"], days_offset=1, tm_hours=20)
        next_step_time = datetime.utcnow() + timedelta(seconds=5)
        await update_scheduler(user_id=user_id, next_step=f"workout:1|week:{week_id + 1}|support", dtime=next_step_time)
        await callback.message.answer(text)
    await bot.answer_callback_query(callback.id)


@router.callback_query(F.data == "trainer")
async def get_trainer(callback: CallbackQuery, state: FSMContext):
    text = "Напишите как с вами связаться, например телефон"
    await state.set_state(UserFSM.trainer)
    await callback.message.answer(text)
    await bot.answer_callback_query(callback.id)


@router.message(F.text, UserFSM.trainer)
async def get_trainer(message: Message, state: FSMContext):
    user_id = str(message.from_user.id)
    user_text = "Отлично! Мы скоро с вами свяжемся по указанным контактам"
    await state.set_state(UserFSM.home)
    user = await UsersDAO.get_one_or_none(user_id=user_id)
    user_profile = await user_profile_config(user=user)
    admin_text = f"⚠️ Заявка на тренера:\n{user_profile}\nКонтакт: <i>{message.text}</i>"
    await message.answer(user_text)
    await bot.send_message(chat_id=admin_group, text=admin_text)


