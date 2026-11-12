from rest_framework.views import APIView
from rest_framework.response import Response
from booking.permissions import IsCustomer
from rest_framework.authentication import TokenAuthentication
from booking.serializers import BookingSerializer
from rest_framework import status
from booking.models import Booking
from django.shortcuts import get_object_or_404
from events.models import Event
from rest_framework.permissions import IsAuthenticated

class BookingEvent(APIView):
    permission_classes=[IsCustomer]
    authentication_classes= [TokenAuthentication]
    def post(self,request):
        
        serializer_instance=BookingSerializer(data=request.data)
        if serializer_instance.is_valid():
            data=serializer_instance.validated_data

            event=data["event"]
            seats=data["seats"]
            amount=event.amount*seats

            u=request.user
            serializer_instance.save(user=u,amount=amount)
            response={
                        "message":"""Booking successfully created. payment is pending,make your payment within 15 minutes""",
                        "booking_data":serializer_instance.data
                    }
            return Response(response,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer_instance.errors,status=status.HTTP_400_BAD_REQUEST)


    def get(self,request):
        user=request.user
        if(user.role=="customer"):
            b=Booking.objects.filter(user=request.user)
        else:
            b=Booking.objects.filter(event__organizer=request.user)
        serializer_instance=BookingSerializer(b,many=True)
        return Response(serializer_instance.data,status=status.HTTP_200_OK)  


class BookingRud(APIView):
    permission_classes=[IsCustomer]
    authentication_classes=[TokenAuthentication]
    def get(self,request,i): 
        b = Booking.objects.get(id=i,user=request.user)
        self.check_object_permissions(request,b)
        serializer_instance=BookingSerializer(b)
        return Response(serializer_instance.data,status=status.HTTP_200_OK)


    def put(self,request,i):
        b=Booking.objects.get(id=i, user=request.user)
        self.check_object_permissions(request,b)
        serializer_instance=BookingSerializer(b,data=request.data)
        if serializer_instance.is_valid():
            data=serializer_instance.validated_data
            event=data["event"]
            seats=data["seats"]
            amount=event.amount*seats
            serializer_instance.save(amount=amount)
            return Response(serializer_instance.data, status=status.HTTP_200_OK)
        return Response(serializer_instance.errors, status=status.HTTP_400_BAD_REQUEST)



    def delete(self, request, i):
        b=Booking.objects.get(id=i,user=request.user)
        self.check_object_permissions(request,b)
        b.delete()
        return Response({"message":"Booking deleted successfully"},status=status.HTTP_200_OK)


#Booking cancelling view
class BookingCancel(APIView):
    permission_classes=[IsCustomer]
    authentication_classes=[TokenAuthentication]
    def get(self,request,i):
        b=get_object_or_404(Booking,id=i)
        self.check_object_permissions(request,b)
        b.status="cancelled"
        b.save()
        return Response({"message":"booking successfully cancelled"},status=status.HTTP_200_OK)



# AI CHATBOT INTEGRATION

from google import genai
from google.genai import types
## heres api_key is pasted in .env so below 4 lines are used to connect this code to .env
import os
from dotenv import load_dotenv
load_dotenv()
api_key=os.getenv("api_key")

client=genai.Client(api_key=api_key)  # create a client connection using api key
class  AIChatbotView(APIView):
    permission_classes=[IsAuthenticated,]
    authentication_classes=[TokenAuthentication]
    def post(self,request):
        user_msg=request.data['message']
        if not user_msg:
            return Response({"user message is required"},status=status.HTTP_400_BAD_REQUEST)
        user=request.user
        user_role=user.role
        user_name=user.username
        #fetches the active events from database
        active_events=Event.objects.filter(available_seats__gt=0)
        print(active_events)
        if active_events:
            #converts this qs into text format or more readable format
            event_lists=""
            for e in active_events:
                event_list=f"Title:{e.title},organizer:{e.organizer.username},Description:{e.description},date:{e.date},time:{e.time},venue:{e.venue},availableseats:{e.available_seats}"
            print(event_list)
            database_context=f"These are the current live events:{event_list}"
        else:
            database_context=f"There are no active events in our database"
        system_instruction = (
             f"You are a dedicated AI Assistant for our Event Booking Platform.\n"
              f"The user speaking to you is '{user_name}' who is a '{user_role}'.\n\n"
             "STRICT GUIDELINES:\n"
            "1. ONLY answer questions related to events in our database, ticket prices, seat counts, booking workflows, or event creation support.\n"
             "2. If the user asks general knowledge questions, coding/math help, general news, or anything UNRELATED to events or our platform, politely reply:\n"
             "   'ക്ഷമിക്കണം, എനിക്ക് ഈവന്റുകളുമായും ബുക്കിംഗുമായും ബന്ധപ്പെട്ട ചോദ്യങ്ങൾക്ക് മാത്രമേ മറുപടി നൽകാൻ സാധിക്കൂ.' (or equivalent in English if the query is in English).\n"
             "3. Do NOT make up fake events. Only answer using the live database events provided below.\n\n"
            f"{database_context}"
             )
       # to create response
        try:
            response=client.models.generate_content(
                model="gemini-3.5-flash",
                contents=user_msg,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,temperature=0.7

                )
            )

            return Response({"message":response.text},status=status.HTTP_200_OK)
        except:
            return Response({"message":"error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)