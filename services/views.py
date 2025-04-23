from rest_framework.exceptions import ValidationError
from rest_framework import generics, permissions, status, filters
from services.serializers import (
    AllServicesSerializer,
    RequestServiceSerializer,
    SubscribeToNewsLetterSerializer,
)
from services.models import RequestService, SubscribeToNewsLetter, AllServices
from utils.html2pdf import render_to_pdf
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
from django.http import HttpResponse

import csv
from io import StringIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from rest_framework.pagination import PageNumberPagination
from datetime import datetime
from rest_framework.decorators import api_view, permission_classes

from services import serializers

# Create your views here.


class PublicServiceBannerView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        try:
            banner = ServiceBanner.objects.first()
            if not banner:
                return Response(
                    {"detail": "No banner found."}, status=status.HTTP_404_NOT_FOUND
                )

            serializer = serializers.ServiceBannerSerializer(banner)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response(
                {"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ProtectedServiceBannerUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request):
        try:
            banner = ServiceBanner.objects.first()
            if not banner:
                banner = ServiceBanner.objects.create()

            serializer = serializers.ServiceBannerSerializer(
                banner, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes(
    [permissions.IsAuthenticated]
)  # or replace with your custom permission
def download_request_services(request):
    download_format = request.data.get("format", "").lower()
    queryset = RequestService.objects.all()

    print(download_format)
    print(queryset)

    # Apply optional filters (similar to your class-based view)
    is_verified = request.data.get("is_verified")
    if is_verified is not None:
        queryset = queryset.filter(is_verified=is_verified.lower() == "true")

    company_name = request.data.get("company_name")
    if company_name:
        queryset = queryset.filter(company_name__icontains=company_name)

    ref = request.data.get("ref")
    if ref:
        queryset = queryset.filter(ref__icontains=ref)

    if download_format == "csv":
        return _download_csv(queryset)
    elif download_format == "pdf":
        return _download_pdf(queryset)
    else:
        return Response({"error": "Invalid format"}, status=status.HTTP_400_BAD_REQUEST)


def _download_csv(queryset):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename=request_services.csv"

    writer = csv.writer(response)
    writer.writerow(
        [
            "Ref",
            "Name",
            "Email",
            "Company Name",
            "Message",
            "Is Verified",
            "Created At",
            "Updated At",
        ]
    )

    for request in queryset:
        writer.writerow(
            [
                request.ref,
                request.name,
                request.email,
                request.company_name,
                request.message,
                request.is_verified,
                request.created_at,
                request.updated_at,
            ]
        )

    return response


from django.http import HttpResponse
from django.template.loader import render_to_string


def _download_pdf(queryset):
    # Prepare data for template
    data = []
    for request in queryset:
        data.append(
            {
                "ref": request.ref,
                "name": request.name,
                "email": request.email,
                "company_name": request.company_name,
                "message": request.message,
                "is_verified": request.is_verified,
                "created_at": request.created_at,
                "updated_at": request.updated_at,
            }
        )

    context = {
        "title": "Request Services Report",
        "requests": data,
    }

    # Render to PDF
    pdf = render_to_pdf("request_services_pdf.html", context)

    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = "attachment; filename=request_services.pdf"
    return response


class CustomRequestServicePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class RequestServiceView(generics.GenericAPIView):
    serializer_class = RequestServiceSerializer
    permission_classes = [custom_permissions.IsPostRequestOrAuthenticated]
    pagination_class = CustomRequestServicePagination

    def get_queryset(self):
        print("=== START: get_queryset ===")

        queryset = RequestService.objects.all()
        print(f"[DEBUG] Initial queryset count: {queryset.count()}")

        # Filter by is_verified
        is_verified = self.request.query_params.get("is_verified")
        if is_verified is not None:
            is_verified_bool = is_verified.lower() == "true"
            queryset = queryset.filter(is_verified=is_verified_bool)
            print(
                f"[DEBUG] Applied is_verified={is_verified_bool} filter, count: {queryset.count()}"
            )

        # Filter by company_name
        company_name = self.request.query_params.get("company_name")
        if company_name:
            queryset = queryset.filter(company_name__icontains=company_name)
            print(
                f"[DEBUG] Applied company_name={company_name} filter, count: {queryset.count()}"
            )

        # Filter by ref
        ref = self.request.query_params.get("ref")
        if ref:
            queryset = queryset.filter(ref__icontains=ref)
            print(f"[DEBUG] Applied ref={ref} filter, count: {queryset.count()}")

        print(f"[DEBUG] Final queryset count: {queryset.count()}")
        print("=== END: get_queryset ===")
        return queryset

    def get(self, request):
        try:
            print("=== START: GET service requests ===")

            # Step 2: Get filtered and paginated queryset
            queryset = self.get_queryset()
            print(f"[INFO] Queryset count: {queryset.count()}")

            page = self.paginate_queryset(queryset)
            print(f"[INFO] Page object: {page}")

            # Step 4: Return paginated response if pagination was successful
            if page is not None:
                print("[INFO] Returning paginated response...")
                serializer = self.serializer_class(page, many=True)
                return self.get_paginated_response(serializer.data)

            # Step 5: Return normal serialized data
            print("[INFO] Returning full queryset (no pagination or download)...")
            serializer = self.serializer_class(queryset, many=True)
            return custom_response.Success_response(
                msg="All service requests", data=serializer.data
            )

        except ValidationError as e:
            print(f"[VALIDATION ERROR] {str(e)}")
            return custom_response.Error_response(
                msg="Validation error occurred", details=str(e)
            )

        except Exception as e:
            print(f"[UNEXPECTED ERROR] {str(e)}")
            return custom_response.Error_response(
                msg="An unexpected error occurred", details=str(e)
            )

    # def get_queryset(self):
    #     return RequestService.objects.filter(is_verified=True)

    # def get(self, request):
    #     all_requests = self.get_queryset()
    #     serializer = self.serializer_class(all_requests, many=True)

    #     return custom_response.Success_response(
    #         msg="all service request", data=serializer.data
    # )

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


from .models import NewsletterUIConfig, ServiceBanner
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
