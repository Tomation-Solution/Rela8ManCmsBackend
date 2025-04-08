from rest_framework import generics, permissions, status, filters
from services.serializers import (
    AllServicesSerializer,
    RequestServiceSerializer,
    SubscribeToNewsLetterSerializer,
)
from services.models import RequestService, SubscribeToNewsLetter, AllServices
from utils.tokens_handler import generate_token, decode_token
from django.contrib.sites.shortcuts import get_current_site
from utils import mailer, custom_response, custom_permissions, custom_parsers
from rest_framework.parsers import FormParser
from django.urls import reverse
import jwt
from django.forms.models import model_to_dict
from django.template.loader import render_to_string
from django.shortcuts import render
from rest_framework.parsers import FormParser
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.


class RequestServiceView(generics.GenericAPIView):
    serializer_class = RequestServiceSerializer
    permission_classes = [custom_permissions.IsPostRequestOrAuthenticated]

    def get_queryset(self):
        return RequestService.objects.filter(is_verified=True)

    def get(self, request):
        all_requests = self.get_queryset()
        serializer = self.serializer_class(all_requests, many=True)

        return custom_response.Success_response(
            msg="all service request", data=serializer.data
        )

    def post(self, request):
        request_data = request.data
        serializer = self.serializer_class(data=request_data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        request_serialized = serializer.data

        request_obj = RequestService.objects.get(
            email=request_serialized["email"], ref=request_serialized["ref"]
        )

        request_obj = model_to_dict(request_obj)

        token = generate_token(
            {"name": request_obj["name"], "email": request_obj["email"]}
        )
        ref_no = request_obj["ref"]

        # setting up domain getting object
        # to get the domain of the site for redirection from the email
        current_site = get_current_site(request).domain
        # redirect to our verify-email view
        relativePath = reverse("verify-request")

        absUrl = (
            "http://"
            + current_site
            + relativePath
            + "?token="
            + str(token)
            + "&ref="
            + str(ref_no)
        )
        email_subject = "Service Request Email Verification"

        html_message = render_to_string(
            "RequestServiceMail.html",
            {"redirect_url": absUrl, "client_mail": request_obj["email"]},
        )

        # my send mail utility class
        mailer.sib_send_mail(
            to=[{"email": request_obj["email"], "name": request_obj["email"]}],
            html_content=html_message,
            subject=email_subject,
        )

        return custom_response.Success_response(
            msg="mail successfully sent", data=request_serialized
        )


class VerifyServiceRequestEmailView(generics.GenericAPIView):
    def get(self, request):
        token = request.GET.get("token")
        ref_no = request.GET.get("ref")

        try:
            payload = decode_token(token=token)
            serviceRequest: RequestService = RequestService.objects.get(
                email=payload["email"], name=payload["name"], ref=ref_no
            )

            if not serviceRequest.is_verified:
                serviceRequest.is_verified = True
                serviceRequest.save()
                return render(
                    request,
                    "ConfirmationPage.html",
                    context={"message": "service request email verified"},
                )
            return render(
                request,
                "ConfirmationPage.html",
                context={"message": "service request email verified"},
            )

        except jwt.ExpiredSignatureError as err:
            return render(
                request,
                "ConfirmationPage.html",
                context={"message": "Activation Token Expired"},
            )
        except jwt.exceptions.DecodeError as err:
            return render(
                request,
                "ConfirmationPage.html",
                context={"message": "Invalid token, request a new one"},
            )
        except:
            return render(
                request,
                "ConfirmationPage.html",
                context={"message": "Invalid token, Something went wrong"},
            )


# class SubscribeToNewsLetterVIew(generics.GenericAPIView):
#     serializer_class = SubscribeToNewsLetterSerializer
#     permission_classes = [custom_permissions.IsPostRequestOrAuthenticated]

#     def get_queryset(self):
#         return SubscribeToNewsLetter.objects.filter(is_verified=True)

#     def get(self, request):
#         queryset = self.get_queryset()
#         serializer = self.serializer_class(queryset, many=True)

#         return custom_response.Success_response(
#             msg="all newletter subscribers", data=serializer.data
#         )

#     def post(self, request):
#         email = request.data
#         serializer = self.serializer_class(data=email)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         request_serialized = serializer.data

#         request_obj = SubscribeToNewsLetter.objects.get(
#             email=request_serialized["email"], ref=request_serialized["ref"]
#         )

#         request_obj = model_to_dict(request_obj)

#         token = generate_token({"email": request_obj["email"]})
#         ref_no = request_obj["ref"]

#         current_site = get_current_site(request).domain

#         relativePath = reverse("newsletter-email-verification")

#         absUrl = (
#             "http://"
#             + current_site
#             + relativePath
#             + "?token="
#             + str(token)
#             + "&ref="
#             + str(ref_no)
#         )
#         email_subject = "MAN newsletter email verification"

#         html_message = render_to_string(
#             "NewLetterSubscriptionMail.html",
#             {"redirect_url": absUrl, "client_mail": request_obj["email"]},
#         )

#         # my send mail utility class
#         mailer.sib_send_mail(
#             to=[{"email": request_obj["email"], "name": request_obj["email"]}],
#             html_content=html_message,
#             subject=email_subject,
#         )

#         return custom_response.Success_response(
#             msg="mail successfully sent", data=request_serialized
#         )


from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10  # default size
    page_size_query_param = "page_size"  # allow client to override
    max_page_size = 100


class SubscribeToNewsLetterView(generics.ListCreateAPIView):
    serializer_class = SubscribeToNewsLetterSerializer
    permission_classes = [custom_permissions.IsPostRequestOrAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    pagination_class = StandardResultsSetPagination
    filterset_fields = ["is_verified"]
    search_fields = ["name", "email"]

    def get_queryset(self):
        queryset = SubscribeToNewsLetter.objects.all().order_by("-created_at")
        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")

        if start_date and end_date:
            queryset = queryset.filter(created_at__range=[start_date, end_date])

        return queryset

    def perform_create(self, serializer):
        instance = serializer.save()
        token = generate_token({"email": instance.email})
        origin = self.request.META.get("HTTP_ORIGIN")
        abs_url = f"{origin}/newsletter/verify?token={token}&ref={instance.ref}"

        email_subject = "MAN Newsletter Email Verification"
        html_message = render_to_string(
            "NewLetterSubscriptionMail.html",
            {"redirect_url": abs_url, "client_mail": instance.email},
        )

        mailer.sib_send_mail(
            sender="support@manufacturersnigeria.org",
            to=[{"email": instance.email, "name": instance.name}],
            html_content=html_message,
            subject=email_subject,
        )


# class VerifyNewsletterEmailView(generics.GenericAPIView):
#     def get(self, request):
#         token = request.GET.get("token")
#         ref = request.GET.get("ref")

#         try:
#             payload = decode_token(token=token)
#             newLetterSubscription: SubscribeToNewsLetter = (
#                 SubscribeToNewsLetter.objects.get(email=payload["email"], ref=ref)
#             )

#             if not newLetterSubscription.is_verified:
#                 newLetterSubscription.is_verified = True
#                 newLetterSubscription.save()
#                 return render(
#                     request,
#                     "ConfirmationPage.html",
#                     context={"message": "successfully subscribed to man newsletter"},
#                 )

#             return render(
#                 request,
#                 "ConfirmationPage.html",
#                 context={"message": "successfully subscribed to man newsletter"},
#             )

#         except jwt.ExpiredSignatureError as err:
#             return render(
#                 request,
#                 "ConfirmationPage.html",
#                 context={"message": "Activation Token Expired"},
#             )
#         except jwt.exceptions.DecodeError as err:
#             return render(
#                 request,
#                 "ConfirmationPage.html",
#                 context={"message": "Invalid token, request a new one"},
#             )
#         except:
#             return render(
#                 request,
#                 "ConfirmationPage.html",
#                 context={"message": "Invalid token, Something went wrong"},
#             )


class VerifyNewsletterSubscriptionView(APIView):
    def post(self, request):
        token = request.GET.get("token")
        ref = request.GET.get("ref")

        if not token or not ref:
            return custom_response.Error_response("Missing token or ref")

        try:
            payload = decode_token(token)
            email = payload["email"]
        except Exception as e:
            return custom_response.Error_response("Invalid or expired token")

        try:
            subscriber = SubscribeToNewsLetter.objects.get(ref=ref, email=email)
        except SubscribeToNewsLetter.DoesNotExist:
            return custom_response.Error_response("Invalid subscriber")

        subscriber.is_verified = True
        subscriber.save()

        # Notify Admin
        mailer.sib_send_mail(
            to=[
                {"email": "info@manufacturersnigeria.org", "name": "MAN Admin"},
            ],
            cc=[{"email": "support@manufacturersnigeria.org"}],
            subject="New Verified Newsletter Subscriber",
            html_content=f"<p>{subscriber.name} ({subscriber.email}) has verified their email subscription.</p>",
        )

        return custom_response.Success_response("Email successfully verified")


from .models import NewsletterUIConfig
from .serializers import NewsletterUIConfigSerializer


class NewsletterUIConfigPublicView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        try:
            config = NewsletterUIConfig.objects.first()
            if not config:
                return Response(
                    {"detail": "No UI config found."}, status=status.HTTP_404_NOT_FOUND
                )
            serializer = NewsletterUIConfigSerializer(
                config, context={"request": request}
            )
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


from rest_framework.parsers import MultiPartParser, FormParser


class NewsletterUIConfigAdminUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def put(self, request):
        config = NewsletterUIConfig.objects.first()

        data = request.data.copy()
        files = request.FILES

        if not config:
            serializer = NewsletterUIConfigSerializer(
                data=data, context={"request": request}
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # update existing
        serializer = NewsletterUIConfigSerializer(
            config, data=data, partial=True, context={"request": request}
        )

        if serializer.is_valid():
            # Save image if included
            if "form_image" in files:
                config.form_image = files["form_image"]
                config.save()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AllServicesPagination(PageNumberPagination):
    page_size = 10  # Set the number of items per page
    page_size_query_param = "page_size"  # Allow clients to specify page size
    max_page_size = 50  # Limit the max results per page


class AllServicesView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [custom_parsers.NestedMultipartParser, FormParser]
    pagination_class = AllServicesPagination

    def get(self, request):
        queryset = AllServices.objects.all().order_by("-id")  # Order latest first

        # Apply pagination
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)

        serializer = AllServicesSerializer(
            paginated_queryset, many=True, context={"request": request}
        )
        return paginator.get_paginated_response(
            {"msg": "services", "data": serializer.data}
        )

    def post(self, request):
        serializer = AllServicesSerializer(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid():
            serializer.save(writer=request.user)
            return Response(
                {"msg": "Service created successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
