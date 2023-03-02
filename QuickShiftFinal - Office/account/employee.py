from django.db import models
from django.contrib.auth.models import User

from account.Department import Department, Team


class Employee(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    Emp_Id = models.IntegerField(verbose_name='Employee ID', unique=True)
    first_name = models.CharField(max_length=50, verbose_name='First Name')
    last_name =models.CharField(max_length=50, verbose_name='Last Name')
    is_on_schedule = models.BooleanField(default=False, verbose_name='On Schedule')
    department =  models.ForeignKey(Department, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)
    manager_id = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='employees', verbose_name='Manager')
