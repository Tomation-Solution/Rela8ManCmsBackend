# payments/views.py
import csv
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status, generics, permissions
from rest_framework.views import APIView

from utils import mailer
from .models import (
    Payment,
    PublicationPayment,
    EventTrainingRegistration,
    PublicationDownloadLink,
)
from utils.html2pdf import render_to_pdf
from trainings.models import Training
from events.models import Event

from datetime import timedelta
from django.urls import reverse
from rest_framework.views import APIView
from .serializers import (
    PublicationPaymentSerializer,
    EventTrainingRegistrationSerializer,
)
from rest_framework.pagination import PageNumberPagination
from django.template.loader import render_to_string
from weasyprint import HTML

from django.core.validators import validate_email
from django.core.exceptions import ValidationError


def process_payment(request):
    try:
        is_paid = request.data["is_paid"] if "is_paid" in request.data else True
        amount = request.data.get("amount", 0)
        if not is_paid:
            # Create payment record
            payment = Payment.objects.create(
                amount=amount,
                status="success",
            )
            return payment

        payment_method = request.data.get("paymentGateWay")
        payment_response = request.data.get("payment_response")

        if not payment_method or not amount or not payment_response:
            raise ValueError("Missing required payment data.")

        ref = ""
        access_code = ""

        # Validate based on payment method
        if payment_method == "paystack":
            if payment_response.get("status") == "success":
                ref = payment_response.get("reference", "")
            else:
                raise ValueError("Paystack payment failed")

        elif payment_method == "flutterwave":
            if payment_response.get("status") == "success":
                ref = payment_response.get("flw_ref", "")
            else:
                raise ValueError("Flutterwave payment failed")

        elif payment_method == "interswitch":
            if payment_response.get("resp") == "00":
                ref = payment_response.get("payRef", "")
            else:
                raise ValueError("Interswitch payment failed")

        else:
            raise ValueError(f"Unsupported payment method: {payment_method}")

        if not ref:
            raise ValueError("Missing payment reference.")

        # Create payment record
        payment = Payment.objects.create(
            payment_method=payment_method,
            payment_ref=ref,
            access_code=access_code,
            amount=amount,
            status="success",
        )
        return payment

    except Exception as e:
        raise e  # Raise to be caught by the view


