from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.parsers import FormParser
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import logging

logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
class UssdCallbackView(APIView):
    parser_classes = [FormParser]
    """
    CBV to handle USSD menu requests from Africa's Talking.
    Bilingual quiz for Kenya's crop & livestock farmers.
    """

    def post(self, request, *args, **kwargs):
        try:
            text = request.POST.get("text", "").strip()
            session_id = request.POST.get("sessionId", "")
            phone_number = request.POST.get("phoneNumber", "")
            service_code = request.POST.get("serviceCode", "")

            inputs = text.split("*") if text else []
            level = len(inputs)

            # Language selection is first
            if level == 0:
                response = "CON Choose language:\n1. English\n2. Kiswahili"
            else:
                lang = inputs[0]
                # Define English questions
                questions_en = {
                    2: "CON What is your main enterprise?\n1. Maize\n2. Coffee\n3. Dairy cattle\n4. Poultry\n5. Other",
                    3: "CON Enter your farm size (acres for crops or herd size for livestock):",
                    4: "CON What was your last season's estimated revenue (KES)?",
                    5: "CON How many years have you been farming?",
                    6: "CON Do you have any collateral?\n1. Yes\n2. No",
                    7: "CON Have you taken and repaid a farm loan before?\n1. Yes\n2. No"
                }
                # Define Swahili questions
                questions_sw = {
                    2: "CON Chagua shughuli yako kuu ya kilimo:\n1. Mahindi\n2. Kahawa\n3. Ng'ombe wa maziwa\n4. Kuku\n5. Nyingine",
                    3: "CON Weka ukubwa wa shamba lako (ekari kwa mazao au idadi ya mifugo):",
                    4: "CON Je, mapato yako ya msimu uliopita yalikuwa kiasi gani (KES)?",
                    5: "CON Umekuwa ukifanya kilimo kwa miaka mingapi?",
                    6: "CON Je, una dhamana yoyote?\n1. Ndiyo\n2. Hapana",
                    7: "CON Je, umewahi kuchukua na kurudisha mkopo wa kilimo hapo awali?\n1. Ndiyo\n2. Hapana"
                }

                # Build response based on level
                if level == 1:
                    response = questions_en[2] if lang == '1' else questions_sw[2]
                elif level in range(2, 7):
                    idx = level + 1
                    qdict = questions_en if lang == '1' else questions_sw
                    response = qdict.get(idx, "END Invalid selection. Session ended.")
                elif level == 7:
                    # Parse responses
                    enterprise = inputs[1]
                    farm_size = float(inputs[2])
                    revenue = float(inputs[3])
                    years = int(inputs[4])
                    collateral = inputs[5]
                    repaid = inputs[6]

                    # Simple scoring heuristic
                    score = 50
                    score += min(farm_size, 20) * 1.5
                    score += min(revenue/10000, 10)*2
                    score += min(years, 10)
                    if collateral == '1': score += 10
                    if repaid == '1': score += 10
                    score = min(score, 100)

                    # Loan recommendation
                    loan_min = int(score * 50)
                    loan_max = int(score * 100)

                    if lang == '1':
                        response = (
                            f"END Your CreditAgri score is {score:.0f}.\n"
                            f"Recommended loan: KES {loan_min}-{loan_max}.\n"
                            "1. Accept and join guarantee pool\n"
                            "2. Decline"
                        )
                    else:
                        response = (
                            f"END Alama yako ya CreditAgri ni {score:.0f}.\n"
                            f"Mkopo unaopendekezwa: KES {loan_min}-{loan_max}.\n"
                            "1. Kubali na ujiunge na kikundi cha dhamana\n"
                            "2. Katisha"
                        )
                else:
                    # Handle post-recommendation choice
                    choice = inputs[7] if level > 7 else None
                    if choice == '1':
                        response = "END " + ("Thank you! You've joined the guarantee pool." if lang == '1' else "Asante! Umejiunga na kikundi cha dhamana.")
                    elif choice == '2':
                        response = "END " + ("You have declined the loan recommendation." if lang == '1' else "Umekatisha pendekezo la mkopo.")
                    else:
                        response = "END " + ("Invalid choice. Session ended." if lang == '1' else "Chaguo batili. Kikao kimebaki.")

            logger.info(f"Response: {response}")
            return HttpResponse(
                response,
                content_type='text/plain; charset=utf-8',
                headers={'Access-Control-Allow-Origin': '*', 'Cache-Control': 'no-cache'}
            )

        except Exception as e:
            logger.error(f"Error: {e}", exc_info=True)
            return HttpResponse(
                "END An error occurred. Please try again later.",
                content_type='text/plain; charset=utf-8'
            )

    def get(self, request, *args, **kwargs):
        return HttpResponse(
            "This endpoint only accepts POST.",
            status=400,
            content_type='text/plain; charset=utf-8'
        )

