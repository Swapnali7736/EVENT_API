from rest_framework import serializers
from accounts.models import MyUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=MyUser
        fields=["id","username","password","email","first_name","last_name","role","phone"]
        read_only_fields=["id",]




## used to encrypt the password/password hashing(Password hashing is used to protect users' passwords from being exposed if someone accesses the database.)
    def create(self,validated_data):
        u=MyUser.objects.create_user(**validated_data)
        u.save()
        return u    