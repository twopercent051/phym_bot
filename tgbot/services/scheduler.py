from datetime import datetime, timedelta

from create_bot import bot, scheduler
from tgbot.keyboards.inline import UserInlineKeyboard
from tgbot.misc.text_config import msg_config, next_step_timer
from tgbot.models.sql_connector import UsersDAO


async def main_dispatcher(user_id: str, step: str, feedback: str|None):
    next_step, next_step_dtime, kb = None, None, None
    if step == "intro|how_it_work":
        next_step = "intro|are_you_ready"
        next_step_dtime = datetime.utcnow() + timedelta(hours=1)
        next_step_dtime = datetime.utcnow() + timedelta(seconds=5)
    if step == "intro|are_you_ready":
        next_step = "intro|heating"
        next_step_dtime = datetime.utcnow() + timedelta(days=1)
        next_step_dtime = datetime.utcnow() + timedelta(seconds=5)
        kb = UserInlineKeyboard.are_you_ready_kb()
    if step == "intro|heating":
        next_step = "intro|heating"
        next_step_dtime = datetime.utcnow() + timedelta(days=2)
        next_step_dtime = datetime.utcnow() + timedelta(seconds=5)
        kb = UserInlineKeyboard.heating_kb()
    if step == "intro|start_polling":
        kb = UserInlineKeyboard.ok_kb()
        await msg_config(user_id=user_id, chapter=step, kb=kb)
        return
    if step.split(":")[0] == "week":
        user_profile = await UsersDAO.get_one_or_none(user_id=user_id)
        tz = user_profile["timezone"]
        week_id = step.split("|")[0].split(":")[1]
        subject = step.split("|")[1]
        if subject == "program":
            next_step = f"week:{week_id}|focus"
            next_step_dtime = datetime.utcnow() + timedelta(hours=1)
            next_step_dtime = datetime.utcnow() + timedelta(seconds=5)
        if subject == "focus":
            next_step = f"workout:1|week:{week_id}|program"
            next_step_dtime = next_step_timer(user_tz=tz, days_offset=1, tm_hours=12)
            next_step_dtime = datetime.utcnow() + timedelta(seconds=5)
        if subject == "congratulation":
            next_step = f"week:{week_id}|general_practices"
            next_step_dtime = next_step_timer(user_tz=tz, days_offset=1, tm_hours=10)
            next_step_dtime = datetime.utcnow() + timedelta(seconds=5)
        if subject == "general_practices":
            next_step = f"week:{week_id}|trichotomy_practices"
            next_step_dtime = next_step_timer(user_tz=tz, days_offset=0, tm_hours=12)
            next_step_dtime = datetime.utcnow() + timedelta(seconds=5)
        if subject == "trichotomy_practices":
            next_step = f"week:{week_id}|feedback"
            next_step_dtime = next_step_timer(user_tz=tz, days_offset=0, tm_hours=20)
            next_step_dtime = datetime.utcnow() + timedelta(seconds=5)
        if subject == "feedback":
            kb = UserInlineKeyboard.feedback_week_kb(week_id=week_id)
    if step.split(":")[0] == "workout":
        user_profile = await UsersDAO.get_one_or_none(user_id=user_id)
        tz = user_profile["timezone"]
        workout_id = step.split("|")[0].split(":")[1]
        week_id = step.split("|")[1].split(":")[1]
        subject = step.split("|")[2]
        if subject == "program":
            next_step = f"workout:{workout_id}|week:{week_id}|reminder"
            next_step_dtime = next_step_timer(user_tz=tz, days_offset=0, tm_hours=20)
            next_step_dtime = datetime.utcnow() + timedelta(seconds=5)
        if subject == "reminder":
            next_step = f"workout:{workout_id}|week:{week_id}|feedback_1"
            next_step_dtime = next_step_timer(user_tz=tz, days_offset=1, tm_hours=20)
            next_step_dtime = datetime.utcnow() + timedelta(seconds=5)
        if subject == "feedback_1":
            text = "Как прошла вчерашняя тренировка? Поделись обратной связью:"
            kb = UserInlineKeyboard.feedback_1_kb(week_id=week_id, workout_id=workout_id)
            await bot.send_message(chat_id=user_id, text=text, reply_markup=kb)
            return
        if subject == "support":
            next_step = f"workout:{workout_id}|week:{week_id}|habit"
            next_step_dtime = next_step_timer(user_tz=tz, days_offset=1, tm_hours=10)
            next_step_dtime = datetime.utcnow() + timedelta(seconds=5)
            if feedback == "negative":
                step = f"workout:{workout_id}|week:{week_id}|sup_negative"
            else:
                step = f"workout:{workout_id}|week:{week_id}|sup_positive"
        if subject == "habit":
            if workout_id == 1 or workout_id == 2:
                next_step_dtime = next_step_timer(user_tz=tz, days_offset=1, tm_hours=12)
                next_step_dtime = datetime.utcnow() + timedelta(seconds=5)
                next_step = f"workout:{workout_id + 1}|week:{week_id}|program"
            else:
                next_step = f"week:{week_id}|congratulation"
                next_step_dtime = next_step_timer(user_tz=tz, days_offset=0, tm_hours=21)
                next_step_dtime = datetime.utcnow() + timedelta(seconds=5)
    await msg_config(user_id=user_id, chapter=step, kb=kb)
    await update_scheduler(user_id=user_id, next_step=next_step, dtime=next_step_dtime)


async def update_scheduler(user_id: str, next_step: str, dtime: datetime, feedback=None):
    await UsersDAO.update_user_id(user_id=user_id, next_step=next_step, dtime=dtime)
    scheduler.add_job(
        main_dispatcher,
        "date",
        next_run_time=dtime,
        kwargs={
            "user_id": user_id,
            "step": next_step,
            "feedback": feedback
        }
    )
