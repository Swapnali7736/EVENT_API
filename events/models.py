from django.db import models
from accounts.models import MyUser
class Event(models.Model):
    title=models.CharField(max_length=30)
    description=models.TextField()
    date=models.DateField()
    time=models.TimeField()
    venue=models.CharField(max_length=100)
    amount=models.IntegerField()
    organizer=models.ForeignKey(MyUser,on_delete=models.CASCADE)
    total_seats=models.IntegerField()
    available_seats=models.IntegerField()
    created_at=models.DateTimeField(auto_now_add=True)