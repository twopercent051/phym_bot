from celery import Celery

from create_bot import config


celery_app = Celery(
    "tasks",
    broker=f"redis://{config.rds.host}:{config.rds.port}",
    include=["tgbot.services.tasks"]
)
