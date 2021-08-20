import random
import time
import os
from typing import Tuple

from celery import Celery

broker_url = os.getenv('CELERY_BROKER_URL', 'redis://@localhost:6379/0')
app = Celery('tasks', broker=broker_url)


@app.task
def post_submission(solution_id: id) -> Tuple[int, str]:
    """
    Recieve solution id for check
    """
    id = int(time.time() * 1000)
    status = random.choice([*['evaluation'] * 10, 'correct', 'wrong'])

    return id, status

@app.task
def get_submission(id: int) -> Tuple[int, str]:
    status = random.choice([*['evaluation'] * 10, 'correct', 'wrong'])

    return id, status
