import asyncio
from datetime import datetime

from create_bot import bot, config


from tgbot.services.celery_init import celery_app


@celery_app.task
def schedule_task():
    asyncio.run(bot.send_message(chat_id=389929933, text=f"Celery test at {datetime.now()}"))
    # print(datetime.now().second)


# schedule_task.apply_async(eta=datetime(2023, 6, 4, 11, 5))
# schedule_task.delay()

# while True:
#     pass