class PaymentRedirectView(APIView):
    """
    Handles post-payment processing from inline payment flow
    """

    def post(self, request, *args, **kwargs):
        try:
            # Email validation
            email = request.data.get("email")
            if not email:
                return JsonResponse(
                    {"error": "Email address is required."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                validate_email(email)
            except ValidationError:
                return JsonResponse(
                    {"error": "Please enter a valid email address."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            payment = process_payment(request)

            data = request.data
            model_data = {
                "payment": payment,
                "fullname": data.get("fullname"),
                "email": email,
                "phone_number": data.get("phone_number"),
                "company_name": data.get("company_name"),
                "amount_to_pay": payment.amount,
            }

            if "publication" in data:
                publication_payment = PublicationPayment.objects.create(
                    **model_data,
                    publication_id=data.get("publication"),
                    is_verified=True,
                )

                # Create download link
                download_link = PublicationDownloadLink.objects.create(
                    publication_payment=publication_payment,
                    expires_at=timezone.now() + timedelta(hours=12),
                )

                # Build full URL
                download_url = request.build_absolute_uri(
                    reverse("download_publication", args=[str(download_link.token)])
                )

                # Send confirmation email to user
                mailer.sib_send_mail(
                    to=[{"email": email, "name": model_data.get('fullname')}],
                    subject="Publication Purchase Confirmation",
                    html_content=f"""
                        <p>Dear {model_data.get('fullname')},</p>
                        <p>Your publication purchase has been successfully processed.</p>
                        <p>You can download your publication using the link below:</p>
                        <p><a href="{download_url}">Download Publication</a></p>
                        <p>This link will expire in 12 hours.</p>
                        <p>Thank you for your purchase!</p>
                    """,
                )

                # Notify Admin (existing code)
                mailer.sib_send_mail(
                    to=[{"email": "info@manufacturersnigeria.org", "name": "MAN Admin"}],
                    cc=[{"email": "support@manufacturersnigeria.org"}],
                    subject=f"New Publication Payment Received",
                    html_content=f"""
                        <p><strong>New Payment Received</strong></p>
                        <p><strong>Full Name:</strong> {model_data.get('fullname')}</p>
                        <p><strong>Email:</strong> {model_data.get('email')}</p>
                        <p><strong>Phone:</strong> {model_data.get('phone_number')}</p>
                        <p><strong>Company:</strong> {model_data.get('company_name')}</p>
                        <p><strong>Amount Paid:</strong> ₦{model_data.get('amount_to_pay')}</p>
                        <p><strong>Publication ID:</strong> {data.get('publication')}</p>
                    """,
                )

                return JsonResponse(
                    {
                        "message": "Payment processed successfully. Check your email for confirmation.",
                        "download_url": download_url,
                        "expires_at": download_link.expires_at.isoformat(),
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                # Handle event/training registration
                event_type = data.get("event_type")
                model_data["event_type"] = event_type

                if event_type == "TRAINING":
                    training_id = data.get("event")
                    training_instance = Training.objects.get(id=training_id) if training_id else None
                    model_data["training"] = training_instance
                    model_data["event"] = None
                    event_name = training_instance.name if training_instance else "Training"

                elif event_type == "EVENT":
                    event_id = data.get("event")
                    event_instance = Event.objects.get(id=event_id) if event_id else None
                    model_data["event"] = event_instance
                    model_data["training"] = None
                    event_name = event_instance.name if event_instance else "Event"
                else:
                    event_name = "Event/Training"

                EventTrainingRegistration.objects.create(**model_data)

                # Send confirmation email to user
                mailer.sib_send_mail(
                    to=[{"email": email, "name": model_data.get('fullname')}],
                    subject=f"{event_type.title()} Registration Confirmation",
                    html_content=f"""
                        <p>Dear {model_data.get('fullname')},</p>
                        <p>Your request has been successfully submitted. You will be contacted soon.</p>
                        <p><strong>Registration Details:</strong></p>
                        <p><strong>Event/Training:</strong> {event_name}</p>
                        <p><strong>Type:</strong> {event_type}</p>
                        <p><strong>Email:</strong> {email}</p>
                        <p><strong>Phone:</strong> {model_data.get('phone_number')}</p>
                        <p>Thank you for registering with us!</p>
                    """,
                )

                # Notify Admin (existing code)
                mailer.sib_send_mail(
                    to=[{"email": "info@manufacturersnigeria.org", "name": "MAN Admin"}],
                    cc=[{"email": "support@manufacturersnigeria.org"}],
                    subject=f"New {event_type} Registration",
                    html_content=f"""
                        <p><strong>New Registration Received</strong></p>
                        <p><strong>Full Name:</strong> {model_data.get('fullname')}</p>
                        <p><strong>Email:</strong> {model_data.get('email')}</p>
                        <p><strong>Phone:</strong> {model_data.get('phone_number')}</p>
                        <p><strong>Company:</strong> {model_data.get('company_name')}</p>
                        <p><strong>Amount Paid:</strong> ₦{model_data.get('amount_to_pay')}</p>
                        <p><strong>Event Type:</strong> {event_type}</p>
                        <p><strong>Event/Training:</strong> {event_name}</p>
                    """,
                )

                return JsonResponse(
                    {"message": "Registration successful! Check your email for confirmation. You will be contacted soon."},
                    status=status.HTTP_200_OK,
                )

        except ValueError as ve:
            return JsonResponse({"error": str(ve)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return JsonResponse(
                {"error": "An unexpected error occurred.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

class DownloadPublicationPDFView(generics.GenericAPIView):
    """
    Download publication if user has a valid link
    """

    def get(self, request, token):
        link = get_object_or_404(PublicationDownloadLink, token=token)

        if link.is_expired():
            return JsonResponse(
                {"message": "This download link has expired."},
                status=status.HTTP_410_GONE,
            )

        payment = link.publication_payment

        if not payment or not payment.is_verified:
            return JsonResponse(
                {"message": "Payment not verified."}, status=status.HTTP_403_FORBIDDEN
            )

        publication = payment.publication
        if not publication:
            return JsonResponse(
                {"message": "Publication not found."}, status=status.HTTP_404_NOT_FOUND
            )

        # Prepare the context to be passed to the template
        publication_dict = {
            "name": publication.name,
            "title": publication.title,
            "publication_content": publication.publication_content,
        }

        # Prepare optional fields
        attachment_link = getattr(publication.link, "url", "")
        read_more_link = publication.readmore_link or ""
        publications_type = publication.type.name
        created_at = publication.created_at.date()

        context = {
            "attachment_link": attachment_link,
            "read_more_link": read_more_link,
            "created_at": created_at,
            "publications_type": publications_type,
            **publication_dict,
        }

        # Generate the PDF using the template
        pdf = render_to_pdf("PublicationHtml2Pdf.html", context)
        payment.file_received = True
        payment.save()

        response = HttpResponse(pdf, content_type="application/pdf")
        filename = f"Publication_{publication.name.replace(' ', '_')}.pdf"
        response["Content-Disposition"] = f"attachment; filename={filename}"

        return response


class PublicationPaymentPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class PublicationPaymentListView(generics.ListAPIView):
    queryset = PublicationPayment.objects.all().select_related("payment")
    serializer_class = PublicationPaymentSerializer
    pagination_class = PublicationPaymentPagination
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()

        # Get filters from query params
        payment_method = self.request.query_params.get("payment_method")
        status = self.request.query_params.get("status")
        fullname = self.request.query_params.get("fullname")
        email = self.request.query_params.get("email")
        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")

        # Apply filters if provided
        if payment_method:
            queryset = queryset.filter(payment__payment_method=payment_method)
        if status:
            queryset = queryset.filter(payment__status=status)
        if fullname:
            queryset = queryset.filter(fullname__icontains=fullname)
        if email:
            queryset = queryset.filter(email__icontains=email)
        if start_date and end_date:
            queryset = queryset.filter(
                payment__created_at__range=[start_date, end_date]
            )

        return queryset


class EventTrainingRegistrationPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class EventTrainingRegistrationListView(generics.ListAPIView):
    queryset = EventTrainingRegistration.objects.all()
    serializer_class = EventTrainingRegistrationSerializer
    pagination_class = EventTrainingRegistrationPagination
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()

        # Get filters from query params
        event_type = self.request.query_params.get("event_type")
        payment_method = self.request.query_params.get("payment_method")
        fullname = self.request.query_params.get("fullname")
        email = self.request.query_params.get("email")
        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")
        options = self.request.query_params.get("options")

        # Filter by `options`
        if options == "event":
            queryset = queryset.filter(event_type="EVENT")
        elif options == "mrc-training":
            queryset = queryset.filter(
                event_type="TRAINING", training__training_type__iexact="MRC"
            )
        elif options == "mpdcl-training":
            queryset = queryset.filter(
                event_type="TRAINING", training__training_type__iexact="MPDCL"
            )
        elif options == "others":
            queryset = (
                queryset.filter(event_type="TRAINING")
                .exclude(training__training_type__iexact="MRC")
                .exclude(training__training_type__iexact="MPDCL")
            )

        # Apply additional filters
        if event_type:
            queryset = queryset.filter(event_type=event_type)
        if payment_method:
            queryset = queryset.filter(payment__payment_method=payment_method)
        if fullname:
            queryset = queryset.filter(fullname__icontains=fullname)
        if email:
            queryset = queryset.filter(email__icontains=email)
        if start_date and end_date:
            queryset = queryset.filter(
                payment__created_at__range=[start_date, end_date]
            )

        return queryset


def publication_payment_download(request):
    # Get filters from query params
    payment_method = request.GET.get("payment_method")
    status = request.GET.get("status")
    download_format = request.GET.get("format", "pdf").lower()
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    # Start with the base queryset
    queryset = PublicationPayment.objects.select_related("payment", "publication").all()

    # Apply filters if provided
    if payment_method:
        queryset = queryset.filter(payment__payment_method=payment_method)
    if status:
        queryset = queryset.filter(payment__status=status)
    if start_date and end_date:
        queryset = queryset.filter(payment__created_at__range=[start_date, end_date])

    if download_format == "csv":
        # Create the HttpResponse object with CSV header
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = (
            'attachment; filename="publication_payments.csv"'
        )

        writer = csv.writer(response)
        # Write CSV headers
        writer.writerow(
            [
                "Full Name",
                "Email",
                "Phone Number",
                "Publication Title",
                "Amount Paid",
                "Payment Ref",
                "Payment Method",
                "Payment Status",
                "Payment Date",
            ]
        )

        for obj in queryset:
            writer.writerow(
                [
                    obj.fullname,
                    obj.email,
                    obj.phone_number,
                    obj.publication.title if obj.publication else "",
                    obj.payment.amount if obj.payment else "",
                    obj.payment.payment_ref if obj.payment else "",
                    obj.payment.payment_method if obj.payment else "",
                    obj.payment.status if obj.payment else "",
                    (
                        obj.payment.created_at.strftime("%Y-%m-%d %H:%M:%S")
                        if obj.payment
                        else ""
                    ),
                ]
            )
        return response

    # Default to PDF
    context = {"publication_payments": queryset, "now": timezone.now()}
    html_string = render_to_string("publication_payment_pdf.html", context)
    html = HTML(string=html_string)
    pdf = html.write_pdf()

    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="publication_payments.pdf"'
    return response


def event_training_registration_download(request):
    # Get filters from query params
    event_type = request.GET.get("event_type")
    payment_method = request.GET.get("payment_method")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    options = request.GET.get("options")
    download_format = request.GET.get("format", "pdf").lower()

    # Start with base queryset
    queryset = EventTrainingRegistration.objects.select_related(
        "payment", "training", "event"
    ).all()

    # Apply `options` filters
    if options == "event":
        queryset = queryset.filter(event_type="EVENT")
    elif options == "mrc-training":
        queryset = queryset.filter(
            event_type="TRAINING", training__training_type__iexact="MRC"
        )
    elif options == "mpdcl-training":
        queryset = queryset.filter(
            event_type="TRAINING", training__training_type__iexact="MPDCL"
        )
    elif options == "others":
        queryset = (
            queryset.filter(event_type="TRAINING")
            .exclude(training__training_type__iexact="MRC")
            .exclude(training__training_type__iexact="MPDCL")
        )

    # Apply other filters
    if event_type:
        queryset = queryset.filter(event_type=event_type)
    if payment_method:
        queryset = queryset.filter(payment__payment_method=payment_method)
    if start_date and end_date:
        queryset = queryset.filter(payment__created_at__range=[start_date, end_date])

    # CSV format
    if download_format == "csv":
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = (
            'attachment; filename="event_training_registrations.csv"'
        )

        writer = csv.writer(response)
        writer.writerow(
            [
                "Full Name",
                "Email",
                "Phone Number",
                "Company Name",
                "Event Type",
                "Title",
                "Amount",
                "Payment Method",
                "Status",
                "Created At",
            ]
        )

        for reg in queryset:
            title = (
                reg.training.name
                if reg.training
                else (reg.event.name if reg.event else "N/A")
            )
            writer.writerow(
                [
                    reg.fullname,
                    reg.email,
                    reg.phone_number,
                    reg.company_name,
                    reg.event_type,
                    title,
                    reg.amount_to_pay,
                    reg.payment.payment_method if reg.payment else "",
                    reg.payment.status if reg.payment else "",
                    (
                        reg.payment.created_at.strftime("%Y-%m-%d %H:%M:%S")
                        if reg.payment
                        else ""
                    ),
                ]
            )
        return response

    # Default: PDF

    # Determine option text based on the `options` parameter
    if options == "event":
        option_text = "Event Registrations"
    elif options == "mrc-training":
        option_text = "MRC Training Registrations"
    elif options == "mpdcl-training":
        option_text = "MPDCL Training Registrations"
    elif options == "others":
        option_text = "Other Training Registrations"
    else:
        option_text = "Event and Training Registrations"

    context = {"event_trainings": queryset, "option_text": option_text}

    html_string = render_to_string("event_training_registration_pdf.html", context)
    html = HTML(string=html_string)
    pdf = html.write_pdf()

    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = (
        'attachment; filename="event_training_registrations.pdf"'
    )
    return response


# from django.forms import model_to_dict
# from django.http import HttpResponse
# from django.shortcuts import get_object_or_404
# import json
# from publications.models import Publication
# from payments.models import PublicationPayment, EventTrainingRegistration, MembersAGMRegistration, ExhibitorsAGMRegistration
# from payments.serializers import PublicationPaymentSerailzer, EventTrainingRegistrationSerializer
# from utils import custom_permissions, custom_response, mailer
# from utils.extras import initialize_payment, webhook_payment_handler
# from rest_framework import generics, status
# from rest_framework.response import Response
# from django.views.decorators.csrf import csrf_exempt
# from django.template.loader import render_to_string
# from django.views.decorators.http import require_POST

# from utils.html2pdf import render_to_pdf


# # Create your views here.
# @require_POST
# @csrf_exempt
# def paystack_webhook(request, pk=None):
#     payload = json.loads(request.body)
#     meta_data = payload['data']['metadata']

#     forWhat = meta_data["forWhat"]
#     ref = payload['data']['reference']
#     amount = payload['data']['amount']

#     if payload.get('event') == 'charge.success':
#         return webhook_payment_handler(request=request, forWhat=forWhat, ref=ref, amount=amount)

#     return HttpResponse(status=500)


# class EventTrainingRegistrationView(generics.GenericAPIView):
#     """
#     class handles payments for events and trainings
#     """
#     serializer_class = EventTrainingRegistrationSerializer
#     permission_classes = [custom_permissions.IsPostRequestOrAuthenticated]

#     def get_queryset(self):
#         return EventTrainingRegistration.objects.all()

#     def get(self, request):
#         queryset = self.get_queryset()
#         serializer = self.serializer_class(queryset, many=True)
#         return custom_response.Success_response(msg="events and trainings registrations", data=serializer.data)

#     def post(self, request):
#         body = request.data
#         gatewaytype = request.GET.get("gatewaytype", "")
#         serializer = self.serializer_class(data=body)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         registration_instance = EventTrainingRegistration.objects.get(
#             ref=serializer.data["ref"], email=serializer.data["email"])

#         registation_obj = model_to_dict(registration_instance)

#         if (registration_instance.type == "EVENT" and registration_instance.event.is_paid):
#             event_amount = registration_instance.event.price
#             return initialize_payment(reason_for_payment="event_purchase",
#                                       gatewaytype=gatewaytype,
#                                       amount=event_amount, buyer_obj=registation_obj)

#         if (registration_instance.type == "TRAINING" and registration_instance.training.is_paid):
#             event_amount = registration_instance.training.price
#             return initialize_payment(reason_for_payment="training_purchase",
#                                       gatewaytype=gatewaytype,
#                                       amount=event_amount, buyer_obj=registation_obj)

#         if registration_instance.type == "EVENT":
#             registation_obj["event_training_name"] = registration_instance.event.name

#         elif registration_instance.type == "TRAINING":
#             registation_obj["event_training_name"] = registration_instance.training.name

#         email_subject = f"Registration for {registation_obj['type']}"

#         html_message = render_to_string('EventTrainingRegistration.html', {
#                                         'ref_no': registation_obj["ref"], 'client_mail': registation_obj["email"], 'registration_name': registation_obj['event_training_name'], 'type': registation_obj["type"]})

#         # my send mail utility class
#         mailer.sib_send_mail(to=[{"email": registation_obj["email"], "name": registation_obj["fullname"]}],
#                              html_content=html_message, subject=email_subject)

#         return custom_response.Success_response(msg="event or training registration", data=serializer.data)


# class PublicationPaymentView(generics.GenericAPIView):
#     """
#     class handles payments for publications
#     """
#     serializer_class = PublicationPaymentSerailzer
#     permission_classes = [custom_permissions.IsPostRequestOrAuthenticated]

#     def get_queryset(self):
#         return PublicationPayment.objects.all()

#     def get(self, request):
#         queryset = self.get_queryset()
#         serializer = self.serializer_class(queryset, many=True)

#         return custom_response.Success_response(msg="all publication payments attempted", data=serializer.data)

#     def post(self, request):
#         body = request.data
#         gatewaytype = request.GET.get("gatewaytype", "")
#         serializer = self.serializer_class(data=body)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         buyer_instance = PublicationPayment.objects.get(
#             ref=serializer.data["ref"], email=serializer.data["email"])
#         publication_amount = buyer_instance.publication.price

#         buyer_obj = model_to_dict(buyer_instance)

#         reason_for_payment = "publication_purchase"

#         return initialize_payment(reason_for_payment=reason_for_payment,
#                                   gatewaytype=gatewaytype,
#                                   amount=publication_amount, buyer_obj=buyer_obj, callback_url="https://manufacturersnigeria.org/paid-publications")


# class ViewPublicationPDF(generics.GenericAPIView):
#     """
#         class for viewing publications pdf to be downloaded by users
#     """

#     def get(self, request):
#         ref = request.GET.get("ref")

#         publication_payment = get_object_or_404(PublicationPayment, ref=ref)

#         try:
#             publication_obj = Publication.objects.get(
#                 pk=publication_payment.publication.pk)

#             publication = model_to_dict(publication_obj)

#             created_at = publication_obj.created_at.date()

#             read_more_link = ""

#             read_more_link_2 = ""

#             if (publication_obj.link):
#                 read_more_link = publication_obj.link.url

#             if (publication_obj.readmore_link):
#                 read_more_link_2 = publication_obj.readmore_link

#             publications_type = publication_obj.type.name

#             pdf = render_to_pdf('PublicationHtml2Pdf.html', {"read_more_link": read_more_link, "read_more_link_2": read_more_link_2,
#                                 "created_at": created_at, "publications_type": publications_type, **publication})
#             return HttpResponse(pdf, content_type='application/pdf')
#         except:
#             return Response(data={"message": "failed to get publication"}, status=status.HTTP_404_NOT_FOUND)


# class DownloadPublicationPDF(generics.GenericAPIView):
#     """
#         class generating the publications pdf to be downloaded by users
#     """

#     def get(self, request):
#         ref = request.GET.get("ref")

#         publication_payment = get_object_or_404(PublicationPayment, ref=ref)

#         try:
#             publication_obj = Publication.objects.get(
#                 pk=publication_payment.publication.pk)
#             publication = model_to_dict(publication_obj)

#             created_at = publication_obj.created_at.date()

#             read_more_link = ""

#             read_more_link_2 = ""

#             if (publication_obj.link):
#                 read_more_link = publication_obj.link.url

#             if (publication_obj.readmore_link):
#                 read_more_link_2 = publication_obj.readmore_link

#             publications_type = publication_obj.type.name

#             pdf = render_to_pdf('PublicationHtml2Pdf.html', {"read_more_link": read_more_link, "read_more_link_2": read_more_link_2,
#                                 "created_at": created_at, "publications_type": publications_type, **publication})

#             response = HttpResponse(pdf, content_type='application/pdf')
#             filename = "Publication_%s.pdf" % (f"{publication['name']}")
#             content = "attachment; filename=%s" % (filename)
#             response['Content-Disposition'] = content
#             return response
#         except:
#             return Response(data={"message": "failed to get publication"}, status=status.HTTP_404_NOT_FOUND)
