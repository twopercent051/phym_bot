from datetime import datetime, timedelta

from create_bot import bot, logger
from tgbot.models.sql_connector import TextsDAO, UsersDAO, FeedbacksDAO


async def msg_config(user_id: str, chapter: str, kb=None):
    text_data = await TextsDAO.get_one_or_none(chapter=chapter)
    if text_data:
        text = text_data["text"] if text_data["text"] else "Текст отсутствует"
        photo_id = text_data["photo_id"] if text_data["photo_id"] else None
    else:
        text = "Текст отсутствует"
        photo_id = None
    try:
        if photo_id:
            await bot.send_photo(chat_id=user_id, photo=photo_id, caption=text,
                                 reply_markup=kb)
        else:
            await bot.send_message(chat_id=user_id, text=text, reply_markup=kb)
    except Exception as ex:
        logger.info(f"{user_id} || {ex}")


def next_step_timer(user_tz: int, days_offset: int, tm_hours: int) -> datetime:
    user_time = datetime.utcnow() + timedelta(hours=user_tz)
    user_next_day = user_time + timedelta(days=days_offset)
    user_next_day_mod = user_next_day.replace(hour=tm_hours, minute=0)
    utc_result = user_next_day_mod - timedelta(hours=user_tz)
    return utc_result


async def user_profile_config(user: dict) -> str:
    text = [
        f"<b>{user['username']}</b> [{user['user_id']}]\n",
        f"Год рождения: <i>{user['year']}</i>",
        f"Рост: <i>{user['height']} см</i>",
        f"Вес: <i>{user['weight']} кг</i>",
        f"Курение: <i>{user['smoking']}</i>",
        f"Алкоголь: <i>{user['drinking']}</i>",
    ]
    return "\n".join(text)


async def user_feedbacks(user_id: str) -> str:
    feedbacks = await FeedbacksDAO.get_many(user_id=user_id)
    result = []
    for week_id in range(1, 4):
        result.append(f"Неделя {week_id}")
        for workout_id in range(1, 4):
            for fb in feedbacks:
                if fb["week_id"] == week_id and fb["workout_id"] == workout_id:
                    result.append(f"Тренировка {workout_id}: <i>{fb['feedback_1']}</i> | <i>{fb['feedback_2']}</i>")
        for fb in feedbacks:
            if fb["week_id"] == week_id:
                result.append(f"Итог недели: <i>{fb['feedback_week']}</i>\n")
                break
    return "\n".join(result)
