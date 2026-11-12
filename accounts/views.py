from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.serializers import UserSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


class Register(APIView):
    def post(self,request):
        serializer_instance=UserSerializer(data=request.data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(serializer_instance.data,status=status.HTTP_201_CREATED) 
        else:
           return Response(serializer_instance.errors,status=status.HTTP_400_BAD_REQUEST)
                        
class LogoutAPIView(APIView):
    permission_classes=[IsAuthenticated,]
    def get(self,request):
        print(self.request.user) #Prints the currently logged-in user's details in the terminal.
        self.request.user.auth_token.delete()
        return Response({"message":"Logout successsfully"})
