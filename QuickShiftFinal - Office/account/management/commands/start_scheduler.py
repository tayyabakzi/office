from django.core.management.base import BaseCommand
from account.worker import worker


class Command(BaseCommand):
    help = 'Start scheduler'

    def handle(self, *args, **options):
        print('Scheduler started!!')
        worker()
