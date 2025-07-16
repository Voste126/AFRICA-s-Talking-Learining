from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.parsers import FormParser
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import logging
import json

logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class UssdCallbackView(APIView):
    parser_classes = [FormParser]
    """
    CBV to handle USSD menu requests from Africa's Talking.
    """

    def post(self, request, *args, **kwargs):
        try:
            # Log request info
            logger.info("=== USSD Request Received ===")
            logger.info(f"Request Method: {request.method}")
            logger.info(f"Content-Type: {request.content_type}")
            logger.info(f"POST Data: {request.POST}")

            # Get the POST data and clean it
            text = request.POST.get("text", "default").strip()
            session_id = request.POST.get("sessionId", "default")
            phone_number = request.POST.get("phoneNumber", "default")
            service_code = request.POST.get("serviceCode", "default")

            logger.info(f"Received Parameters:")
            logger.info(f"text: '{text}'")  # Added quotes to see exact text
            logger.info(f"sessionId: {session_id}")
            logger.info(f"phoneNumber: {phone_number}")
            logger.info(f"serviceCode: {service_code}")

            # Split input and clean it
            inputs = [part.strip() for part in text.split('*')] if text else []
            logger.info(f"Split inputs: {inputs}")

            # Menu logic
            if not text or text == "":
                response = "CON Welcome to Offline Account Manager\n"
                response += "1. My Account\n"
                response += "2. My Phone Number"
                logger.info("Sending initial menu")
            
            elif text == "1":
                response = "CON Account Info\n"
                response += "1. Account Number\n"
                response += "2. Account Balance"
                logger.info("Sending account menu")
            
            elif len(inputs) >= 2 and inputs[0] == "1":
                if inputs[1] == "1":
                    response = "END Your account number is ACC1001"
                    logger.info("Sending account number")
                elif inputs[1] == "2":
                    response = "END Your balance is KES 10,000"
                    logger.info("Sending balance")
                else:
                    response = "END Invalid selection for account info"
                    logger.info("Invalid account selection")
            
            elif text == "2":
                response = f"END Your phone number is {phone_number}"
                logger.info("Sending phone number")
            
            else:
                response = "END Invalid choice. Please try again."
                logger.info("Sending invalid choice message")

            logger.info(f"Final Response: '{response}'")  # Added quotes to see exact response

            # Send response with proper headers
            return HttpResponse(
                response,
                content_type='text/plain; charset=utf-8',
                headers={
                    'Access-Control-Allow-Origin': '*',
                    'Cache-Control': 'no-cache'
                }
            )

        except Exception as e:
            logger.error(f"Error in USSD processing: {str(e)}", exc_info=True)
            return HttpResponse(
                "END An error occurred",
                content_type='text/plain; charset=utf-8'
            )

    def get(self, request, *args, **kwargs):
        return HttpResponse(
            "This endpoint only accepts POST requests",
            status=400,
            content_type='text/plain; charset=utf-8'
        )
