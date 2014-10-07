import logging

from podiobooks.celery import app

logger = logging.getLogger("celerytasks")


@app.task
def hello_world():
    logger.error("JUST TESTING")
