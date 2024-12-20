import time

from config.celery import app


@app.task
def celery_test_task():
    time.sleep(10)
    return "Celery task completed"
