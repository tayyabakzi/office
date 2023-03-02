from django.apps import AppConfig
from account.management.commands.start_scheduler import Command as startSchedulerCommand

class AccountConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "account"

#    def ready(self):
#        startSchedulerCommand.handle(self)
#