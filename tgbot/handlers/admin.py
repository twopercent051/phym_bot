import os

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import Command
from aiogram import F, Router

from create_bot import bot, config
from tgbot.filters.admin import AdminFilter
from tgbot.keyboards.inline import AdminInlineKeyboard
from tgbot.misc.states import AdminFSM
from tgbot.misc.text_config import user_profile_config, user_feedbacks
from tgbot.models.sql_connector import TextsDAO, UsersDAO
from tgbot.services.xlsx_create import create_excel

admin_group = config.tg_bot.admin_group

router = Router()
router.message.filter(AdminFilter())
router.callback_query.filter(AdminFilter())


@router.message(Command('start'))
async def main_menu(message: Message, state: FSMContext):
    text = "Добро пожаловать в  главное меню"
    kb = AdminInlineKeyboard.main_menu_kb()
    await state.set_state(AdminFSM.home)
    await message.answer(text, reply_markup=kb)


@router.callback_query(F.data == "home")
async def main_menu(callback: CallbackQuery, state: FSMContext):
    text = "Добро пожаловать в  главное меню"
    kb = AdminInlineKeyboard.main_menu_kb()
    await state.set_state(AdminFSM.home)
    await callback.message.answer(text, reply_markup=kb)
    await bot.answer_callback_query(callback.id)


@router.callback_query(F.data == "edit_text")
async def edit_text(callback: CallbackQuery):
    text = "Выберите раздел редактирования"
    kb = AdminInlineKeyboard.edition_menu()
    await callback.message.answer(text, reply_markup=kb)
    await bot.answer_callback_query(callback.id)


@router.callback_query(F.data.split(":")[0] == "week")
async def edit_week(callback: CallbackQuery, state: FSMContext):
    week_id = callback.data.split(":")[1]
    text = "Выберите раздел редактирования"
    kb = AdminInlineKeyboard.week_menu()
    await state.update_data(week_id=week_id)
    await callback.message.answer(text, reply_markup=kb)
    await bot.answer_callback_query(callback.id)


@router.callback_query(F.data.split(":")[0] == "workout")
async def edit_workout(callback: CallbackQuery, state: FSMContext):
    workout_id = callback.data.split(":")[1]
    await state.update_data(workout_id=workout_id)
    text = "Выберите раздел редактирования"
    kb = AdminInlineKeyboard.workout_menu()
    await callback.message.answer(text, reply_markup=kb)
    await bot.answer_callback_query(callback.id)


@router.callback_query(F.data.split(":")[0] == "edit")
async def edit_text(callback: CallbackQuery, state: FSMContext):
    chapter = callback.data.split("|")[0].split(":")[1]
    subject = callback.data.split("|")[1]
    if chapter == "intro":
        query = f"intro|{subject}"
    elif chapter == "week":
        state_data = await state.get_data()
        week_id = state_data["week_id"]
        query = f"week:{week_id}|{subject}"
    else:
        state_data = await state.get_data()
        week_id = state_data["week_id"]
        workout_id = state_data["workout_id"]
        query = f"workout:{workout_id}|week:{week_id}|{subject}"
    await state.update_data(query=query)
    msg_sql = await TextsDAO.get_one_or_none(chapter=query)
    kb = AdminInlineKeyboard.home_kb()
    if msg_sql:
        await callback.message.answer("Сейчас сообщение такое:")
        await state.update_data(is_none=False)
        if msg_sql["photo_id"]:
            await callback.message.answer_photo(photo=msg_sql["photo_id"], caption=msg_sql["text"], reply_markup=kb)
        else:
            await callback.message.answer(msg_sql["text"])
    else:
        text = "Отправьте текст или картинку с текстом одним сообщением. Форматирование будет сохранено"
        await callback.message.answer(text, reply_markup=kb)
        await state.update_data(is_none=True)
    await state.set_state(AdminFSM.edit)
    await bot.answer_callback_query(callback.id)


@router.message(F.text, AdminFSM.edit)
@router.message(F.photo, AdminFSM.edit)
async def edit_intro(message: Message, state: FSMContext):
    state_data = await state.get_data()
    is_none = state_data["is_none"]
    photo_id = None
    if message.photo:
        photo_id = message.photo[-1].file_id
    new_text = message.html_text
    text = "Сообщение сохранено"
    kb = AdminInlineKeyboard.home_kb()
    if is_none:
        await TextsDAO.create(chapter=state_data["query"], photo_id=photo_id, text=new_text)
    else:
        await TextsDAO.update(chapter=state_data["query"], photo_id=photo_id, text=new_text)
    await state.set_state(AdminFSM.home)
    await message.answer(text, reply_markup=kb)


@router.callback_query(F.data == "users")
async def find_user(callback: CallbackQuery):
    user_list = await UsersDAO.get_many()
    await create_excel(user_list=user_list)
    kb = AdminInlineKeyboard.users_kb()
    file = FSInputFile(path=f'{os.getcwd()}/user_list.xlsx', filename=f"user_list.xlsx")
    await bot.send_document(chat_id=admin_group, document=file, reply_markup=kb)
    await bot.answer_callback_query(callback.id)


@router.callback_query(F.data == "find_user")
async def find_user(callback: CallbackQuery, state: FSMContext):
    text = "Введите id пользователя"
    kb = AdminInlineKeyboard.home_kb()
    await state.set_state(AdminFSM.users)
    await callback.message.answer(text, reply_markup=kb)
    await bot.answer_callback_query(callback.id)


@router.message(F.text, AdminFSM.users)
async def user_profile(message: Message, state: FSMContext):
    user_id = message.text
    user = await UsersDAO.get_one_or_none(user_id=user_id)
    kb = AdminInlineKeyboard.home_kb()
    if user:
        profile_text = await user_profile_config(user=user)
        text = await user_feedbacks(user_id=user_id)
        await message.answer(profile_text)
    else:
        text = "Такой пользователь не найден"
    await state.set_state(AdminFSM.home)
    await message.answer(text, reply_markup=kb)
