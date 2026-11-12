from rest_framework import serializers
from booking.models import Booking
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model=Booking
        fields="__all__"
        read_only_fields=["user","amount",'created_at',"status"]



    def validate(self,data):
        event=data['event']
        seats=data['seats']

        if event.available_seats<seats:
            raise serializers.ValidationError("seats are not available")
        return data