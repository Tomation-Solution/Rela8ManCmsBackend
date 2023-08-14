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

    signature = request.headers.get("Verif-Hash")

    if signature == None or (signature != secret_hash):
        return HttpResponse(status=401)

    if main_data["status"] == "successful" and main_data["currency"] == "NGN":
        reason_for_payment, ref = main_data.get('txRef').split("--")
        amount = main_data.get("amount", "")

        return extras.webhook_payment_handler(request=request, forWhat=reason_for_payment, ref=ref, amount=amount)

    return HttpResponse(status=500)
