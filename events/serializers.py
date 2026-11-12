
from rest_framework import serializers
from events.models import Event
from datetime import datetime


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model=Event
        fields="__all__"
        read_only_fields=["organizer","created_at"]





    def validate(self,data):
        date=data['date']
        todays_date=datetime.today().date()
        if date<todays_date:
            raise serializers.ValidationError('invalid date')
        return data


# datetime.today()--Current date and time
# datetime.today().date()--Only date
# datetime.today().time()--Only time
# datetime.today().year--Current year
# datetime.today().month--Current month
# datetime.today().day--Current day
