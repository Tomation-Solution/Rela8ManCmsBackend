from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
import json
from publications.models import Publication
from payments.models import PublicationPayment, EventTrainingRegistration, MembersAGMRegistration, ExhibitorsAGMRegistration
from payments.serializers import PublicationPaymentSerailzer, EventTrainingRegistrationSerializer
from utils import custom_permissions, custom_response, mailer
from utils.extras import initialize_payment
from rest_framework import generics
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.template.loader import render_to_string

from utils.html2pdf import render_to_pdf


# Create your views here.

@csrf_exempt
def paystack_webhook(request, pk=None):
    payload = json.loads(request.body)
    meta_data = payload['data']['metadata']

    if payload.get('event') == 'charge.success':

        if meta_data["forWhat"] == "publication_purchase":
            reference_num = payload['data']['reference']
            amount_paid = payload['data']['amount']
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

        if meta_data["forWhat"] in ("event_purchase", "training_purchase"):
            reference_num = payload['data']['reference']
            amount_paid = payload['data']['amount']
            payment = get_object_or_404(
                EventTrainingRegistration, ref=reference_num)
            amount_to_pay = int(float(payment.amount_to_pay))*100

            if amount_to_pay == amount_paid:
                payment.is_verified = True
                payment.save()

        if meta_data["forWhat"] == "member_agm_purchase":
            reference_num = payload['data']['reference']
            amount_paid = payload['data']['amount']
            payment = get_object_or_404(
                MembersAGMRegistration, ref=reference_num)
            amount_to_pay = int(float(payment.amount_to_pay))*100

            if amount_to_pay == amount_paid:
                payment.is_verified = True
                payment.save()

            email_subject = f"Registration for Annual General Meeting"

            html_message = render_to_string('EventTrainingRegistration.html', {
                                            'ref_no': payment["ref"], 'client_mail': payment["email"], 'registration_name': "MAN AGM event as a member", 'type': "Event"})

            # my send mail utility class
            mailer.sib_send_mail(to=[{"email": payment["email"], "name": payment["company_name"]}],
                                 html_content=html_message, subject=email_subject)

        if meta_data["forWhat"] == "exhibitor_agm_purchase":
            reference_num = payload['data']['reference']
            amount_paid = payload['data']['amount']
            payment = get_object_or_404(
                ExhibitorsAGMRegistration, ref=reference_num)
            amount_to_pay = int(float(payment.amount_to_pay))*100

            if amount_to_pay == amount_paid:
                payment.is_verified = True
                payment.save()

            email_subject = f"Registration for Annual General Meeting"

            html_message = render_to_string('EventTrainingRegistration.html', {
                                            'ref_no': payment["ref"], 'client_mail': payment["email"], 'registration_name': "MAN AGM event an exhibitor", 'type': "AGM Event"})

            # my send mail utility class
            mailer.sib_send_mail(to=[{"email": payment["email"], "name": payment["company_name"]}],
                                 html_content=html_message, subject=email_subject)

    return HttpResponse(status=200)


class EventTrainingRegistrationView(generics.GenericAPIView):
    """
    class handles payments for events and trainings
    """
    serializer_class = EventTrainingRegistrationSerializer
    permission_classes = [custom_permissions.IsPostRequestOrAuthenticated]

    def get_queryset(self):
        return EventTrainingRegistration.objects.all()

    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(msg="events and trainings registrations", data=serializer.data)

    def post(self, request):
        body = request.data
        serializer = self.serializer_class(data=body)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        registration_instance = EventTrainingRegistration.objects.get(
            ref=serializer.data["ref"], email=serializer.data["email"])

        registation_obj = model_to_dict(registration_instance)

        if (registration_instance.type == "EVENT" and registration_instance.event.is_paid):
            event_amount = registration_instance.event.price
            return initialize_payment(reason_for_payment="event_purchase",
                                      amount=event_amount, buyer_obj=registation_obj)

        if (registration_instance.type == "TRAINING" and registration_instance.training.is_paid):
            event_amount = registration_instance.training.price
            return initialize_payment(reason_for_payment="training_purchase",
                                      amount=event_amount, buyer_obj=registation_obj)

        if registration_instance.type == "EVENT":
            registation_obj["event_training_name"] = registration_instance.event.name

        elif registration_instance.type == "TRAINING":
            registation_obj["event_training_name"] = registration_instance.training.name

        email_subject = f"Registration for {registation_obj['type']}"

        html_message = render_to_string('EventTrainingRegistration.html', {
                                        'ref_no': registation_obj["ref"], 'client_mail': registation_obj["email"], 'registration_name': registation_obj['event_training_name'], 'type': registation_obj["type"]})

        # my send mail utility class
        mailer.sib_send_mail(to=[{"email": registation_obj["email"], "name": registation_obj["fullname"]}],
                             html_content=html_message, subject=email_subject)

        return custom_response.Success_response(msg="event or training registration", data=serializer.data)


class PublicationPaymentView(generics.GenericAPIView):
    """
    class handles payments for publications
    """
    serializer_class = PublicationPaymentSerailzer
    permission_classes = [custom_permissions.IsPostRequestOrAuthenticated]

    def get_queryset(self):
        return PublicationPayment.objects.all()

    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)

        return custom_response.Success_response(msg="all publication payments attempted", data=serializer.data)

    def post(self, request):
        body = request.data
        serializer = self.serializer_class(data=body)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        buyer_instance = PublicationPayment.objects.get(
            ref=serializer.data["ref"], email=serializer.data["email"])
        publication_amount = buyer_instance.publication.price

        buyer_obj = model_to_dict(buyer_instance)

        reason_for_payment = "publication_purchase"

        return initialize_payment(reason_for_payment=reason_for_payment,
                                  amount=publication_amount, buyer_obj=buyer_obj, callback_url="https://man-new-test-site.netlify.app/paid-publications")


class ViewPublicationPDF(generics.GenericAPIView):
    """
        class for viewing publications pdf to be downloaded by users
    """

    def get(self, request):
        ref = request.GET.get("ref")

        publication_payment = get_object_or_404(PublicationPayment, ref=ref)
        publication_obj = Publication.objects.get(
            pk=publication_payment.publication.pk)
        publication = model_to_dict(publication_obj)

        created_at = publication_obj.created_at.date()

        read_more_link = publication_obj.link.url

        publications_type = publication_obj.type.name

        pdf = render_to_pdf('PublicationHtml2Pdf.html', {"read_more_link": read_more_link,
                            "created_at": created_at, "publications_type": publications_type, **publication})
        return HttpResponse(pdf, content_type='application/pdf')


class DownloadPublicationPDF(generics.GenericAPIView):
    """
        class generating the publications pdf to be downloaded by users
    """

    def get(self, request):
        ref = request.GET.get("ref")

        publication_payment = get_object_or_404(PublicationPayment, ref=ref)
        publication_obj = Publication.objects.get(
            pk=publication_payment.publication.pk)
        publication = model_to_dict(publication_obj)

        created_at = publication_obj.created_at.date()

        read_more_link = publication_obj.link.url

        publications_type = publication_obj.type.name

        pdf = render_to_pdf('PublicationHtml2Pdf.html', {"read_more_link": read_more_link,
                            "created_at": created_at, "publications_type": publications_type, **publication})

        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Publication_%s.pdf" % (f"{publication['name']}")
        content = "attachment; filename=%s" % (filename)
        response['Content-Disposition'] = content
        return response
