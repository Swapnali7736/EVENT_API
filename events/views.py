from rest_framework.views import APIView
from rest_framework.response import Response
from events.models import Event
from events.serializers import EventSerializer
from rest_framework import status
from events.permissions import IsOrganizerOrReadOnly

class EventAPI(APIView):
    permission_classes=[IsOrganizerOrReadOnly]

    #listing all events
    def get(self,request):
          e=Event.objects.all()
          serializer_instance=EventSerializer(e,many=True)
          return Response(serializer_instance.data,status=status.HTTP_200_OK)


    #creating a new event
    def post(self,request):
        serializer_instance=EventSerializer(data=request.data)
        if serializer_instance.is_valid():
             serializer_instance.save(organizer=request.user)
             return Response(serializer_instance.data,status=status.HTTP_201_CREATED)
        else:
             return Response(serializer_instance.errors,status=status.HTTP_400_BAD_REQUEST)    


class EventRetrieveUpdateDelete(APIView):
    permission_classes=[IsOrganizerOrReadOnly]

    def get(self,request,i):
          e=Event.objects.get(id=i)
          serializer_instance=EventSerializer(e)
          return Response(serializer_instance.data,status=status.HTTP_200_OK)

    def put(self,request,i):
         e=Event.objects.get(id=i)
         self.check_object_permissions(request,e)
         serializer_instance=EventSerializer(e,data=request.data)
         if serializer_instance.is_valid():
              serializer_instance.save()
              return Response(serializer_instance.data,status=status.HTTP_200_OK)
         else:
              return Response(serializer_instance.errors,status=status.HTTP_400_BAD_REQUEST)
             
    def delete(self,request,i):
         e=Event.objects.get(id=i)
         self.check_object_permissions(request,e)
         e.delete()
         return Response({"message":"deleted"},status=status.HTTP_204_NO_CONTENT)         