# from __future__ import absolute_import, unicode_literals
import asyncio
# import subprocess


# from celery import current_app
# from celery.bin import worker

from tgbot.handlers.admin import router as admin_router
from tgbot.handlers.user import router as user_router
from tgbot.handlers.echo import router as echo_router
from tgbot.misc.scheduler import scheduler_jobs
from tgbot.models.redis_connector import RedisConnector as rds

from create_bot import bot, dp, scheduler, logger, register_global_middlewares, config


async def main():
    logger.info("Starting bot")
    scheduler_jobs()
    rds.redis_start()

    dp.include_routers(admin_router, user_router, echo_router)
    # # worker = celery_app.Worker()
    # # process = subprocess.Popen(celery_app.Worker())
    # subprocess.call(celery_app.Worker())
    try:
        # process.start()
        # # subprocess.call(worker.start())
        scheduler.start()
        register_global_middlewares(dp, config)
        await dp.start_polling(bot)
    finally:
        await dp.storage.close()
        await bot.session.close()
        scheduler.shutdown(True)


if __name__ == '__main__':
    try:
        asyncio.run(main())
        # worker = celery_app.Worker()
        # worker.start()
        # worker.run(**options)
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
