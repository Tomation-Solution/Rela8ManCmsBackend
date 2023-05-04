import json
from django.conf import settings
import requests
from rest_framework import status

from utils import custom_response


def convert_naira_to_kobo(naira):
    naira = float(naira)*100
    kobo = int(naira)
    return kobo


def initialize_payment(reason_for_payment, amount, buyer_obj, callback_url=None):
    if callback_url == None:
        callback_url = "https://man-new-test-site.netlify.app/"

    url = 'https://api.paystack.co/transaction/initialize/'
    headers = {
        'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
        'Content-Type': 'application/json',
        'Accept': 'application/json', }
    body = {
        "email": buyer_obj["email"],
        "amount": convert_naira_to_kobo(amount),
        "callback_url": callback_url,
        "reference": buyer_obj["ref"],
        "metadata": {
            "forWhat": reason_for_payment,
        }
    }

    try:
        res = requests.post(url, headers=headers, data=json.dumps(body))
    except requests.ConnectionError:
        return custom_response.Response(data={"error": "Network Error"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

    if res.status_code == 200:
        res_data = res.json()

        return custom_response.Success_response(msg="purchase initilaized", data=res_data)
    else:
        return custom_response.Response(data={"message": "something went wrong, please try again"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
