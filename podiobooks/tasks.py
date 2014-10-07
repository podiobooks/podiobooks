import logging

from podiobooks.celery import app

logger = logging.getLogger("root")


@app.task
def hello_world():
    logger.error("JUST TESTING FROM TASK")
