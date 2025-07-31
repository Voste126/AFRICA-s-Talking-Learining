import os
import google.auth
from google.auth.transport.requests import Request
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.parsers import FormParser
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import logging
import requests

logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name="dispatch")
class UssdCallbackView(APIView):
    parser_classes = [FormParser]
    """
    CBV to handle USSD menu requests for HiveGuard Swarm-Loss Cover
    """

    # Vertex AI endpoint
    RISK_API_URL = (
        "https://us-central1-aiplatform.googleapis.com/v1/"
        "projects/450588661119/locations/us-central1/"
        "endpoints/4641525664493600768:predict"
    )

    def _get_bearer_token(self):
        # use ADC to fetch an OAuth2 token
        creds, project = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
        creds.refresh(Request())
        return creds.token

    def post(self, request, *args, **kwargs):
        try:
            text = request.POST.get("text", "").strip()
            inputs = text.split("*") if text else []
            level = len(inputs)
            session_lang = inputs[0] if level > 0 else None

            # Initial prompt / language selection
            if level == 0:
                response = "CON Chagua lugha / Choose language:\n1. English\n2. Kiswahili"

            else:
                lang = inputs[0]
                # English questions
                questions_en = {
                    2: "CON How many hives do you have? (Enter number):",
                    3: "CON Rate average hive health (1=Poor to 5=Excellent):",
                    4: "CON Years of beekeeping experience?",
                    5: "CON Do you practice swarm prevention (1=Yes 2=No)?",
                    6: "CON Enter your apiary location (County-Ward):",
                }
                # Kiswahili questions
                questions_sw = {
                    2: "CON Una makopo ngapi? (Weka idadi):",
                    3: "CON Kadiria afya ya makopo (1=Dhini 5=Bora):",
                    4: "CON Umekuwa ukulima nyuki kwa miaka mingapi?",
                    5: "CON Je, unatumia mbinu za kuzuia swarm? (1=Ndiyo 2=Hapana)",
                    6: "CON Weka eneo la zuiaji lako (Kaunti-Ward):",
                }

                # Debug logging for USSD flow
                logger.info(f"Current level: {level}, Inputs: {inputs}, Language: {lang}")

                if level == 1:
                    # After language choice, ask for number of hives
                    response = questions_en[2] if lang == '1' else questions_sw[2]
                
                elif 2 <= level <= 6:
                    # Handle questions 2 through 6
                    qdict = questions_en if lang == '1' else questions_sw
                    response = qdict.get(level, "END Invalid question level.")
                    logger.info(f"Sending question for level {level}: {response}")

                elif level == 7:
                    # Debug logging for input processing
                    logger.info(f"Processing final inputs. Total inputs: {len(inputs)}")
                    for i, val in enumerate(inputs):
                        logger.info(f"Input {i}: {val}")

                    # extract the six USSD inputs with validation
                    phone_number = request.POST["phoneNumber"]
                    if len(inputs) < 7:
                        logger.error(f"Insufficient inputs: {len(inputs)}")
                        return HttpResponse(
                            "END Session error. Please start over.",
                            content_type="text/plain"
                        )
                        
                    # Map inputs to variables with proper indexes
                    hive_input = inputs[1]      # First answer after language selection
                    health_input = inputs[2]    # Health rating
                    experience_input = inputs[3] # Years of experience
                    prevention_input = inputs[4] # Prevention practice
                    location = inputs[5]        # Location
                    
                    # Validate numeric inputs with error handling
                    try:
                        # Validate hive count with better error handling
                        if len(inputs) <= 1 or not hive_input:
                            error_msg = "Please enter the number of hives." if lang == '1' else "Tafadhali weka idadi ya mizinga."
                            return HttpResponse(f"END {error_msg}", content_type="text/plain")
                        
                        # Strip any whitespace and check if it's a valid number
                        hive_input = hive_input.strip()
                        
                        # Debug logging
                        logger.info(f"Validating hive count input: '{hive_input}', language: {lang}")
                        
                        # Remove any non-digit characters
                        clean_input = ''.join(filter(str.isdigit, hive_input))
                        
                        if not clean_input:
                            error_msg = "Please enter only numbers for hive count." if lang == '1' else "Tafadhali tumia nambari tu kwa idadi ya mizinga."
                            return HttpResponse(f"END {error_msg}", content_type="text/plain")
                            
                        try:
                            hive_count = int(clean_input)
                            if hive_count <= 0:
                                error_msg = "Number of hives must be greater than 0." if lang == '1' else "Idadi ya mizinga lazima iwe zaidi ya sufuri."
                                return HttpResponse(f"END {error_msg}", content_type="text/plain")
                            if hive_count > 1000:
                                error_msg = "The number of hives seems too high. Please enter a realistic number." if lang == '1' else "Idadi ya mizinga ni kubwa mno. Tafadhali weka nambari inayowezekana."
                                return HttpResponse(f"END {error_msg}", content_type="text/plain")
                        except ValueError:
                            error_msg = "Please enter a valid number for hive count." if lang == '1' else "Tafadhali weka nambari halali ya mizinga."
                            return HttpResponse(f"END {error_msg}", content_type="text/plain")
                        
                        if not inputs[3].isdigit() or not 1 <= int(inputs[3]) <= 5:
                            return HttpResponse(
                                "END Invalid health rating. Please enter a number between 1 and 5.",
                                content_type="text/plain"
                            )
                        health_index = int(inputs[3])
                        
                        if not inputs[4].isdigit():
                            return HttpResponse(
                                "END Invalid experience value. Please enter number of years.",
                                content_type="text/plain"
                            )
                        experience = int(inputs[4])
                        
                        if inputs[5] not in ['1', '2']:
                            return HttpResponse(
                                "END Invalid prevention practice choice. Please select 1 for Yes or 2 for No.",
                                content_type="text/plain"
                            )
                        prevention_bool = (inputs[5] == "1")
                        
                    except (IndexError, ValueError) as e:
                        logger.error(f"Input validation error: {str(e)}")
                        return HttpResponse(
                            "END Invalid input format. Please start over.",
                            content_type="text/plain"
                        )

                    try:
                        # build the Vertex AI request
                        body = {
                            "instances": [
                                {
                                    "location": location,
                                    "hiveCount": hive_count,
                                    "healthIndex": health_index,
                                    "experienceYears": experience,
                                    "preventionPractice": prevention_bool
                                }
                            ]
                        }

                        # Try to get OAuth bearer and make API call
                        token = self._get_bearer_token()
                        headers = {
                            "Authorization": f"Bearer {token}",
                            "Content-Type": "application/json"
                        }

                        res = requests.post(self.RISK_API_URL, json=body, headers=headers)
                        res.raise_for_status()
                        predictions = res.json().get("predictions", [])
                        if not predictions:
                            raise ValueError("No predictions in response")

                        # Vertex AI returns a list of predictions
                        pred = predictions[0]
                        risk_score = pred.get("risk_score")
                        premium = pred.get("premium")
                        cover_amt = pred.get("cover_amount")

                    except google.auth.exceptions.DefaultCredentialsError:
                        logger.warning("Using mock response - Google Cloud credentials not configured")
                        # Calculate mock risk score based on inputs
                        base_risk = 50
                        health_factor = (6 - health_index) * 5  # Higher health = lower risk
                        exp_factor = min(experience, 10) * 2  # Cap experience benefit at 10 years
                        prevention_factor = 10 if prevention_bool else 0
                        
                        risk_score = max(20, min(90, base_risk + health_factor - exp_factor - prevention_factor))
                        
                        # Calculate premium with more realistic factors
                        base_premium = 750  # Base premium per hive in KES
                        risk_multiplier = (risk_score / 50)  # Risk score affects premium
                        volume_discount = max(0, min(0.3, (hive_count - 1) * 0.05))  # 5% discount per hive up to 30%
                        
                        premium = round(hive_count * base_premium * risk_multiplier * (1 - volume_discount), -2)  # Round to nearest 100
                        cover_amt = round(premium * 4, -2)  # Round to nearest 100
                    
                    except Exception as e:
                        logger.error(f"Error calling Vertex AI: {str(e)}")
                        # Simplified fallback calculation
                        risk_score = 75
                        premium = round(hive_count * 1000, -2)  # Simple calculation, rounded to nearest 100
                        cover_amt = round(premium * 3, -2)

                    # Format numbers with thousand separators
                    premium_fmt = "{:,.0f}".format(premium)
                    cover_fmt = "{:,.0f}".format(cover_amt)
                    risk_fmt = "{:.0f}".format(risk_score)

                    if lang == '1':
                        response = (
                            f"CON Your swarm-risk score: {risk_fmt}%\n"
                            f"Premium: KES {premium_fmt}\n"
                            f"Cover amount: KES {cover_fmt}\n"
                            "1. Confirm & Pay\n"
                            "2. Cancel"
                        )
                    else:
                        response = (
                            f"CON Alama yako ya hatari ya swarm: {risk_fmt}%\n"
                            f"Ada: KES {premium_fmt}\n"
                            f"Kiasi cha bima: KES {cover_fmt}\n"
                            "1. Thibitisha & Lipa\n"
                            "2. Ghairi"
                        )

                elif level == 8:
                    choice = inputs[7]
                    if choice == '1':
                        # Trigger MPESA STK Push separately in backend
                        if lang == '1':
                            response = "END Payment initiated. Thank you for protecting your hive!"
                        else:
                            response = "END Lipa imeanzishwa. Asante kwa kulinda zuiaji lako!"
                    else:
                        if lang == '1':
                            response = "END You have cancelled the purchase."
                        else:
                            response = "END Umeghairi ununuzi."
                else:
                    # Fallback
                    response = "END Invalid selection. Session ended."

            return HttpResponse(
                response,
                content_type="text/plain; charset=utf-8",
                headers={"Access-Control-Allow-Origin": "*", "Cache-Control": "no-cache"},
            )

        except Exception as e:
            logger.exception("USSD flow error")
            return HttpResponse("END An error occurred. Try again later.", content_type="text/plain")

    def get(self, request, *args, **kwargs):
        return HttpResponse("This endpoint only accepts POST.", status=400)


