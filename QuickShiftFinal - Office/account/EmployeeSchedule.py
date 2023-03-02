from django.db import models

# Create your models here.
from account.employee import Employee


class EmployeeSchedule(models.Model):
    Emp_Id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    schedule_date = models.DateTimeField()
    working_status = models.CharField(max_length=1)
    seat_no = models.CharField(max_length=20)