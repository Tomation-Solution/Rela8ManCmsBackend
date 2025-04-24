from django.shortcuts import render
from rest_framework import generics, status, exceptions, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import FormParser, MultiPartParser
from utils import custom_parsers, custom_response, custom_permissions, mailer
from aboutus import serializers
from aboutus import models

from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

# Create your views here.


from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
import csv

from utils.html2pdf import render_to_pdf


class AboutContactUsDownloadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        format = request.data.get("format", "csv").lower()
        start_date = request.data.get("start_date")
        end_date = request.data.get("end_date")

        queryset = models.AboutContactUs.objects.all()
        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__lte=end_date)

        if format == "pdf":
            return self._download_pdf(queryset)
        return self._download_csv(queryset)

    def _download_csv(self, queryset):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="about_contact_us.csv"'

        writer = csv.writer(response)
        headers = [
            "id",
            "name",
            "phone_no",
            "email",
            "subject",
            "message",
            "created_at",
            "updated_at",
        ]
        writer.writerow(headers)

        for contact in queryset:
            writer.writerow(
                [
                    contact.id,
                    contact.name,
                    contact.phone_no,
                    contact.email,
                    contact.subject,
                    contact.message,
                    contact.created_at,
                    contact.updated_at,
                ]
            )
        return response

    def _download_pdf(self, queryset):
        data = []
        for contact in queryset:
            data.append(
                {
                    "name": contact.name,
                    "phone_no": contact.phone_no,
                    "email": contact.email,
                    "subject": contact.subject,
                    "message": contact.message,
                    "created_at": contact.created_at,
                    "updated_at": contact.updated_at,
                }
            )

        context = {
            "title": "Contact Us Messages",
            "contacts": data,
        }

        pdf = render_to_pdf("about_contact_us_pdf.html", context)
        response = HttpResponse(pdf, content_type="application/pdf")
        response["Content-Disposition"] = "attachment; filename=about_contact_us.pdf"
        return response


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


import random
from .models import EmailOTP


def generate_otp():
    return f"{random.randint(100000, 999999)}"


