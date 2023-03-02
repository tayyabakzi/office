from django.db import models


# Create your models here.
class Department(models.Model):
    departmentID = models.IntegerField(unique=True)
    departmentName = models.CharField(max_length=250)


class Team(models.Model):
    departmentID = models.ForeignKey(Department, on_delete=models.CASCADE)
    teamNumber = models.IntegerField()
    teamDescription = models.CharField(max_length=250)
