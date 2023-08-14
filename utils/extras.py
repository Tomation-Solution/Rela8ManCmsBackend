import json
from django.conf import settings
import requests
from rest_framework import status
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
import json
from django.template.loader import render_to_string


from utils import custom_response, mailer
from payments.models import PublicationPayment, MembersAGMRegistration, EventTrainingRegistration, ExhibitorsAGMRegistration


def webhook_payment_handler(request, forWhat: str, ref: str, amount: float | int):
    if forWhat == "publication_purchase":
        reference_num = ref
        amount_paid = amount
        payment = get_object_or_404(PublicationPayment, ref=reference_num)
        amount_to_pay = int(float(payment.amount_to_pay))*100

        if amount_to_pay == amount_paid:
            payment.is_verified = True
            payment.save()

            current_site = get_current_site(request).domain

            relativePath = reverse("download-publication")
            viewPath = reverse("view-publication")

            purchase_item = "publication"

            absUrl = "http://" + current_site + \
                relativePath+"?ref="+str(reference_num)
            viewUrl = "http://" + current_site + \
                viewPath + "?ref="+str(reference_num)

            email_subject = "MAN purchase of publication"

            html_message = render_to_string('GetFile.html', {
                                            'purchase_download_url': absUrl, 'client_mail': payment.email, "purchase_item": purchase_item, "purchase_view_url": viewUrl})

            # my send mail utility class
            mailer.sib_send_mail(to=[{"email": payment.email, "name": payment.fullname}],
                                 html_content=html_message, subject=email_subject)

            # THIS WAS WRITTEN HERE AGAIN INCASE THE MAILING PROCESS EVER FAILS
            payment = get_object_or_404(
                PublicationPayment, ref=reference_num)
            payment.file_received = True
            payment.save()

    if forWhat in ("event_purchase", "training_purchase"):
        reference_num = ref
        amount_paid = amount
        payment = get_object_or_404(
            EventTrainingRegistration, ref=reference_num)
        amount_to_pay = int(float(payment.amount_to_pay))*100

        if amount_to_pay == amount_paid:
            payment.is_verified = True
            payment.save()

            registation_obj = model_to_dict(payment)

            if payment.type == "EVENT":
                registation_obj["event_training_name"] = payment.event.name

            elif payment.type == "TRAINING":
                registation_obj["event_training_name"] = payment.training.name

            email_subject = f"Registration for {registation_obj['type']}"

            html_message = render_to_string('EventTrainingRegistration.html', {
                                            'ref_no': registation_obj["ref"], 'client_mail': registation_obj["email"], 'registration_name': registation_obj['event_training_name'], 'type': registation_obj["type"]})

            # my send mail utility class
            mailer.sib_send_mail(to=[{"email": registation_obj["email"], "name": registation_obj["fullname"]}],
                                 html_content=html_message, subject=email_subject)

    if forWhat == "member_agm_purchase":
        reference_num = ref
        amount_paid = amount
        payment = get_object_or_404(
            MembersAGMRegistration, ref=reference_num)
        amount_to_pay = int(float(payment.amount_to_pay))*100

        if amount_to_pay == amount_paid:
            payment.is_verified = True
            payment.save()

            payment = model_to_dict(payment)

            email_subject = f"Registration for Annual General Meeting"

            html_message = render_to_string('EventTrainingRegistration.html', {
                                            'ref_no': payment["ref"], 'client_mail': payment["email"], 'registration_name': "MAN AGM event as a member", 'type': "Event"})

            # my send mail utility class
            mailer.sib_send_mail(to=[{"email": payment["email"], "name": payment["company_name"]}],
                                 html_content=html_message, subject=email_subject)

            # THIS WAS WRITTEN HERE AGAIN INCASE THE MAILING PROCESS EVER FAILS
            payment = get_object_or_404(
                MembersAGMRegistration, ref=reference_num)
            payment.mail_recevied = True
            payment.save()

    if forWhat == "exhibitor_agm_purchase":
        reference_num = ref
        amount_paid = amount
        payment = get_object_or_404(
            ExhibitorsAGMRegistration, ref=reference_num)
        amount_to_pay = int(float(payment.amount_to_pay))*100

        if amount_to_pay == amount_paid:
            payment.is_verified = True
            payment.save()

            payment = model_to_dict(payment)

            email_subject = f"Registration for Annual General Meeting"

            html_message = render_to_string('EventTrainingRegistration.html', {
                                            'ref_no': payment["ref"], 'client_mail': payment["email"], 'registration_name': "MAN AGM event an exhibitor", 'type': "AGM Event"})

            # my send mail utility class
            mailer.sib_send_mail(to=[{"email": payment["email"], "name": payment["company_name"]}],
                                 html_content=html_message, subject=email_subject)

            # THIS WAS WRITTEN HERE AGAIN INCASE THE MAILING PROCESS EVER FAILS
            payment = get_object_or_404(
                ExhibitorsAGMRegistration, ref=reference_num)
            payment.mail_recevied = True
            payment.save()

    return HttpResponse(status=200)


def generatePaystackLikeResponse(ref: str, link: str):
    return {
        "status": True,
        "message": "Authorization URL created",
        "data": {
            "authorization_url": link,
            "access_code": "",
            "reference": ref
        }
    }


def convert_naira_to_kobo(naira):
    naira = float(naira)*100
    kobo = int(naira)
    return kobo


def initialize_payment(reason_for_payment, amount, buyer_obj, callback_url=None):
    if settings.PAYSTACK_SECRET_KEY is None:
        return custom_response.Response(data={"message": "Oops invalid keys, please try again"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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

        return custom_response.Success_response(msg="payment initilaized", data=res_data)
    else:
        return custom_response.Response(data={"message": "something went wrong, please try again"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


def initialize_flutterwave_payment(reason_for_payment, amount, buyer_obj, callback_url=None):
    if settings.FLUTTERWAVE_SECRET_KEY is None:
        return custom_response.Response(data={"message": "Oops invalid keys, please try again"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if callback_url == None:
        callback_url = "https://man-new-test-site.netlify.app/"

    url = 'https://api.flutterwave.com/v3/payments'

    headers = {
        'Authorization': f'Bearer {settings.FLUTTERWAVE_SECRET_KEY}',
        'Content-Type': 'application/json',
        'Accept': 'application/json', }

    body = {
        'tx_ref': buyer_obj["ref"],
        'amount': amount,
        'currency': "NGN",
        'redirect_url': callback_url,
        'meta': {
            "forWhat": reason_for_payment,
        },
        'customer': {
            'email': buyer_obj["email"],
        },
    }

    try:
        res = requests.post(url, headers=headers, data=json.dumps(body))
    except requests.ConnectionError:
        return custom_response.Response(data={"error": "Network Error"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

    print(res.json())

    if res.status_code == 200:
        res_data = res.json()

        # return custom_response.Success_response(msg="payment initilaized", data=res_data)
        paystack_like_response = generatePaystackLikeResponse(
            ref=buyer_obj["ref"], link=res_data["data"]["link"])
        return custom_response.Success_response(msg="payment initilaized", data=paystack_like_response)
    else:
        return custom_response.Response(data={"message": "something went wrong, please try again"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
