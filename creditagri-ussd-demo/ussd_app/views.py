from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
import logging

logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
class UssdCallbackView(APIView):
    """
    CBV to handle USSD menu requests from Africa's Talking.
    """

    def post(self, request, *args, **kwargs):
        # Get the POST data
        session_id = request.POST.get("sessionId", None)
        service_code = request.POST.get("serviceCode", None)
        phone_number = request.POST.get("phoneNumber", None)
        text = request.POST.get("text", "default")

        logger.info(f"Received USSD request: session={session_id}, code={service_code}, phone={phone_number}, text={text}")

        # Process user input
        if text == '':
            response = "CON What would you want to check \n"
            response += "1. My Account \n"
            response += "2. My phone number"
        
        elif text == '1':
            response = "CON Choose account information you want to view \n"
            response += "1. Account number \n"
            response += "2. Account balance"
        
        elif text == '1*1':
            account_number = "ACC1001"
            response = "END Your account number is " + account_number
        
        elif text == '1*2':
            balance = "KES 10,000"
            response = "END Your balance is " + balance
        
        elif text == '2':
            response = "END This is your phone number " + phone_number
        
        else:
            response = "END Invalid input. Please try again."

        # Return response with proper content type
        return HttpResponse(response, content_type='text/plain')