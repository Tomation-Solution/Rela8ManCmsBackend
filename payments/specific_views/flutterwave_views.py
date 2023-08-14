from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions
import secrets
import json
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.http import require_POST

from utils import extras


@require_POST
@csrf_exempt
def flutterwave_webhook(request, pk=None):
    "this function receives payload from flutter wave"

    main_data = json.loads(request.body)

    # VERIFY IF REQUEST COMES FROM FLUTTERWAVE
    secret_hash = settings.FLUTTERWAVE_SECRET_HASH
    print("Personal hash key", secret_hash)

    signature = request.headers.get("verifi-hash")
    print("Flutter hash key", signature)

    if signature == None or (signature != secret_hash):
        return HttpResponse(status=401)

    if main_data["status"] == "successful" and main_data["currency"] == "NGN":
        reason_for_payment, ref = main_data.get('txRef').split("--")
        amount = main_data.get("amount", "")

        print({
            "amount": amount,
            "reason_for_payment": reason_for_payment,
            "ref": ref
        })

        # return extras.webhook_payment_handler(request=request, forWhat=forWhat, ref=ref, amount=amount)

    return HttpResponse(status=200)


class TestFlutterWavePayment(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        ref = secrets.token_urlsafe(20)
        buyer_obj = {
            "email": "popoolakejiah@gmail.com",
            "ref": ref
        }

        return extras.initialize_flutterwave_payment(
            "food", 50, buyer_obj, "www.youtube.com")
