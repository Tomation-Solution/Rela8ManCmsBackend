from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions
import secrets
import json
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.http import require_POST

from utils import extras

'''
{
  "event": "charge.completed",
  "data": {
    "id": 285959875,
    "tx_ref": "Links-616626414629",
    "flw_ref": "PeterEkene/FLW270177170",
    "device_fingerprint": "a42937f4a73ce8bb8b8df14e63a2df31",
    "amount": 100,
    "currency": "NGN",
    "charged_amount": 100,
    "app_fee": 1.4,
    "merchant_fee": 0,
    "processor_response": "Approved by Financial Institution",
    "auth_model": "PIN",
    "ip": "197.210.64.96",
    "narration": "CARD Transaction ",
    "status": "successful",
    "payment_type": "card",
    "created_at": "2020-07-06T19:17:04.000Z",
    "account_id": 17321,
    "customer": {
      "id": 215604089,
      "name": "Yemi Desola",
      "phone_number": null,
      "email": "user@gmail.com",
      "created_at": "2020-07-06T19:17:04.000Z"
    },
    "card": {
      "first_6digits": "123456",
      "last_4digits": "7889",
      "issuer": "VERVE FIRST CITY MONUMENT BANK PLC",
      "country": "NG",
      "type": "VERVE",
      "expiry": "02/23"
    }
  }
}
'''


@require_POST
@csrf_exempt
def flutterwave_webhook(request, pk=None):
    "this function receives payload from flutter wave"
    data = json.loads(request.body)
    main_data = data.get('data', "")

    print("all_payload_data", data)

    # VERIFY IF REQUEST COMES FROM FLUTTERWAVE
    secret_hash = settings.FLUTTERWAVE_SECRET_HASH

    signature = request.headers.get("verifi-hash")

    if signature == None or (signature != secret_hash):
        return HttpResponse(status=401)

    if data.get("event", "") == "charge.completed" and main_data["status"] == "successful":
        print("tx_ref", main_data.get("tx_ref", ""))
        print("amount", main_data.get("amount", ""))

        # forWhat = main_data.get["meta"]["forWhat"]
        # ref = main_data.get("tx_ref", "")
        # amount = main_data.get("amount", "")

        # return extras.webhook_payment_handler(request=request, forWhat=forWhat, ref=ref, amount=amount)

    return HttpResponse(status=200)

# @csrf_exempt
# def useFlutterWaveWebhook(request,pk=None):
#     'this receives payload from flutter waVE'
#     forWhat,user_id,instanceID,schema_name,amount = data.get('txRef').split('---')[1].split('--')
#     meta_data ={
#         'forWhat':forWhat,
#         'instanceID':instanceID,
#         'schema_name':schema_name,
#         'amount_to_be_paid':amount,
#     }
#     connection.set_schema(schema_name=meta_data['schema_name'])
#     user = get_user_model().objects.get(id=user_id)
#     # meta_data['member_id']= Memeber.objects.filter(user=user).first().id

#     if data.get('status') == 'successful' or data.get('event') == 'charge.completed':
#         return webhookPayloadHandler(meta_data,user)


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
