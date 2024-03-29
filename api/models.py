from django.db import models

# Create your models here.
class Students(models.Model):
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    mobile_number=models.IntegerField()
    gender=models.CharField(max_length=100)
    college_email=models.EmailField(max_length=100)
    student_id=models.CharField(max_length=100)
    branch=models.CharField(max_length=100)
    section=models.CharField(max_length=100)
    isHosteler=models.BooleanField(default=False)
    university_roll_number=models.IntegerField()
    hacker_rank_id=models.CharField(max_length=100)
    isPaid=models.BooleanField(default=False)
    isVerified=models.BooleanField(default=False)
    token=models.CharField(max_length=100)
    isContestOnly=models.BooleanField(default=False)
    day1_att=models.BooleanField(default=False)
    day2_att=models.BooleanField(default=False)
    contest_att=models.BooleanField(default=False)
    date=models.DateTimeField(auto_now_add=True)
class Coordinators(models.Model):
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)

class Subscribers(models.Model):
    email=models.EmailField(max_length=100)
    date=models.DateTimeField(auto_now_add=True)
