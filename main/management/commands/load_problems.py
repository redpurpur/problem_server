from django.core.management.base import BaseCommand
from main.models import Problem


class Command(BaseCommand):
    help = 'Добавить в базу тестовые задачи'

    def handle(self, *args, **options):
        problems = [
            {'name': 'Сумма двух', 'description': 'Напишите метод суммирующий два числа a и b'},
        ]

        new_problems = list()
        for p in problems:
            new_problems.append(
                Problem(name=p['name'], description=p['description']),
            )

        Problem.objects.bulk_create(new_problems)
