from django.db import models

# Create your models here.
class Students(models.Model):
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    mobile_number=models.IntegerField()
    gender=models.CharField(max_length=100)
    college_email=models.EmailField(max_length=100)
    student_id=models.IntegerField()
    branch=models.CharField(max_length=100)
    section=models.CharField(max_length=100)
    isHosteler=models.BooleanField()
    hacker_rank_id=models.CharField(max_length=100)
    isPaid=models.BooleanField(default=False)
    

