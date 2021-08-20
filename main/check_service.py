import random
import time
from typing import Tuple

from django.core.cache import cache
from celery import shared_task

from .models import Submission


@shared_task
def long_check(submission_id: int):
    """
    Emulate long checking
    """
    time.sleep(20)

    submission = Submission.objects.get(id=submission_id)
    submission.status = random.choice(['correct', 'wrong'])
    submission.save()

    cache.delete(f'submission_status_{submission_id}')


def post_submission(problem_id: int, reply: str) -> Tuple[int, str]:
    """
    Receive solution id for check
    """
    new_submission = Submission(code=reply, problem_id=problem_id)
    new_submission.status = 'evaluation'
    new_submission.save()

    long_check.delay(new_submission.id)

    return new_submission.id, new_submission.status


async def get_submission(submission_id: int) -> Tuple[int, str]:
    """
    Get submission status
    """
    status = await Submission.get_status_by_id(submission_id)

    return submission_id, status