class AboutContactUsView(generics.GenericAPIView):
    serializer_class = serializers.AboutContactUsSerializer
    permission_classes = (custom_permissions.IsPostRequestOrAuthenticated,)
    pagination_class = CustomPagination

    def get_queryset(self):
        verified = self.request.query_params.get("verified", None) == "true"
        if verified is not None:
            return models.AboutContactUs.objects.filter(verified=verified).order_by(
                "-created_at"
            )
        return models.AboutContactUs.objects.all().order_by("-created_at")

    def get(self, request, id=None):
        contacts = self.get_queryset()
        paginator = self.pagination_class()
        paginated_qs = paginator.paginate_queryset(contacts, request)
        serializer = self.serializer_class(paginated_qs, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        print("Incoming request data:", request.data)

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        contact_instance = serializer.save()
        print("Data serialized and saved successfully.")

        otp_instance = EmailOTP.objects.create(
            email=contact_instance.email,
            message_id=contact_instance,  # Set FK to AboutContactUs
        )
        print("Created OTP instance:", otp_instance)

        # Append token and email as query params
        base_url = request.data.get("frontend_url")
        print("Received frontend_url:", base_url)

        verification_link = (
            f"{base_url}?token={otp_instance.token}&email={otp_instance.email}"
        )
        print("Generated verification link:", verification_link)

        # Notify Admin / Send verification
        mailer.sib_send_mail(
            to=[{"email": request.data["email"], "name": request.data["name"]}],
            cc=[{"email": "support@manufacturersnigeria.org"}],
            subject="Email Verification",
            html_content=f"""
            <div style="font-family: Arial, sans-serif; font-size: 16px; color: #333;">
                <p>Dear {request.data["name"].split()[0]},</p>
                <p>Thank you for reaching out to the Manufacturers Association of Nigeria (MAN).</p>
                <p>Please click the button below to verify your email address:</p>
                <p style="text-align: center;">
                    <a href="{verification_link}" style="display: inline-block; padding: 10px 20px; background-color: #2b3513; color: #fff; text-decoration: none; border-radius: 5px;">
                        Verify My Email
                    </a>
                </p>
                <p>If you did not initiate this request, you can safely ignore this email.</p>
                <p>Best regards,<br>MAN Support Team</p>
                <hr>
                <p style="font-size: 12px; color: #888;">
                    This is an automated message. Please do not reply directly to this email.
                </p>
            </div>
            """,
        )
        print("Verification email sent.")

        return custom_response.Success_response(
            msg="contact message sent",
            status_code=status.HTTP_201_CREATED,
            data=serializer.data,
        )


from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta


class VerifyEmailView(APIView):
    def post(self, request):
        token = request.data.get("token")
        email = request.data.get("email")

        if not token or not email:
            return Response(
                {"detail": "Missing token or email."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            otp_entry = EmailOTP.objects.get(token=token, email=email)
        except EmailOTP.DoesNotExist:
            return Response(
                {"detail": "Invalid token or email."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Check if the related 'AboutContactUs' entry is already verified
        about_contact = (
            otp_entry.message_id
        )  # This is the related 'AboutContactUs' entry
        if about_contact and about_contact.verified:
            return custom_response.Success_response(
                msg="Email already verified.",
                data={"email": otp_entry.email},
            )

        # Check if token has expired (15 minutes max)
        if otp_entry.is_expired():
            return Response(
                {"detail": "Token has expired."},
                status=status.HTTP_410_GONE,
            )

        # Mark the email as verified (by marking the related 'AboutContactUs' as verified)
        if about_contact:
            about_contact.verified = True
            about_contact.save()
            mailer.sib_send_mail(
                to=[{"email": otp_entry.email, "name": otp_entry.email}],
                cc=[{"email": "support@manufacturersnigeria.org"}],
                html_content="<p>Your request has been successfully submitted. You will be contacted soon</p>",
                subject="Your Message has been Delivered",
            )

        return custom_response.Success_response(
            msg="Email verified successfully.",
            data={"email": otp_entry.email},
        )


# class AboutContactUsView(generics.GenericAPIView):
#     serializer_class = serializers.AboutContactUsSerializer
#     permission_classes = (custom_permissions.IsPostRequestOrAuthenticated,)

#     def get_queryset(self):
#         return models.AboutContactUs.objects.all()

#     def get(self, request, id=None):
#         contacts = self.get_queryset()
#         serializer = self.serializer_class(contacts, many=True)
#         return custom_response.Success_response(msg="contacts", data=serializer.data)

#     def post(self, request):
#         contact_data = request.data
#         serializer = self.serializer_class(data=contact_data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         contact_data = serializer.data
#         return custom_response.Success_response(
#             msg="contact message sent",
#             status_code=status.HTTP_201_CREATED,
#             data=contact_data,
#         )


class AboutContactUsDetailsView(generics.GenericAPIView):
    serializer_class = serializers.AboutContactUsSerializer
    permission_classes = (custom_permissions.IsPostRequestOrAuthenticated,)

    def delete(self, request, id=None):
        try:
            contact = models.AboutContactUs.objects.get(id=id)
            contact.delete()
            return custom_response.Success_response(msg="contact deleted")
        except models.AboutContactUs.DoesNotExist as exp:
            raise exceptions.NotFound
        except:
            return custom_response.Response(
                {"message": "bad request"}, status=status.HTTP_400_BAD_REQUEST
            )


class AboutHistoryView(APIView):
    permission_classes = [custom_permissions.IsGetRequestOrAuthenticated]
    parser_classes = [FormParser, custom_parsers.NestedMultipartParser]

    def get(self, request):
        about_data = get_object_or_404(models.AboutHistory, id=1)
        serializer = serializers.AboutHistorySerializer(
            about_data, context={"request": request}
        )
        return custom_response.Success_response(
            msg="about history", data=serializer.data
        )

    def put(self, request):
        try:
            about_data = models.AboutHistory.objects.get(id=1)
            serializer = serializers.AboutHistorySerializer(
                about_data,
                data=request.data,
                partial=True,
                context={"request": request},
            )

            serializer.is_valid(raise_exception=True)
            serializer.save()

            return custom_response.Success_response(
                msg="about history updated", data=serializer.data
            )
        except models.AboutHistory.DoesNotExist:
            raise exceptions.NotFound
        except Exception as e:
            print(e)
            return custom_response.Response(
                {"message": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class AboutAdvocacyView(APIView):
    permission_classes = [custom_permissions.IsGetRequestOrAuthenticated]
    parser_classes = [FormParser, custom_parsers.NestedMultipartParser]

    def get(self, request):
        try:
            about_data = models.AboutAdvocacy.objects.get(id=1)
            serializer = serializers.AboutAdvocacySerializer(
                about_data, context={"request": request}
            )

            return custom_response.Success_response(
                msg="about advocacy", data=serializer.data
            )
        except models.AboutAdvocacy.DoesNotExist as exp:
            raise exceptions.NotFound
        except:
            return custom_response.Response(
                {"message": "bad request"}, status=status.HTTP_400_BAD_REQUEST
            )

    def put(self, request):
        try:
            about_data = models.AboutAdvocacy.objects.get(id=1)
            serializer = serializers.AboutAdvocacySerializer(
                about_data,
                data=request.data,
                partial=True,
                context={"request": request},
            )

            serializer.is_valid(raise_exception=True)
            serializer.save()

            return custom_response.Success_response(
                msg="about advocacy updated", data=serializer.data
            )
        except models.AboutAdvocacy.DoesNotExist:
            raise exceptions.NotFound
        except Exception as e:
            print(e)
            return custom_response.Response(
                {"message": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class AboutAffilliateView(APIView):
    permission_classes = [custom_permissions.IsGetRequestOrAuthenticated]
    parser_classes = [FormParser, custom_parsers.NestedMultipartParser]

    def get(self, request):
        try:
            about_data = models.AboutAffilliate.objects.get(id=1)
            serializer = serializers.AboutAffilliateSerializer(
                about_data, context={"request": request}
            )

            return custom_response.Success_response(
                msg="about affilliate", data=serializer.data
            )
        except models.AboutAffilliate.DoesNotExist as exp:
            raise exceptions.NotFound
        except:
            return custom_response.Response(
                {"message": "bad request"}, status=status.HTTP_400_BAD_REQUEST
            )

    def put(self, request):
        try:
            about_data = models.AboutAffilliate.objects.get(id=1)
            print(request.data)
            serializer = serializers.AboutAffilliateSerializer(
                about_data,
                data=request.data,
                partial=True,
                context={"request": request},
            )

            serializer.is_valid(raise_exception=True)
            serializer.save()

            return custom_response.Success_response(
                msg="about affilliate updated", data=serializer.data
            )
        except models.AboutAffilliate.DoesNotExist:
            raise exceptions.NotFound
        except Exception as e:
            print(e)
            return custom_response.Response(
                {"message": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class AboutHowWeWorkView(APIView):
    permission_classes = [custom_permissions.IsGetRequestOrAuthenticated]
    parser_classes = [FormParser, custom_parsers.NestedMultipartParser]

    def get(self, request):
        try:
            about_data = models.AboutHowWeWork.objects.get(id=1)
            serializer = serializers.AboutHowWeWorkSerializer(
                about_data, context={"request": request}
            )

            return custom_response.Success_response(
                msg="about how we work", data=serializer.data
            )
        except models.AboutHowWeWork.DoesNotExist as exp:
            raise exceptions.NotFound
        except:
            return custom_response.Response(
                {"message": "bad request"}, status=status.HTTP_400_BAD_REQUEST
            )

    def put(self, request):
        try:
            about_data = models.AboutHowWeWork.objects.get(id=1)
            serializer = serializers.AboutHowWeWorkSerializer(
                about_data,
                data=request.data,
                partial=True,
                context={"request": request},
            )

            serializer.is_valid(raise_exception=True)
            serializer.save()

            return custom_response.Success_response(
                msg="about how we work updated", data=serializer.data
            )
        except models.AboutHowWeWork.DoesNotExist:
            raise exceptions.NotFound
        except Exception as e:
            print(e)
            return custom_response.Response(
                {"message": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class AboutWhereWeOperatView(APIView):
    permission_classes = [custom_permissions.IsGetRequestOrAuthenticated]
    parser_classes = [FormParser, custom_parsers.NestedMultipartParser]

    def get(self, request):
        try:
            about_data = models.AboutWhereWeOperate.objects.get(id=1)
            serializer = serializers.AboutWhereWeOperateSerializer(
                about_data, context={"request": request}
            )

            return custom_response.Success_response(
                msg="about where we operate", data=serializer.data
            )
        except models.AboutWhereWeOperate.DoesNotExist as exp:
            raise exceptions.NotFound
        except:
            return custom_response.Response(
                {"message": "bad request"}, status=status.HTTP_400_BAD_REQUEST
            )

    def put(self, request):
        try:
            about_data = models.AboutWhereWeOperate.objects.get(id=1)
            serializer = serializers.AboutWhereWeOperateSerializer(
                about_data,
                data=request.data,
                partial=True,
                context={"request": request},
            )

            serializer.is_valid(raise_exception=True)
            serializer.save()

            return custom_response.Success_response(
                msg="about where we operate updated", data=serializer.data
            )
        except models.AboutWhereWeOperate.DoesNotExist:
            raise exceptions.NotFound
        except Exception as e:
            print(e)
            return custom_response.Response(
                {"message": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class AboutWhereWeOperateOfficeViews(generics.ListCreateAPIView):
    serializer_class = serializers.AboutWhereWeOperateOfficeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = models.AboutWhereWeOperateOffice.objects.all()
        return queryset

    def perform_create(self, serializer):
        return serializer.save(writer=self.request.user)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(
            data=serializer.data, msg="operation offices"
        )


class AboutWhereWeOperateOfficeDetailViews(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.AboutWhereWeOperateOfficeSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "id"

    def get_queryset(self):
        return models.AboutWhereWeOperateOffice.objects.all()


class AboutWhereWeOperateBranchViews(generics.ListCreateAPIView):
    serializer_class = serializers.AboutWhereWeOperateBranchSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = models.AboutWhereWeOperateBranch.objects.all()
        return queryset

    def perform_create(self, serializer):
        return serializer.save(writer=self.request.user)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(
            data=serializer.data, msg="branch offices"
        )


class AboutWhereWeOperateBranchDetailsViews(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.AboutWhereWeOperateBranchSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "id"

    def get_queryset(self):
        return models.AboutWhereWeOperateBranch.objects.all()


class AboutOurExecutivesPagination(PageNumberPagination):
    page_size = 10  # Set default page size
    page_size_query_param = "page_size"
    max_page_size = 50


class AboutOurExecutivesViews(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [FormParser, MultiPartParser]
    pagination_class = AboutOurExecutivesPagination

    def get(self, request):
        queryset = models.AboutOurExecutives.objects.order_by("order_position", "id")

        # Debugging - Check the first few records before pagination
        print(
            "Ordered Queryset:",
            list(queryset.values("id", "name", "order_position"))[:10],
        )
        paginator = AboutOurExecutivesPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)

        serializer = serializers.AboutOurExecutivesSerializer(
            paginated_queryset, many=True, context={"request": request}
        )

        return paginator.get_paginated_response(
            {"msg": "Our executives data", "data": serializer.data}
        )

    def post(self, request):
        serializer = serializers.AboutOurExecutivesSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save(writer=request.user)
            return custom_response.Success_response(
                msg="Executive created successfully", data=serializer.data
            )
        print(serializer.errors)
        return custom_response.Response(
            data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


class AboutOurExecutivesDetailViews(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.AboutOurExecutivesSerializer
    permission_classes = [custom_permissions.IsAuthenticated]
    parser_classes = [FormParser, custom_parsers.NestedMultipartParser]
    lookup_field = "id"

    def get_queryset(self):
        return models.AboutOurExecutives.objects.all()


# PUBLIC VIEW
class AboutWhereWeOperateBranchPublicViews(generics.ListAPIView):
    serializer_class = serializers.AboutWhereWeOperateBranchSerializer

    def get_queryset(self):
        queryset = models.AboutWhereWeOperateBranch.objects.all()
        return queryset

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(
            data=serializer.data, msg="branch offices"
        )


class AboutWhereWeOperateOfficePublicViews(generics.ListAPIView):
    serializer_class = serializers.AboutWhereWeOperateOfficeSerializer

    def get_queryset(self):
        queryset = models.AboutWhereWeOperateOffice.objects.all()
        return queryset

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(
            data=serializer.data, msg="operation offices"
        )


class AboutOurExecutivesPublicView(generics.ListAPIView):
    serializer_class = serializers.AboutOurExecutivesSerializer

    def get_queryset(self):
        return models.AboutOurExecutives.objects.all()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return custom_response.Success_response(
            data=serializer.data, msg="our executives data"
        )
