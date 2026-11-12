from django.db import models
from accounts.models import MyUser
from events.models import Event
from datetime import datetime,timedelta

class Booking(models.Model):
    status_choices=[("pending","Pending"),("confirmed","Confirmed"),("expired","Expired"),("cancelled","Cancelled")]
    event=models.ForeignKey(Event,on_delete=models.CASCADE)
    user=models.ForeignKey(MyUser,on_delete=models.CASCADE)
    seats=models.IntegerField()
    amount=models.IntegerField()
    status=models.CharField(max_length=20,choices=status_choices,default="pending")
    ticket_code=models.CharField(max_length=50,unique=True,null=True) #after confirmation we create ticket
    created_at=models.DateTimeField(auto_now_add=True)
    ticket_code=models.CharField(max_length=50,unique=True,blank=True)


#this function checks expiration before making payment
    def check_expiration(self):
        # dynamically calculates if 15 minutes have passed since the booking was created.if yes changes the status to expired
        time=self.created_at+timedelta(minutes=15)
        if datetime.now()>time:
            self.status="expired"
            self.save()
        return    