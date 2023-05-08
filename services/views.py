from rest_framework import generics, permissions
from services.serializers import AllServicesSerializer, RequestServiceSerializer, SubscribeToNewsLetterSerializer
from services.models import RequestService, SubscribeToNewsLetter, AllServices
from utils.tokens_handler import generate_token, decode_token
from django.contrib.sites.shortcuts import get_current_site
from utils import mailer, custom_response, custom_permissions, custom_parsers
from rest_framework.parsers import FormParser
from django.urls import reverse
import jwt
from django.forms.models import model_to_dict
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.shortcuts import render
# Create your views here.


class RequestServiceView(generics.GenericAPIView):
    serializer_class = RequestServiceSerializer
    permission_classes = [custom_permissions.IsPostRequestOrAuthenticated]

    def get_queryset(self):
        return RequestService.objects.filter(is_verified=True)

    def get(self, request):
        all_requests = self.get_queryset()
        serializer = self.serializer_class(all_requests, many=True)

        return custom_response.Success_response(msg="all service request", data=serializer.data)

    def post(self, request):
        request_data = request.data
        serializer = self.serializer_class(data=request_data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        request_serialized = serializer.data

        request_obj = RequestService.objects.get(
            email=request_serialized["email"], ref=request_serialized["ref"])

        request_obj = model_to_dict(request_obj)

        token = generate_token(
            {"name": request_obj["name"], "email": request_obj["email"]})
        ref_no = request_obj["ref"]

        # setting up domain getting object
        # to get the domain of the site for redirection from the email
        current_site = get_current_site(request).domain
        # redirect to our verify-email view
        relativePath = reverse("verify-request")

        absUrl = "http://"+current_site+relativePath + \
            "?token="+str(token)+"&ref="+str(ref_no)
        email_subject = "Service Request Email Verification"

        html_message = render_to_string('RequestServiceMail.html', {
                                        'redirect_url': absUrl, 'client_mail': request_obj["email"]})

        # my send mail utility class
        mailer.sib_send_mail(to=[{"email": request_obj["email"], "name":request_obj["email"]}],
                             html_content=html_message, subject=email_subject)

        return custom_response.Success_response(msg="mail successfully sent", data=request_serialized)


class VerifyServiceRequestEmailView(generics.GenericAPIView):
    def get(self, request):
        token = request.GET.get("token")
        ref_no = request.GET.get("ref")

        try:
            payload = decode_token(token=token)
            serviceRequest: RequestService = RequestService.objects.get(
                email=payload["email"], name=payload["name"], ref=ref_no)

            if not serviceRequest.is_verified:
                serviceRequest.is_verified = True
                serviceRequest.save()
                return render(request, "ConfirmationPage.html", context={'message': 'service request email verified'})
            return render(request, "ConfirmationPage.html", context={'message': 'service request email verified'})

        except jwt.ExpiredSignatureError as err:
            return render(request, "ConfirmationPage.html", context={'message': 'Activation Token Expired'})
        except jwt.exceptions.DecodeError as err:
            return render(request, "ConfirmationPage.html", context={'message': "Invalid token, request a new one"})
        except:
            return render(request, "ConfirmationPage.html", context={"message": "Invalid token, Something went wrong"})


class SubscribeToNewsLetterVIew(generics.GenericAPIView):
    serializer_class = SubscribeToNewsLetterSerializer
    permission_classes = [custom_permissions.IsPostRequestOrAuthenticated]

    def get_queryset(self):
        return SubscribeToNewsLetter.objects.filter(is_verified=True)

    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)

        return custom_response.Success_response(msg="all newletter subscribers", data=serializer.data)

    def post(self, request):
        email = request.data
        serializer = self.serializer_class(data=email)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        request_serialized = serializer.data

        request_obj = SubscribeToNewsLetter.objects.get(
            email=request_serialized["email"], ref=request_serialized['ref'])

        request_obj = model_to_dict(request_obj)

        token = generate_token(
            {"email": request_obj['email']})
        ref_no = request_obj['ref']

        current_site = get_current_site(request).domain

        relativePath = reverse("newsletter-email-verification")

        absUrl = "http://"+current_site+relativePath + \
            "?token="+str(token)+"&ref="+str(ref_no)
        email_subject = "MAN newsletter email verification"

        html_message = render_to_string('NewLetterSubscriptionMail.html', {
                                        'redirect_url': absUrl, 'client_mail': request_obj["email"]})

        # my send mail utility class
        mailer.sib_send_mail(to=[{"email": request_obj["email"], "name":request_obj["email"]}],
                             html_content=html_message, subject=email_subject)

        return custom_response.Success_response(msg="mail successfully sent", data=request_serialized)


class VerifyNewsletterEmailView(generics.GenericAPIView):
    def get(self, request):
        token = request.GET.get("token")
        ref = request.GET.get("ref")

        try:
            payload = decode_token(token=token)
            newLetterSubscription: SubscribeToNewsLetter = SubscribeToNewsLetter.objects.get(
                email=payload["email"], ref=ref)

            if not newLetterSubscription.is_verified:
                newLetterSubscription.is_verified = True
                newLetterSubscription.save()
                return render(request, "ConfirmationPage.html", context={'message': 'successfully subscribed to man newsletter'})

            return render(request, "ConfirmationPage.html", context={'message': 'successfully subscribed to man newsletter'})

        except jwt.ExpiredSignatureError as err:
            return render(request, "ConfirmationPage.html", context={'message': 'Activation Token Expired'})
        except jwt.exceptions.DecodeError as err:
            return render(request, "ConfirmationPage.html", context={'message': "Invalid token, request a new one"})
        except:
            return render(request, "ConfirmationPage.html", context={"message": "Invalid token, Something went wrong"})


class AllServicesView(generics.ListCreateAPIView):
    serializer_class = AllServicesSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [custom_parsers.NestedMultipartParser, FormParser]

    def get_queryset(self):
        return AllServices.objects.all()

    def perform_create(self, serializer):
        return serializer.save(writer=self.request.user)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(data=serializer.data, msg="services")


class AllServicesDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AllServicesSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [custom_parsers.NestedMultipartParser, FormParser]
    lookup_field = "id"

    def get_queryset(self):
        return AllServices.objects.all()

# PUBLIC VIEWS


class AllServicesViewPublic(generics.ListAPIView):
    serializer_class = AllServicesSerializer

    def get_queryset(self):
        return AllServices.objects.all()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(data=serializer.data, msg="services")
