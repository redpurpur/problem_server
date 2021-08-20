from django.db import models
from channels.db import database_sync_to_async


class Problem(models.Model):

    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return f'Задача {self.id}'


class Submission(models.Model):

    class Status(models.TextChoices):
        EVALUATION = 'evaluation', 'evaluation'
        CORRECT = 'correct', 'correct'
        WRONG = 'wrong', 'wrong'

    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    code = models.TextField()
    status = models.CharField(max_length=30, null=True, default=Status.EVALUATION, choices=Status.choices)

    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Решение'
        verbose_name_plural = 'Решения'

    def __str__(self):
        return f'Решение {self.id}'

    @classmethod
    @database_sync_to_async
    def get_status_by_id(cls, solution_id: int) -> str:
        solution = cls.objects.filter(id=solution_id).first()
        if solution:
            return solution.status
        return 'not exist'
