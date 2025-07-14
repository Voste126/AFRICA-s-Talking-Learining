from django.shortcuts import render

# Create your views here.
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings

logger = logging.getLogger(__name__)

class UssdCallbackView(APIView):
    """
    CBV to handle USSD menu requests from Africa's Talking.
    """

    def post(self, request, *args, **kwargs):
        # 1) Extract the USSD parameters
        session_id   = request.data.get("sessionId", "")
        service_code = request.data.get("serviceCode", "")
        phone_number = request.data.get("phoneNumber", "")
        text         = request.data.get("text", "")

        logger.debug(f"USSD Request: session={session_id} text={text}")

        # 2) Split the input text by '*' to get the menu path
        inputs = text.split("*") if text else []

        # 3) Begin your menu logic
        if text == "":
            # First screen
            response = (
                "CON Welcome to Offline Account Manager\n"
                "1. My Account\n"
                "2. My Phone Number"
            )

        elif inputs[0] == "1":
            # User chose "My Account"
            if len(inputs) == 1:
                # show sub-menu
                response = (
                    "CON Account Info\n"
                    "1. Account Number\n"
                    "2. Account Balance"
                )
            elif inputs[1] == "1":
                # 1*1 → Account Number
                account_number = "ACC1001"
                response = f"END Your account number is {account_number}"
            elif inputs[1] == "2":
                # 1*2 → Account Balance
                balance = "KES 10,000"
                response = f"END Your balance is {balance}"
            else:
                response = "END Invalid selection."

        elif inputs[0] == "2":
            # User chose "My Phone Number"
            response = f"END Your phone number is {phone_number}"

        else:
            # Fallback
            response = "END Invalid choice. Please try again."

        # 4) Return a plain‑text response with the proper prefix
        return Response(response, content_type="text/plain")
