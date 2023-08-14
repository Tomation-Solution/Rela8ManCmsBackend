from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
import json
from publications.models import Publication
from payments.models import PublicationPayment, EventTrainingRegistration, MembersAGMRegistration, ExhibitorsAGMRegistration
from payments.serializers import PublicationPaymentSerailzer, EventTrainingRegistrationSerializer
from utils import custom_permissions, custom_response, mailer
from utils.extras import initialize_payment, webhook_payment_handler
from rest_framework import generics, status
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST

from utils.html2pdf import render_to_pdf


# Create your views here.
@require_POST
@csrf_exempt
def paystack_webhook(request, pk=None):
    payload = json.loads(request.body)
    meta_data = payload['data']['metadata']

    forWhat = meta_data["forWhat"]
    ref = payload['data']['reference']
    amount = payload['data']['amount']

    if payload.get('event') == 'charge.success':
        return webhook_payment_handler(request=request, forWhat=forWhat, ref=ref, amount=amount)

    return HttpResponse(status=500)


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
        gatewaytype = request.GET.get("gatewaytype", "")
        serializer = self.serializer_class(data=body)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        registration_instance = EventTrainingRegistration.objects.get(
            ref=serializer.data["ref"], email=serializer.data["email"])

        registation_obj = model_to_dict(registration_instance)

        if (registration_instance.type == "EVENT" and registration_instance.event.is_paid):
            event_amount = registration_instance.event.price
            return initialize_payment(reason_for_payment="event_purchase",
                                      gatewaytype=gatewaytype,
                                      amount=event_amount, buyer_obj=registation_obj)

        if (registration_instance.type == "TRAINING" and registration_instance.training.is_paid):
            event_amount = registration_instance.training.price
            return initialize_payment(reason_for_payment="training_purchase",
                                      gatewaytype=gatewaytype,
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
        gatewaytype = request.GET.get("gatewaytype", "")
        serializer = self.serializer_class(data=body)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        buyer_instance = PublicationPayment.objects.get(
            ref=serializer.data["ref"], email=serializer.data["email"])
        publication_amount = buyer_instance.publication.price

        buyer_obj = model_to_dict(buyer_instance)

        reason_for_payment = "publication_purchase"

        return initialize_payment(reason_for_payment=reason_for_payment,
                                  gatewaytype=gatewaytype,
                                  amount=publication_amount, buyer_obj=buyer_obj, callback_url="https://man-new-test-site.netlify.app/paid-publications")


class ViewPublicationPDF(generics.GenericAPIView):
    """
        class for viewing publications pdf to be downloaded by users
    """

    def get(self, request):
        ref = request.GET.get("ref")

        publication_payment = get_object_or_404(PublicationPayment, ref=ref)

        try:
            publication_obj = Publication.objects.get(
                pk=publication_payment.publication.pk)

            publication = model_to_dict(publication_obj)

            created_at = publication_obj.created_at.date()

            read_more_link = ""

            read_more_link_2 = ""

            if (publication_obj.link):
                read_more_link = publication_obj.link.url

            if (publication_obj.readmore_link):
                read_more_link_2 = publication_obj.readmore_link

            publications_type = publication_obj.type.name

            pdf = render_to_pdf('PublicationHtml2Pdf.html', {"read_more_link": read_more_link, "read_more_link_2": read_more_link_2,
                                "created_at": created_at, "publications_type": publications_type, **publication})
            return HttpResponse(pdf, content_type='application/pdf')
        except:
            return Response(data={"message": "failed to get publication"}, status=status.HTTP_404_NOT_FOUND)


class DownloadPublicationPDF(generics.GenericAPIView):
    """
        class generating the publications pdf to be downloaded by users
    """

    def get(self, request):
        ref = request.GET.get("ref")

        publication_payment = get_object_or_404(PublicationPayment, ref=ref)

        try:
            publication_obj = Publication.objects.get(
                pk=publication_payment.publication.pk)
            publication = model_to_dict(publication_obj)

            created_at = publication_obj.created_at.date()

            read_more_link = ""

            read_more_link_2 = ""

            if (publication_obj.link):
                read_more_link = publication_obj.link.url

            if (publication_obj.readmore_link):
                read_more_link_2 = publication_obj.readmore_link

            publications_type = publication_obj.type.name

            pdf = render_to_pdf('PublicationHtml2Pdf.html', {"read_more_link": read_more_link, "read_more_link_2": read_more_link_2,
                                "created_at": created_at, "publications_type": publications_type, **publication})

            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Publication_%s.pdf" % (f"{publication['name']}")
            content = "attachment; filename=%s" % (filename)
            response['Content-Disposition'] = content
            return response
        except:
            return Response(data={"message": "failed to get publication"}, status=status.HTTP_404_NOT_FOUND)
